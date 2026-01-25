import random
from typing import Tuple, Any
import pygame

from core.exercise import Exercise


class MultiplicationExerciseNum(Exercise):
    """Exercise for practicing multiplication facts."""

    def __init__(self, max_number: int = 12):
        """
        Args:
            max_number: Maximum multiplier (e.g. 5 → up to 5x5)
        """
        self.max_number = max(1, min(max_number, 12))
        self._question_text = ""
        self._correct_answer = None
        self._factors = (0, 0)

    def generate_question(self) -> Tuple[str, Any]:
        """Generate a multiplication question."""
        a = random.randint(1, self.max_number)
        b = random.randint(1, self.max_number)

        self._factors = (a, b)
        self._correct_answer = a * b
        self._question_text = f"What is {a} × {b} ?"

        return self._question_text, self._correct_answer

    def validate_guess(self, guess: Any) -> Tuple[bool, float]:
        """
        Validate the guess.
        Returns:
            (is_correct, accuracy_score)
        """
        if not isinstance(guess, int):
            return False, 0.0

        if guess == self._correct_answer:
            return True, 1.0

        # Partial credit for close answers (mental math support)
        distance = abs(guess - self._correct_answer)

        if distance == 1:
            return True, 0.7
        elif distance <= 2:
            return True, 0.4
        else:
            return False, 0.0

    def get_type(self) -> str:
        return "multiplication"

    def render_question(self, screen, fonts: dict):
        """Render the multiplication question."""
        super().render_question(screen, fonts)

        # Optional visual hint: repeated groups
        font = fonts.get('small', fonts.get('font'))
        if font:
            a, b = self._factors
            hint = f"{a} groups of {b}"
            hint_surf = font.render(hint, True, (120, 120, 120))
            screen.blit(hint_surf, (50, 180))

    def render_feedback(self, screen, guess: int, correct: int, fonts: dict):
        """Render feedback after answering."""
        font = fonts.get('small', fonts.get('font'))
        if not font:
            return

        lines = [
            f"Your answer: {guess}",
            f"Correct answer: {correct}",
            f"{self._factors[0]} × {self._factors[1]} = {correct}"
        ]

        is_correct = guess == correct
        base_color = (0, 180, 0) if is_correct else (180, 0, 0)

        for i, line in enumerate(lines):
            surf = font.render(line, True, base_color)
            screen.blit(surf, (50, 240 + i * 30))
