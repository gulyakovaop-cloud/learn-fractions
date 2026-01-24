import datetime
from typing import Any


class ProgressLogger:
    """Handles logging of user progress and attempts."""

    def __init__(self, log_file: str = "progress_pygame.log"):
        self.log_file = log_file

    def log_attempt(self, exercise_type: str, question: str, correct: Any,
                   guess: Any, thinking_time: float, accuracy: float):
        """
        Log a single attempt at an exercise.

        Args:
            exercise_type: Type of exercise (e.g., "number_line")
            question: The question text
            correct: The correct answer
            guess: The user's guess
            thinking_time: Time taken to answer in seconds
            accuracy: Accuracy score (0.0 to 1.0)
        """
        timestamp = datetime.datetime.now().isoformat()
        distance = abs(float(guess) - float(correct)) if guess is not None and correct is not None else 0.0

        log_entry = (
            f"{timestamp}, {exercise_type}, {thinking_time:.2f}, "
            f"{distance:.3f}, {accuracy:.2f}, {question}, {correct}, {guess}\n"
        )

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error logging progress: {e}")