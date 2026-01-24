# TASK1: Refactoring Learn Fractions App with SOLID OOP Principles

## Current Issues Analysis

The current `learn_fractions_pygame.py` implementation has several architectural problems:

1. **Single Responsibility Violation**: The `main()` function handles UI rendering, event processing, game logic, and data persistence all in one place.

2. **Tight Coupling**: Global variables (`value`, `label`, `start_time`, etc.) create dependencies between different parts of the code.

3. **No Abstraction**: Question generation, UI rendering, and result calculation are all hardcoded for number line exercises.

4. **Difficult Extension**: Adding new exercise types requires modifying the core game loop and UI logic.

5. **Mixed Concerns**: UI code, business logic, and data persistence are interleaved.

## SOLID Principles Application Plan

### 1. Single Responsibility Principle (SRP)
Each class will have one reason to change:

- `QuestionGenerator`: Responsible for generating questions
- `UIRenderer`: Responsible for drawing UI elements
- `GameController`: Responsible for game state management
- `ProgressLogger`: Responsible for data persistence
- `InputHandler`: Responsible for processing user input

### 2. Open/Closed Principle (OCP)
The system will be open for extension but closed for modification:

- Abstract `Exercise` base class allows new exercise types without changing existing code
- `QuestionManager` can handle any `Exercise` subclass
- UI components can render different exercise types through polymorphism

### 3. Liskov Substitution Principle (LSP)
Subclasses will be substitutable for their base classes:

- Any `Exercise` subclass can be used wherever an `Exercise` is expected
- All exercise types will implement the same interface consistently

### 4. Interface Segregation Principle (ISP)
Clients won't be forced to depend on interfaces they don't use:

- `Exercise` interface will be minimal and focused
- UI rendering will be separated from exercise logic
- Input handling will be abstracted from specific exercise types

### 5. Dependency Inversion Principle (DIP)
High-level modules won't depend on low-level modules:

- `GameController` will depend on abstractions (`Exercise`, `UIRenderer`)
- Concrete implementations will be injected through dependency injection
- Configuration will determine which exercise types to use

## Proposed Class Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GameController                           │
│  - Manages overall game state                              │
│  - Coordinates between components                          │
│  - Handles main game loop                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
           ┌──────────┴──────────┐
           │                     │
┌──────────▼─────────┐  ┌────────▼──────────┐
│   QuestionManager  │  │   ProgressLogger  │
│  - Selects exercises│  │  - Logs results  │
│  - Tracks progress  │  │  - Persists data │
└──────────┬─────────┘  └───────────────────┘
           │
     ┌─────┴─────┐
     │ Exercise  │  ← Abstract Base Class
     └─────┬─────┘
           │
    ┌──────┼──────┐
    │      │      │
┌───▼──┐ ┌─▼──┐ ┌─▼──┐
│Number│ │Frac│ │Deci│
│Line   │ │tion│ │mal │
│Exerc.│ │Comp│ │Conv│
└──────┘ └────┘ └────┘
```

### Core Classes

#### 1. `Exercise` (Abstract Base Class)
```python
from abc import ABC, abstractmethod
from typing import Any, Tuple

class Exercise(ABC):
    @abstractmethod
    def generate_question(self) -> Tuple[str, Any]:
        """Generate a question and return (question_text, correct_answer)"""
        pass

    @abstractmethod
    def validate_guess(self, guess: Any, correct_answer: Any) -> float:
        """Validate user guess and return accuracy score (0.0 to 1.0)"""
        pass

    @abstractmethod
    def get_exercise_type(self) -> str:
        """Return string identifier for the exercise type"""
        pass
```

#### 2. `NumberLineExercise` (Concrete Implementation)
```python
class NumberLineExercise(Exercise):
    def generate_question(self) -> Tuple[str, float]:
        # Current random_number() logic
        pass

    def validate_guess(self, guess: float, correct_answer: float) -> float:
        # Calculate accuracy based on distance
        pass

    def get_exercise_type(self) -> str:
        return "number_line"
```

#### 3. `QuestionManager`
```python
class QuestionManager:
    def __init__(self, exercises: List[Exercise]):
        self.exercises = exercises
        self.current_exercise = None

    def get_next_question(self) -> Tuple[Exercise, str, Any]:
        """Randomly select an exercise and generate a question"""
        self.current_exercise = random.choice(self.exercises)
        question_text, correct_answer = self.current_exercise.generate_question()
        return self.current_exercise, question_text, correct_answer
```

#### 4. `UIRenderer` (Abstract Interface)
```python
class UIRenderer(ABC):
    @abstractmethod
    def render_question(self, question_text: str):
        pass

    @abstractmethod
    def render_guess_feedback(self, guess: Any, correct: Any, accuracy: float):
        pass

    @abstractmethod
    def render_next_button(self):
        pass
