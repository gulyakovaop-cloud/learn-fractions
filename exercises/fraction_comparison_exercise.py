import random
import math
from fractions import Fraction
from typing import Tuple, Any, Optional
import pygame

from core.exercise import Exercise


class FractionComparisonExercise(Exercise):
    """Exercise for comparing two fractions to determine which is larger or smaller."""

    def __init__(self):
        self.frac1: Optional[Fraction] = None
        self.frac2: Optional[Fraction] = None
        self.correct_answer: Optional[Fraction] = None
        self.question_type: Optional[str] = None  # "larger" or "smaller"
        self.question_text = ""

        # UI layout constants
        self.FRAC_WIDTH = 150
        self.FRAC_HEIGHT = 150
        self.FRAC1_X = 125  # Adjusted for better centering
        self.FRAC2_X = 325
        self.FRAC_Y = 150

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (200, 200, 200)

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a question asking which fraction is larger or smaller."""
        # Generate two different fractions
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

        return self.question_text, self.correct_answer

    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        """Validate the selected fraction."""
        if guess is None:
            return False, 0.0

        is_correct = (guess == self.correct_answer)
        accuracy = 1.0 if is_correct else 0.0

        return is_correct, accuracy

    def get_type(self) -> str:
        return "fraction_comparison"

    def render_question(self, screen, fonts: dict):
        """Render the comparison question with pie charts."""
        # Draw question text
        font = fonts.get('main', fonts.get('font'))
        if font:
            question_surf = font.render(self.question_text, True, self.BLACK)
            screen.blit(question_surf, (400 - question_surf.get_width()//2, 50))

        # Draw fraction 1
        self._draw_fraction_visual(screen, self.frac1, self.FRAC1_X, self.FRAC_Y)
        self._draw_fraction_text(screen, fonts, str(self.frac1), self.FRAC1_X, self.FRAC_Y)

        # Draw fraction 2
        self._draw_fraction_visual(screen, self.frac2, self.FRAC2_X, self.FRAC_Y)
        self._draw_fraction_text(screen, fonts, str(self.frac2), self.FRAC2_X, self.FRAC_Y)

        # Draw hover effects
        mouse_pos = pygame.mouse.get_pos()
        if self._get_fraction_rect(1).collidepoint(mouse_pos):
            self._draw_highlight(screen, self.FRAC1_X, self.FRAC_Y, self.BLUE)
        if self._get_fraction_rect(2).collidepoint(mouse_pos):
            self._draw_highlight(screen, self.FRAC2_X, self.FRAC_Y, self.BLUE)

    def render_feedback(self, screen, guess: Any, correct: Any, fonts: dict):
        """Render feedback showing the selected and correct answers."""
        # Show selected answer
        if guess:
            if guess == self.frac1:
                self._draw_selection_indicator(screen, self.FRAC1_X, self.FRAC_Y, "selected")
            else:
                self._draw_selection_indicator(screen, self.FRAC2_X, self.FRAC_Y, "selected")

        # Show correct answer
        if correct == self.frac1:
            self._draw_selection_indicator(screen, self.FRAC1_X, self.FRAC_Y, "correct")
        else:
            self._draw_selection_indicator(screen, self.FRAC2_X, self.FRAC_Y, "correct")

        # Show result text
        self._draw_result_text(screen, fonts, guess == correct)

    def handle_click(self, pos: tuple) -> Any:
        """Process mouse click and return selected fraction or None."""
        if self._get_fraction_rect(1).collidepoint(pos):
            return self.frac1
        elif self._get_fraction_rect(2).collidepoint(pos):
            return self.frac2
        return None

    def _generate_fraction_pair(self) -> Tuple[Fraction, Fraction]:
        """Generate two different fractions."""
        denominators = [2, 3, 4, 5, 6, 8, 9, 10, 12]

        while True:
            d1 = random.choice(denominators)
            n1 = random.randint(1, d1 - 1)  # Proper fraction
            frac1 = Fraction(n1, d1)

            d2 = random.choice(denominators)
            n2 = random.randint(1, d2 - 1)
            frac2 = Fraction(n2, d2)

            if frac1 != frac2:  # Ensure they're different
                return frac1, frac2

    def _get_fraction_rect(self, fraction_num: int) -> pygame.Rect:
        """Get clickable rectangle for a fraction."""
        if fraction_num == 1:
            return pygame.Rect(self.FRAC1_X, self.FRAC_Y,
                              self.FRAC_WIDTH, self.FRAC_HEIGHT)
        else:
            return pygame.Rect(self.FRAC2_X, self.FRAC_Y,
                              self.FRAC_WIDTH, self.FRAC_HEIGHT)

    def _draw_fraction_visual(self, screen, fraction: Fraction, x: int, y: int):
        """Draw pie chart representation of fraction."""
        center_x = x + self.FRAC_WIDTH // 2
        center_y = y + self.FRAC_HEIGHT // 2
        radius = min(self.FRAC_WIDTH, self.FRAC_HEIGHT) // 2 - 10

        # Draw circle outline
        pygame.draw.circle(screen, self.BLACK, (center_x, center_y), radius, 2)

        # Draw filled portion
        if float(fraction) > 0:
            # Calculate angle for the fraction
            angle = 2 * math.pi * float(fraction)

            # Draw filled arc using polygon
            points = [(center_x, center_y)]
            num_points = max(10, int(angle * 180 / math.pi / 5))  # Adaptive point density

            for i in range(num_points + 1):
                rad = (angle * i / num_points) - math.pi/2  # Start from top
                px = center_x + int(radius * math.cos(rad))
                py = center_y + int(radius * math.sin(rad))
                points.append((px, py))

            if len(points) > 2:
                pygame.draw.polygon(screen, self.BLUE, points)

    def _draw_fraction_text(self, screen, fonts: dict, text: str, x: int, y: int):
        """Draw fraction text below visual."""
        font = fonts.get('main', fonts.get('font'))
        if font:
            text_surf = font.render(text, True, self.BLACK)
            text_x = x + (self.FRAC_WIDTH - text_surf.get_width()) // 2
            text_y = y + self.FRAC_HEIGHT + 10
            screen.blit(text_surf, (text_x, text_y))

    def _draw_highlight(self, screen, x: int, y: int, color: tuple):
        """Draw highlight border around clickable area."""
        rect = pygame.Rect(x, y, self.FRAC_WIDTH, self.FRAC_HEIGHT)
        pygame.draw.rect(screen, color, rect, 3)

    def _draw_selection_indicator(self, screen, x: int, y: int, indicator_type: str):
        """Draw visual indicator around fraction."""
        color = {
            "selected": self.ORANGE,
            "correct": self.GREEN,
            "incorrect": self.RED
        }.get(indicator_type, self.BLACK)

        rect = pygame.Rect(x-5, y-5, self.FRAC_WIDTH+10, self.FRAC_HEIGHT+10)
        pygame.draw.rect(screen, color, rect, 4)

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
            screen.blit(text_surf, (400 - text_surf.get_width()//2, 350))