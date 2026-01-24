import random
import math
from fractions import Fraction
from typing import Tuple, Any, Optional, List
import pygame

from core.exercise import Exercise


class GridCell:
    """Represents a single cell in the multiplication grid."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = False
        self.is_correct = False  # Part of the actual product area

    def draw(self, screen: pygame.Surface, colors: dict):
        """Draw the cell with appropriate color."""
        if self.is_correct:
            color = colors['correct']  # Green for correct area
        elif self.clicked:
            color = colors['clicked']  # Blue for user selection
        else:
            color = colors['empty']  # White for unselected

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, colors['border'], self.rect, 1)  # Border


class MultiplicationExercise(Exercise):
    """Exercise for teaching fraction multiplication through visual grid representations."""

    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty

        # Difficulty configurations
        self.difficulty_config = {
            "easy": {
                "grid_size": (4, 4),  # 4x4 grid = 16 cells
                "fractions": [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)]  # Simple fractions
            },
            "medium": {
                "grid_size": (6, 6),  # 6x6 grid = 36 cells
                "fractions": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)]  # More variety
            },
            "hard": {
                "grid_size": (8, 8),  # 8x8 grid = 64 cells
                "fractions": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6)]  # Complex fractions
            }
        }

        # Current question state
        self.frac1: Optional[Tuple[int, int]] = None  # First fraction (numerator, denominator)
        self.frac2: Optional[Tuple[int, int]] = None  # Second fraction ("of" fraction)
        self.correct_answer: float = 0.0
        self.question_text = ""

        # Grid state
        self.grid_size = self.difficulty_config[difficulty]["grid_size"]
        self.cells: List[GridCell] = []
        self.clicked_cells = 0

        # UI layout constants
        self.GRID_WIDTH = 400
        self.GRID_HEIGHT = 400
        self.GRID_START_X = 50
        self.GRID_START_Y = 150

        # Colors
        self.colors = {
            'empty': (255, 255, 255),      # White
            'clicked': (0, 0, 255),        # Blue
            'correct': (0, 255, 0),        # Green
            'border': (0, 0, 0),           # Black
            'text': (0, 0, 0),             # Black
            'instruction': (100, 100, 100) # Gray
        }

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a multiplication question with visual grid."""
        config = self.difficulty_config[self.difficulty]
        fractions = config["fractions"]

        # Generate two fractions
        self.frac1 = random.choice(fractions)
        self.frac2 = random.choice(fractions)

        # Calculate correct answer (product)
        self.correct_answer = (self.frac1[0] * self.frac2[0]) / (self.frac1[1] * self.frac2[1])

        # Create question text
        self.question_text = f"What is {self.frac1[0]}/{self.frac1[1]} of {self.frac2[0]}/{self.frac2[1]}?"

        # Setup the grid
        self._setup_grid()

        return self.question_text, self.correct_answer

    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        """Validate the user's estimation based on clicked cells."""
        if not isinstance(guess, int) or guess < 0:
            return False, 0.0

        total_cells = self.grid_size[0] * self.grid_size[1]
        correct_cells = int(self.correct_answer * total_cells)

        # Calculate accuracy based on proximity to correct answer
        difference = abs(guess - correct_cells)
        max_difference = total_cells * 0.5  # Allow 50% margin for "reasonable" estimates

        if difference == 0:
            accuracy = 1.0  # Perfect
        elif difference <= max_difference:
            accuracy = max(0.1, 1.0 - (difference / max_difference))
        else:
            accuracy = 0.1  # Minimum score for very poor estimates

        is_correct = (difference <= total_cells * 0.1)  # Within 10% is considered correct

        return is_correct, accuracy

    def get_type(self) -> str:
        return f"multiplication_{self.difficulty}"

    def render_question(self, screen, fonts: dict):
        """Render the multiplication question with interactive grid."""
        # Draw question text
        main_font = fonts.get('main', fonts.get('font'))
        if main_font:
            question_surf = main_font.render(self.question_text, True, self.colors['text'])
            screen.blit(question_surf, (400 - question_surf.get_width()//2, 50))

        # Draw instruction text
        small_font = fonts.get('small', fonts.get('font'))
        if small_font:
            instruction = "Click on cells to estimate the shaded area"
            instruction_surf = small_font.render(instruction, True, self.colors['instruction'])
            screen.blit(instruction_surf, (400 - instruction_surf.get_width()//2, 100))

        # Draw the grid
        self._draw_grid(screen)

        # Draw estimation counter
        if small_font:
            estimate_text = f"Cells selected: {self.clicked_cells}"
            estimate_surf = small_font.render(estimate_text, True, self.colors['text'])
            screen.blit(estimate_surf, (50, self.GRID_START_Y + self.GRID_HEIGHT + 20))

    def render_feedback(self, screen, guess: Any, correct: Any, fonts: dict):
        """Render feedback showing the correct answer and user's estimation."""
        # Show correct shaded area
        self._show_correct_answer(screen)

        # Draw feedback text
        small_font = fonts.get('small', fonts.get('font'))
        if small_font:
            total_cells = self.grid_size[0] * self.grid_size[1]
            correct_cells = int(correct * total_cells)

            feedback_lines = [
                f"Your estimate: {guess} cells",
                f"Correct answer: {correct_cells} cells",
                f"Estimated fraction: {guess/total_cells:.3f}",
                f"Actual fraction: {correct:.3f}"
            ]

            for i, line in enumerate(feedback_lines):
                text_surf = small_font.render(line, True, self.colors['text'])
                screen.blit(text_surf, (50, self.GRID_START_Y + self.GRID_HEIGHT + 50 + i * 25))

    def handle_click(self, pos: tuple) -> Any:
        """Handle mouse click on the grid."""
        for cell in self.cells:
            if cell.rect.collidepoint(pos):
                # Toggle cell selection
                cell.clicked = not cell.clicked
                self.clicked_cells = sum(1 for c in self.cells if c.clicked)
                return self.clicked_cells  # Return current count as the guess
        return None

    def _setup_grid(self):
        """Initialize the grid cells based on geometric fraction representation."""
        self.cells = []
        cell_width = self.GRID_WIDTH // self.grid_size[0]
        cell_height = self.GRID_HEIGHT // self.grid_size[1]

        # Calculate the ratios for correct area
        frac1_ratio = self.frac1[0] / self.frac1[1]  # First fraction (width)
        frac2_ratio = self.frac2[0] / self.frac2[1]  # Second fraction (height)

        # Create cells and mark correct ones based on geometric intersection
        for row in range(self.grid_size[1]):
            for col in range(self.grid_size[0]):
                x = self.GRID_START_X + col * cell_width
                y = self.GRID_START_Y + row * cell_height

                cell = GridCell(x, y, cell_width, cell_height)
                # A cell is correct if it's within the fraction ratios
                cell.is_correct = (col < frac1_ratio * self.grid_size[0]) and (row < frac2_ratio * self.grid_size[1])
                self.cells.append(cell)

        # Reset clicked state
        self.clicked_cells = 0

    def _draw_grid(self, screen):
        """Draw the multiplication grid."""
        # Draw grid background
        grid_rect = pygame.Rect(self.GRID_START_X, self.GRID_START_Y,
                               self.GRID_WIDTH, self.GRID_HEIGHT)
        pygame.draw.rect(screen, self.colors['border'], grid_rect, 2)

        # Draw all cells
        for cell in self.cells:
            cell.draw(screen, self.colors)

        # Draw fraction labels to show the concept
        if self.frac1 and self.frac2:
            self._draw_fraction_labels(screen)

    def _draw_fraction_labels(self, screen):
        """Draw labels showing which parts represent which fractions."""
        # Label for the "of" fraction (vertical division)
        font = pygame.font.Font(None, 24)
        of_label = f"{self.frac2[0]}/{self.frac2[1]} of the area"
        of_surf = font.render(of_label, True, self.colors['text'])
        screen.blit(of_surf, (self.GRID_START_X + self.GRID_WIDTH + 10, self.GRID_START_Y))

        # Label for the first fraction (horizontal division)
        frac_label = f"{self.frac1[0]}/{self.frac1[1]} of the width"
        frac_surf = font.render(frac_label, True, self.colors['text'])
        screen.blit(frac_surf, (self.GRID_START_X, self.GRID_START_Y - 30))

    def _show_correct_answer(self, screen):
        """Show the correct shaded area after guess is made."""
        # All cells will show their correct/incorrect state
        # This is already handled in _draw_grid since is_correct is set
        pass