```

#### 5. `PygameRenderer` (Concrete Implementation)
```python
class PygameRenderer(UIRenderer):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        # Initialize fonts, colors, etc.

    def render_question(self, question_text: str):
        # Draw question text on screen
        pass

    def render_guess_feedback(self, guess: Any, correct: Any, accuracy: float):
        # Draw visual feedback for the guess
        pass
```

#### 6. `GameController`
```python
class GameController:
    def __init__(self, question_manager: QuestionManager,
                 ui_renderer: UIRenderer,
                 progress_logger: ProgressLogger,
                 input_handler: InputHandler):
        self.question_manager = question_manager
        self.ui_renderer = ui_renderer
        self.progress_logger = progress_logger
        self.input_handler = input_handler

        self.current_exercise = None
        self.current_question = None
        self.correct_answer = None
        self.start_time = None
        self.guess_made = False

    def start_new_question(self):
        self.current_exercise, self.current_question, self.correct_answer = \
            self.question_manager.get_next_question()
        self.start_time = datetime.datetime.now()
        self.guess_made = False

    def process_guess(self, guess: Any):
        if not self.guess_made:
            thinking_time = (datetime.datetime.now() - self.start_time).total_seconds()
            accuracy = self.current_exercise.validate_guess(guess, self.correct_answer)

            self.progress_logger.log_attempt(
                exercise_type=self.current_exercise.get_exercise_type(),
                question=self.current_question,
                correct_answer=self.correct_answer,
                guess=guess,
                thinking_time=thinking_time,
                accuracy=accuracy
            )

            self.guess_made = True
            return accuracy
        return None

    def run_game_loop(self):
        # Main game loop logic
        pass
```

## Step-by-Step Refactoring Plan

### Phase 1: Extract Core Classes (1-2 days)
1. Create `Exercise` abstract base class
2. Create `NumberLineExercise` class
3. Extract `QuestionManager` class
4. Create `ProgressLogger` class
5. Basic unit tests for each class

### Phase 2: UI Abstraction (1-2 days)
1. Create `UIRenderer` abstract interface
2. Create `PygameRenderer` implementation
3. Extract UI constants and helper functions
4. Separate drawing logic from game logic

### Phase 3: Game Controller (1 day)
1. Create `GameController` class
2. Implement dependency injection
3. Refactor main game loop
4. Remove global variables

### Phase 4: Input Handling (1 day)
1. Create `InputHandler` abstract interface
2. Implement `PygameInputHandler`
3. Separate input processing from game logic

### Phase 5: Configuration and Factory (1 day)
1. Create configuration system for exercise types
2. Implement factory pattern for exercise creation
3. Add command-line options for exercise selection
4. Update main entry point

### Phase 6: Testing and Documentation (1-2 days)
1. Comprehensive unit tests
2. Integration tests
3. Update documentation
4. Performance testing

## Benefits of New Design

### Extensibility
- **Easy Exercise Addition**: New exercise types only require implementing the `Exercise` interface
- **UI Flexibility**: Different UI renderers can be swapped (Pygame, Web, Console)
- **Multiple Input Methods**: Support for mouse, keyboard, touch, etc.

### Maintainability
- **Clear Separation**: Each class has a single responsibility
- **Testability**: Components can be tested in isolation
- **Debugging**: Issues are localized to specific components

### Flexibility
- **Mixed Topics**: `QuestionManager` can randomly select from any exercise type
- **Dynamic Configuration**: Exercise types can be enabled/disabled at runtime
- **Progress Tracking**: Separate logging allows for detailed analytics per exercise type

## Example Usage After Refactoring

```python
# Configuration
exercises = [
    NumberLineExercise(),
    FractionComparisonExercise(),  # Future addition
    DecimalConversionExercise(),   # Future addition
]

# Dependency injection
question_manager = QuestionManager(exercises)
ui_renderer = PygameRenderer(screen)
progress_logger = ProgressLogger("progress.log")
input_handler = PygameInputHandler()

# Create and run game
game = GameController(question_manager, ui_renderer, progress_logger, input_handler)
game.run()
```

## Migration Strategy

1. **Parallel Development**: Develop new architecture alongside existing code
2. **Gradual Migration**: Move functionality piece by piece
3. **Feature Flags**: Use configuration to switch between old and new implementations
4. **Backward Compatibility**: Ensure existing log files remain readable

## Future Exercise Types Examples

- **FractionComparisonExercise**: Compare which fraction is larger
- **DecimalConversionExercise**: Convert between fractions and decimals
- **PercentageExercise**: Estimate percentages on number lines
- **AdditionExercise**: Add fractions visually
- **MultiplicationExercise**: Estimate products on number grids

This refactoring will create a solid foundation for expanding the educational app while maintaining clean, maintainable code.</content>
<parameter name="filePath">c:\Users\gulya\src\fractions\learn-fractions\TASK1-refactoring.md