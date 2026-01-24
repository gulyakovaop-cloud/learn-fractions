import datetime
import random
from typing import List, Any, Optional
import pygame

from core.exercise import Exercise
from core.progress_logger import ProgressLogger


class GameManager:
    """Main coordinator for the fractions learning game."""

    def __init__(self, exercises: List[Exercise], screen: pygame.Surface,
                 fonts: dict):
        """
        Initialize the game manager.

        Args:
            exercises: List of available exercises
            screen: Pygame screen surface
            fonts: Dictionary of fonts
        """
        self.exercises = exercises
        self.screen = screen
        self.fonts = fonts

        # Game state
        self.current_exercise: Optional[Exercise] = None
        self.question_text = ""
        self.correct_answer: Any = None
        self.guess_made = False
        self.guess: Any = None
        self.start_time: Optional[datetime.datetime] = None
        self.accuracy: float = 0.0

        # Dependencies
        self.logger = ProgressLogger()

        # UI constants
        self.BUTTON_WIDTH = 150
        self.BUTTON_HEIGHT = 50
        self.BUTTON_X = 600  # WIDTH - 200, assuming WIDTH=800
        self.BUTTON_Y = 320  # HEIGHT - 80, assuming HEIGHT=400

    def next_question(self):
        """Generate the next random question."""
        self.current_exercise = random.choice(self.exercises)
        self.question_text, self.correct_answer = self.current_exercise.generate_question()
        self.guess_made = False
        self.guess = None
        self.accuracy = 0.0
        self.start_time = datetime.datetime.now()

    def make_guess(self, guess: Any) -> Optional[float]:
        """
        Process a user's guess.

        Args:
            guess: The user's guess

        Returns:
            Accuracy score if guess was processed, None if already guessed
        """
        if self.guess_made or self.current_exercise is None:
            return None

        thinking_time = (datetime.datetime.now() - self.start_time).total_seconds()
        is_correct, self.accuracy = self.current_exercise.validate_guess(guess)

        # Log the attempt
        self.logger.log_attempt(
            exercise_type=self.current_exercise.get_type(),
            question=self.question_text,
            correct=self.correct_answer,
            guess=guess,
            thinking_time=thinking_time,
            accuracy=self.accuracy
        )

        self.guess_made = True
        self.guess = guess
        return self.accuracy

    def render(self):
        """Render the current game state."""
        # Clear screen
        self.screen.fill((255, 255, 255))

        if self.current_exercise:
            # Render the exercise
            self.current_exercise.render_question(self.screen, self.fonts)

            # Render feedback if guess was made
            if self.guess_made:
                self.current_exercise.render_feedback(
                    self.screen, self.guess, self.correct_answer, self.fonts
                )

        # Draw next button
        self._draw_button("Next", self.BUTTON_X, self.BUTTON_Y,
                         self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def handle_input(self, event) -> bool:
        """
        Handle input events (mouse and keyboard).

        Args:
            event: Pygame event

        Returns:
            True if the event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_click(event.pos[0], event.pos[1])
        elif event.type == pygame.KEYDOWN:
            return self._handle_keydown(event)
        return False

    def _handle_keydown(self, event) -> bool:
        """
        Handle keyboard input.

        Args:
            event: Pygame KEYDOWN event

        Returns:
            True if the key was handled
        """
        if self.guess_made:
            # Check for next question key
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.next_question()
                return True
        else:
            # Let current exercise handle keyboard input
            if self.current_exercise and hasattr(self.current_exercise, 'handle_input'):
                guess = self.current_exercise.handle_input(event)
                if guess is not None:
                    self.make_guess(guess)
                    return True
        return False

    def _draw_button(self, text: str, x: int, y: int, width: int, height: int,
                    color: tuple = (200, 200, 200)):
        """Draw a button on the screen."""
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 2)

        font = self.fonts.get('main', self.fonts.get('font'))
        if font:
            text_surf = font.render(text, True, (0, 0, 0))
            text_x = x + (width - text_surf.get_width()) // 2
            text_y = y + (height - text_surf.get_height()) // 2
            self.screen.blit(text_surf, (text_x, text_y))