import random
from fractions import Fraction
from typing import Tuple, Any
import pygame

from core.exercise import Exercise


class NumberLineExercise(Exercise):
    """Exercise for placing fractions/decimals on a number line from 0 to 1."""

    def __init__(self):
        self._question_text = ""
        self._correct_answer = None
        self.LINE_START_X = 100
        self.LINE_END_X = 700  # WIDTH - 100, assuming WIDTH=800

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a random fraction or decimal between 0 and 1."""
        if random.choice([True, False]):
            # Generate a fraction
            numerator = random.randint(1, 14)
            denominator = random.randint(numerator + 1, 15)
            frac = Fraction(numerator, denominator)
            value = float(frac)
            display_text = str(frac)
        else:
            # Generate a decimal
            value = round(random.uniform(0.1, 0.9), 2)
            display_text = str(value)

        self._question_text = f"Click where you think {display_text} is"
        self._correct_answer = value
        return self._question_text, self._correct_answer

    def validate_guess(self, guess: float) -> Tuple[bool, float]:
        """
        Validate the guess based on distance from correct answer.
        Returns accuracy score based on how close the guess is.
        """
        if not isinstance(guess, (int, float)):
            return False, 0.0

        distance = abs(guess - self._correct_answer)

        # Perfect guess (within 0.01)
        if distance < 0.01:
            return True, 1.0
        # Very close (within 0.05)
        elif distance < 0.05:
            return True, 0.8
        # Close (within 0.1)
        elif distance < 0.1:
            return True, 0.6
        # Reasonable (within 0.2)
        elif distance < 0.2:
            return True, 0.3
        else:
            return False, 0.0

    def get_type(self) -> str:
        return "number_line"

    def render_question(self, screen, fonts: dict):
        """Render the number line and question."""
        # Draw the number line
        self._draw_number_line(screen, fonts.get('small', fonts.get('font')))

        # Draw the question text
        super().render_question(screen, fonts)

    def render_feedback(self, screen, guess: float, correct: float, fonts: dict):
        """Render the guess and correct answer on the number line."""
        small_font = fonts.get('small', fonts.get('font'))

        # Draw guess (blue circle)
        if isinstance(guess, (int, float)):
            guess_x = self.LINE_START_X + (self.LINE_END_X - self.LINE_START_X) * guess
            pygame.draw.circle(screen, (0, 0, 255), (int(guess_x), 200), 8)

        # Draw correct answer (red circle)
        correct_x = self.LINE_START_X + (self.LINE_END_X - self.LINE_START_X) * correct
        pygame.draw.circle(screen, (255, 0, 0), (int(correct_x), 200), 8)

        # Draw feedback text
        if small_font and isinstance(guess, (int, float)):
            distance = abs(guess - correct)
            feedback_lines = [
                f"Your guess: {round(guess, 3)}",
                f"Correct value: {correct}",
                f"Distance: {distance:.3f}"
            ]

            for i, line in enumerate(feedback_lines):
                color = (0, 255, 0) if distance < 0.1 else (0, 0, 0)
                text_surf = small_font.render(line, True, color)
                screen.blit(text_surf, (50, 300 + i * 25))

    def _draw_number_line(self, screen, font):
        """Draw the number line from 0 to 1 with tick marks."""
        # Main line
        pygame.draw.line(screen, (0, 0, 0), (self.LINE_START_X, 200), (self.LINE_END_X, 200), 3)

        # Tick marks and labels
        if font:
            for i in range(11):
                x = self.LINE_START_X + (self.LINE_END_X - self.LINE_START_X) * i // 10
                pygame.draw.line(screen, (0, 0, 0), (x, 190), (x, 210), 2)

                # Label
                label = font.render(str(i/10), True, (0, 0, 0))
                screen.blit(label, (x - label.get_width()//2, 215))

    def get_click_position(self, mouse_x: int, screen_width: int = 800) -> float:
        """
        Convert mouse x position to value between 0 and 1.

        Args:
            mouse_x: Mouse x coordinate
            screen_width: Screen width (for calculating line positions)

        Returns:
            Value between 0.0 and 1.0
        """
        if mouse_x < self.LINE_START_X:
            return 0.0
        elif mouse_x > self.LINE_END_X:
            return 1.0
        else:
            return (mouse_x - self.LINE_START_X) / (self.LINE_END_X - self.LINE_START_X)