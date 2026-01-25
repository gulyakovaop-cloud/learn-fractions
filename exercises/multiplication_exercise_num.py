import random
from typing import Tuple, Any, List, Optional
import pygame

from core.exercise import Exercise


class MultiplicationExerciseNum(Exercise):
    """Multiple-choice multiplication exercise."""

    def __init__(self, max_number: int = 12):
        self.max_number = max(1, min(max_number, 12))

        self.a: int = 0
        self.b: int = 0
        self.correct_answer: Optional[int] = None
        self.options: List[int] = []
        self.question_text: str = ""

        # UI layout
        self.OPTION_WIDTH = 200
        self.OPTION_HEIGHT = 50
        self.OPTION_START_X = 200
        self.OPTION_START_Y = 200
        self.OPTION_GAP = 15

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (220, 220, 220)
        self.BLUE = (0, 120, 255)
        self.GREEN = (0, 180, 0)
        self.RED = (200, 0, 0)

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a multiplication question with 4 choices."""
        self.a = random.randint(1, self.max_number)
        self.b = random.randint(1, self.max_number)
        self.correct_answer = self.a * self.b

        self.options = self._generate_options(self.correct_answer)
        self.question_text = f"What is {self.a} × {self.b} ?"

        return self.question_text, self.correct_answer

    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        if not isinstance(guess, int):
            return False, 0.0

        is_correct = (guess == self.correct_answer)
        return is_correct, 1.0 if is_correct else 0.0

    def get_type(self) -> str:
        return "multiplication_choice"

    def render_question(self, screen, fonts: dict):
        """Render question and answer choices."""
        font = fonts.get('main', fonts.get('font'))
        small_font = fonts.get('small', font)

        # Question text
        if font:
            q_surf = font.render(self.question_text, True, self.BLACK)
            screen.blit(q_surf, (400 - q_surf.get_width() // 2, 80))

        # Draw options
        mouse_pos = pygame.mouse.get_pos()

        for i, value in enumerate(self.options):
            rect = self._get_option_rect(i)
            is_hover = rect.collidepoint(mouse_pos)

            color = self.BLUE if is_hover else self.GRAY
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, self.BLACK, rect, 2, border_radius=6)

            label = chr(ord('A') + i)
            text = f"{label}. {value}"

            if small_font:
                text_surf = small_font.render(text, True, self.BLACK)
                screen.blit(
                    text_surf,
                    (
                        rect.x + 15,
                        rect.y + (self.OPTION_HEIGHT - text_surf.get_height()) // 2
                    )
                )

    def render_feedback(self, screen, guess: Any, correct: Any, fonts: dict):
        """Highlight correct and selected answers."""
        font = fonts.get('small', fonts.get('font'))

        for i, value in enumerate(self.options):
            rect = self._get_option_rect(i)

            if value == correct:
                pygame.draw.rect(screen, self.GREEN, rect, 4, border_radius=6)
            elif guess == value:
                pygame.draw.rect(screen, self.RED, rect, 4, border_radius=6)

        # Result text
        if font and guess is not None:
            is_correct = (guess == correct)
            text = "Correct! ✓" if is_correct else "Incorrect ✗"
            color = self.GREEN if is_correct else self.RED

            text_surf = font.render(text, True, color)
            screen.blit(text_surf, (400 - text_surf.get_width() // 2, 360))

    def handle_click(self, pos: tuple) -> Any:
        """Return selected answer based on mouse click."""
        for i, value in enumerate(self.options):
            if self._get_option_rect(i).collidepoint(pos):
                return value
        return None

    # ---------- Helpers ----------

    def _generate_options(self, correct: int) -> List[int]:
        """Generate plausible wrong answers."""
        options = {correct}

        while len(options) < 4:
            delta = random.choice([-3, -2, -1, 1, 2, 3, 5])
            wrong = correct + delta

            if wrong > 0:
                options.add(wrong)

        opts = list(options)
        random.shuffle(opts)
        return opts

    def _get_option_rect(self, index: int) -> pygame.Rect:
        """Get rectangle for option A/B/C/D."""
        return pygame.Rect(
            self.OPTION_START_X,
            self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_GAP),
            self.OPTION_WIDTH,
            self.OPTION_HEIGHT
        )
