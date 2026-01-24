import pygame
import sys

from core.game_manager import GameManager
from exercises.number_line_exercise import NumberLineExercise
from exercises.fraction_comparison_exercise import FractionComparisonExercise
from exercises.advanced_fraction_comparison_exercise import AdvancedFractionComparisonExercise
from exercises.multiplication_exercise import MultiplicationExercise


def main():
    """Main entry point for the refactored fractions learning game."""
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 400

    # Colors (keeping for compatibility)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GRAY = (200, 200, 200)

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Learn Fractions - SOLID Refactored Edition")

    # Fonts
    fonts = {
        'main': pygame.font.Font(None, 36),
        'small': pygame.font.Font(None, 24),
        'font': pygame.font.Font(None, 36),  # Alias for backward compatibility
    }

    # Create exercises
    exercises = [
        NumberLineExercise(),
        FractionComparisonExercise(),
        AdvancedFractionComparisonExercise(difficulty="easy"),
        AdvancedFractionComparisonExercise(difficulty="medium"),
        AdvancedFractionComparisonExercise(difficulty="hard"),
        MultiplicationExercise(difficulty="easy"),
        # MultiplicationExercise(difficulty="medium"),
        # MultiplicationExercise(difficulty="hard"),
    ]

    # Create game manager
    game_manager = GameManager(exercises, screen, fonts)

    # Initialize first question
    game_manager.next_question()

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Let game manager handle all input events (mouse and keyboard)
                game_manager.handle_input(event)

        # Render everything
        game_manager.render()

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()