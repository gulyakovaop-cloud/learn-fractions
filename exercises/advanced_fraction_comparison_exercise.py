import random
from fractions import Fraction
from typing import Tuple, Any, Optional, List, Dict
import pygame

from core.exercise import Exercise


class AdvancedFractionComparisonExercise(Exercise):
    """Advanced exercise for comparing fractions without visual aids - text-only multiple choice."""

    def __init__(self, difficulty: str = "medium"):
        self.frac1: Optional[Fraction] = None
        self.frac2: Optional[Fraction] = None
        self.correct_answer: Optional[Fraction] = None
        self.question_type: Optional[str] = None  # "larger" or "smaller"
        self.options: List[str] = []  # List of 4 multiple choice options
        self.difficulty = difficulty
        self.question_text = ""

        # UI layout constants
        self.OPTION_HEIGHT = 40
        self.OPTION_SPACING = 10
        self.OPTION_START_Y = 150
        self.OPTION_WIDTH = 400
        self.OPTION_START_X = 200

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a text-only fraction comparison question."""
        # Generate two different fractions based on difficulty
        self.frac1, self.frac2 = self._generate_fraction_pair()

        # Randomly choose question type
        self.question_type = random.choice(["larger", "smaller"])

        # Determine correct answer
        if self.question_type == "larger":
            self.correct_answer = max(self.frac1, self.frac2, key=float)
            self.question_text = f"Which is larger: {self.frac1} or {self.frac2}?"
        else:
            self.correct_answer = min(self.frac1, self.frac2, key=float)
            self.question_text = f"Which is smaller: {self.frac1} or {self.frac2}?"

        # Generate multiple choice options
        self.options = self._generate_options()

        return self.question_text, self.correct_answer

    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        """Validate the selected option."""
        if guess is None:
            return False, 0.0

        is_correct = (guess == self.correct_answer)
        accuracy = 1.0 if is_correct else 0.0

        return is_correct, accuracy

    def get_type(self) -> str:
        return f"advanced_fraction_comparison_{self.difficulty}"

    def render_question(self, screen, fonts: dict):
        """Render the text-only question with multiple choice options."""
        # Draw question text
        font = fonts.get('main', fonts.get('font'))
        if font:
            question_surf = font.render(self.question_text, True, self.BLACK)
            screen.blit(question_surf, (400 - question_surf.get_width()//2, 50))

        # Draw multiple choice options
        for i, option in enumerate(self.options):
            self._draw_option(screen, fonts, option, i)

        # Draw instructions
        small_font = fonts.get('small', fonts.get('font'))
        if small_font:
            instruction = "Press A, B, C, D or click on an option"
            inst_surf = small_font.render(instruction, True, self.GRAY)
            screen.blit(inst_surf, (400 - inst_surf.get_width()//2, 350))

    def render_feedback(self, screen, guess: Any, correct: Any, fonts: dict):
        """Render feedback showing selected and correct answers."""
        # Show selected answer
        if guess:
            selected_index = self._get_selected_index(guess)
            if selected_index is not None:
                self._highlight_option(screen, selected_index, "selected")

        # Show correct answer
        correct_index = self._get_selected_index(correct)
        if correct_index is not None:
            self._highlight_option(screen, correct_index, "correct")

        # Show result text
        self._draw_result_text(screen, fonts, guess == correct)

    def handle_input(self, event) -> Any:
        """Handle keyboard or mouse input for multiple choice selection."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                return self._get_option_value(0)
            elif event.key == pygame.K_b:
                return self._get_option_value(1)
            elif event.key == pygame.K_c:
                return self._get_option_value(2)
            elif event.key == pygame.K_d:
                return self._get_option_value(3)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event.pos)

        return None

    def _generate_fraction_pair(self) -> Tuple[Fraction, Fraction]:
        """Generate two different fractions based on difficulty level."""
        config = self._get_difficulty_config()

        while True:
            d1 = random.choice(config["denominators"])
            n1 = random.randint(1, min(d1 - 1, int(config["max_value"] * d1)))
            frac1 = Fraction(n1, d1)

            d2 = random.choice(config["denominators"])
            n2 = random.randint(1, min(d2 - 1, int(config["max_value"] * d2)))
            frac2 = Fraction(n2, d2)

            if frac1 != frac2:  # Ensure they're different
                return frac1, frac2

    def _generate_options(self) -> List[str]:
        """Generate 4 multiple choice options."""
        return [
            f"A) {self.frac1}",
            f"B) {self.frac2}",
            f"C) They are equal",
            f"D) Cannot determine"
        ]

    def _get_difficulty_config(self) -> Dict:
        """Get configuration for current difficulty level."""
        configs = {
            "easy": {"denominators": [2, 3, 4], "max_value": 1.0},
            "medium": {"denominators": [2, 3, 4, 5, 6, 8], "max_value": 1.2},
            "hard": {"denominators": [2, 3, 4, 5, 6, 7, 8, 9, 10, 12], "max_value": 1.5}
        }
        return configs.get(self.difficulty, configs["medium"])

    def _draw_option(self, screen, fonts: dict, option_text: str, index: int):
        """Draw a multiple choice option."""
        y = self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_SPACING)

        # Draw option background
        rect = pygame.Rect(self.OPTION_START_X, y, self.OPTION_WIDTH, self.OPTION_HEIGHT)
        pygame.draw.rect(screen, self.WHITE, rect)
        pygame.draw.rect(screen, self.BLACK, rect, 2)

        # Draw option text
        font = fonts.get('main', fonts.get('font'))
        if font:
            text_surf = font.render(option_text, True, self.BLACK)
            screen.blit(text_surf, (self.OPTION_START_X + 20, y + 10))

        # Highlight on hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.LIGHT_BLUE, rect, 3)

    def _handle_mouse_click(self, pos: tuple) -> Any:
        """Handle mouse click on options."""
        for i in range(4):
            rect = self._get_option_rect(i)
            if rect.collidepoint(pos):
                return self._get_option_value(i)
        return None

    def _get_option_value(self, index: int) -> Any:
        """Get the value of a selected option."""
        if index == 0:
            return self.frac1
        elif index == 1:
            return self.frac2
        else:
            return None  # "Equal" or "Cannot determine" are invalid choices

    def _get_option_rect(self, index: int) -> pygame.Rect:
        """Get the rectangle for an option."""
        y = self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_SPACING)
        return pygame.Rect(self.OPTION_START_X, y, self.OPTION_WIDTH, self.OPTION_HEIGHT)

    def _highlight_option(self, screen, index: int, highlight_type: str):
        """Highlight a selected option."""
        y = self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_SPACING)
        rect = pygame.Rect(self.OPTION_START_X, y, self.OPTION_WIDTH, self.OPTION_HEIGHT)

        color = {
            "selected": self.ORANGE,
            "correct": self.GREEN,
            "incorrect": self.RED
        }.get(highlight_type, self.BLACK)

        pygame.draw.rect(screen, color, rect, 4)

    def _get_selected_index(self, value) -> Optional[int]:
        """Get the index of the selected option."""
        if value == self.frac1:
            return 0
        elif value == self.frac2:
            return 1
        return None

    def _draw_result_text(self, screen, fonts: dict, is_correct: bool):
        """Draw result message."""
        if is_correct:
            text = "Correct! ✓"
            color = self.GREEN
        else:
            text = "Incorrect ✗"
            color = self.RED

        font = fonts.get('main', fonts.get('font'))
        if font:
            text_surf = font.render(text, True, color)
            screen.blit(text_surf, (400 - text_surf.get_width()//2, 320))