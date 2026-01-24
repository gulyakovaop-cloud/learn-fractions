from abc import ABC, abstractmethod
from typing import Tuple, Any


class Exercise(ABC):
    """Abstract base class for all exercise types in the fractions learning app."""

    @abstractmethod
    def generate_question(self) -> Tuple[str, Any]:
        """
        Generate a new question for this exercise.

        Returns:
            Tuple of (question_text, correct_answer)
        """
        pass

    @abstractmethod
    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        """
        Validate a user's guess against the correct answer.

        Args:
            guess: The user's guess (type depends on exercise)

        Returns:
            Tuple of (is_correct: bool, accuracy_score: float)
            accuracy_score should be between 0.0 and 1.0
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Return a string identifier for this exercise type.

        Returns:
            String like "number_line", "fraction_comparison", etc.
        """
        pass

    def render_question(self, screen, fonts: dict):
        """
        Render the question on the screen.
        Default implementation renders the question text.
        Subclasses can override for custom rendering.

        Args:
            screen: Pygame screen surface
            fonts: Dictionary of fonts (e.g., {'main': font, 'small': small_font})
        """
        if hasattr(self, '_question_text'):
            font = fonts.get('main', fonts.get('font'))
            if font:
                question_surf = font.render(self._question_text, True, (0, 0, 0))
                screen.blit(question_surf, (400 - question_surf.get_width()//2, 50))

    def render_feedback(self, screen, guess: Any, correct: Any, fonts: dict):
        """
        Render feedback after a guess is made.
        Default implementation shows basic text feedback.
        Subclasses can override for custom feedback rendering.

        Args:
            screen: Pygame screen surface
            guess: The user's guess
            correct: The correct answer
            fonts: Dictionary of fonts
        """
        small_font = fonts.get('small', fonts.get('font'))
        if small_font:
            feedback_lines = [
                f"Your guess: {guess}",
                f"Correct: {correct}"
            ]

            for i, line in enumerate(feedback_lines):
                color = (0, 255, 0) if str(guess) == str(correct) else (0, 0, 0)
                text_surf = small_font.render(line, True, color)
                screen.blit(text_surf, (50, 350 + i * 25))