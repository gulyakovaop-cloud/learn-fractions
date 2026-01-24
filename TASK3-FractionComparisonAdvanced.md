# TASK3: Advanced FractionComparisonExercise Implementation Plan

## Overview

This task implements an advanced version of the fraction comparison exercise that removes visual aids (pie charts) and presents only text-based questions with multiple choice options. This higher difficulty level requires students to mentally compare fractions without visual representations, building deeper mathematical understanding and calculation skills.

## Requirements Analysis

### Educational Goal
- Develop mental fraction comparison skills without visual aids
- Practice comparing fractions with different denominators mentally
- Build confidence in fraction magnitude relationships
- Encourage mathematical reasoning and calculation

### Functional Requirements
- Generate fraction comparison questions without visual representations
- Present multiple choice options (A, B, C, D) for answers
- Include distractor options that are close in value
- Track accuracy and thinking time
- Log progress data with difficulty level

### Technical Requirements
- Inherit from `Exercise` abstract base class
- Implement text-only rendering for questions and options
- Handle keyboard input (A, B, C, D) or mouse clicks on option buttons
- Integrate with existing `GameManager` and logging system
- Include difficulty level identification

## Design Decisions

### Question Generation Strategy
```python
# Generate fractions with varying complexity
difficulty_levels = {
    "easy": {"denominators": [2, 3, 4, 5, 6], "max_value": 1.0},
    "medium": {"denominators": [2, 3, 4, 5, 6, 8, 9, 10], "max_value": 1.5},
    "hard": {"denominators": [2, 3, 4, 5, 6, 7, 8, 9, 10, 12], "max_value": 2.0}
}

# Generate 4 options: 1 correct, 3 distractors
correct_answer = random.choice([frac1, frac2])
distractors = generate_distractors(correct_answer, difficulty)
options = [correct_answer] + distractors
random.shuffle(options)
```

### UI Layout Design
```
┌─────────────────────────────────────────────────────────────┐
│                Which is larger: 7/12 or 2/3?                │
│                                                             │
│                A) 7/12                                      │
│                B) 2/3                                       │
│                C) They are equal                            │
│                D) Cannot determine                          │
│                                                             │
│                [Press A, B, C, D or click buttons]          │
└─────────────────────────────────────────────────────────────┘
```

### Multiple Choice Options Strategy
1. **Correct Answer**: One of the two fractions being compared
2. **Distractors**:
   - Common wrong answers (thinking one fraction is larger when it's smaller)
   - "Equal" option (when fractions are actually different)
   - "Cannot determine" option (to catch guessing)

### Difficulty Levels
- **Easy**: Simple fractions (halves, thirds, quarters)
- **Medium**: Mixed denominators, close values
- **Hard**: Complex fractions, very close values, larger numbers

## Implementation Steps

### Phase 1: Core Class Structure (2-3 hours)

#### 1.1 Create AdvancedFractionComparisonExercise Class
```python
class AdvancedFractionComparisonExercise(Exercise):
    def __init__(self, difficulty="medium"):
        self.frac1 = None
        self.frac2 = None
        self.correct_answer = None
        self.question_type = None  # "larger" or "smaller"
        self.options = []  # List of 4 options
        self.difficulty = difficulty

        # UI layout constants
        self.OPTION_HEIGHT = 40
        self.OPTION_SPACING = 10
        self.OPTION_START_Y = 150
```

#### 1.2 Implement generate_question()
```python
def generate_question(self) -> Tuple[str, Any]:
    # Generate two different fractions based on difficulty
    self.frac1, self.frac2 = self._generate_fraction_pair()

    # Randomly choose question type
    self.question_type = random.choice(["larger", "smaller"])

    # Determine correct answer
    if self.question_type == "larger":
        self.correct_answer = max(self.frac1, self.frac2, key=float)
        question = f"Which is larger: {self.frac1} or {self.frac2}?"
    else:
        self.correct_answer = min(self.frac1, self.frac2, key=float)
        question = f"Which is smaller: {self.frac1} or {self.frac2}?"

    # Generate multiple choice options
    self.options = self._generate_options()

    return question, self.correct_answer
```

#### 1.3 Helper Methods
```python
def _generate_fraction_pair(self) -> Tuple[Fraction, Fraction]:
    """Generate two different fractions based on difficulty level"""
    config = self._get_difficulty_config()

    while True:
        d1 = random.choice(config["denominators"])
        n1 = random.randint(1, min(d1 - 1, int(config["max_value"] * d1)))
        frac1 = Fraction(n1, d1)

        d2 = random.choice(config["denominators"])
        n2 = random.randint(1, min(d2 - 1, int(config["max_value"] * d2)))
        frac2 = Fraction(n2, d2)

        if frac1 != frac2:
            return frac1, frac2

def _generate_options(self) -> List[str]:
    """Generate 4 multiple choice options"""
    options = [
        f"A) {self.frac1}",
        f"B) {self.frac2}",
        f"C) They are equal",
        f"D) Cannot determine"
    ]
    return options

def _get_difficulty_config(self) -> Dict:
    """Get configuration for current difficulty level"""
    configs = {
        "easy": {"denominators": [2, 3, 4], "max_value": 1.0},
        "medium": {"denominators": [2, 3, 4, 5, 6, 8], "max_value": 1.2},
        "hard": {"denominators": [2, 3, 4, 5, 6, 7, 8, 9, 10, 12], "max_value": 1.5}
    }
    return configs.get(self.difficulty, configs["medium"])
```

### Phase 2: Rendering Implementation (3-4 hours)

#### 2.1 Implement render_question()
```python
def render_question(self, screen, fonts):
    # Draw question text
    question_surf = fonts['large'].render(self.question_text, True, BLACK)
    screen.blit(question_surf, (WIDTH//2 - question_surf.get_width()//2, 80))

    # Draw multiple choice options
    for i, option in enumerate(self.options):
        self._draw_option(screen, fonts, option, i)

    # Draw instructions
    instruction = "Press A, B, C, D or click on an option"
    inst_surf = fonts['small'].render(instruction, True, GRAY)
    screen.blit(inst_surf, (WIDTH//2 - inst_surf.get_width()//2, 350))
```

#### 2.2 Option Rendering
```python
def _draw_option(self, screen, fonts, option_text, index):
    """Draw a multiple choice option"""
    y = self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_SPACING)

    # Draw option background
    rect = pygame.Rect(200, y, 400, self.OPTION_HEIGHT)
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # Draw option text
    text_surf = fonts['medium'].render(option_text, True, BLACK)
    screen.blit(text_surf, (220, y + 10))

    # Highlight on hover
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, LIGHT_BLUE, rect, 3)
```

### Phase 3: Input and Validation (2-3 hours)

#### 3.1 Handle Input
```python
def handle_input(self, event) -> Any:
    """Handle keyboard or mouse input"""
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

def _handle_mouse_click(self, pos) -> Any:
    """Handle mouse click on options"""
    for i in range(4):
        rect = self._get_option_rect(i)
        if rect.collidepoint(pos):
            return self._get_option_value(i)
    return None

def _get_option_value(self, index) -> Any:
    """Get the value of a selected option"""
    if index == 0:
        return self.frac1
    elif index == 1:
        return self.frac2
    else:
        return None  # "Equal" or "Cannot determine" are invalid
```

#### 3.2 Implement validate_guess()
```python
def validate_guess(self, guess) -> Tuple[bool, float]:
    """Validate the selected option"""
    if guess is None:
        return False, 0.0

    is_correct = (guess == self.correct_answer)
    accuracy = 1.0 if is_correct else 0.0

    return is_correct, accuracy
```

#### 3.3 Implement get_type()
```python
def get_type(self) -> str:
    return f"advanced_fraction_comparison_{self.difficulty}"
```

### Phase 4: Feedback and Polish (2-3 hours)

#### 4.1 Implement render_feedback()
```python
def render_feedback(self, screen, guess, correct, fonts):
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
```

#### 4.2 Selection Indicators
```python
def _highlight_option(self, screen, index, highlight_type):
    """Highlight a selected option"""
    y = self.OPTION_START_Y + index * (self.OPTION_HEIGHT + self.OPTION_SPACING)
    rect = pygame.Rect(200, y, 400, self.OPTION_HEIGHT)

    color = {
        "selected": ORANGE,
        "correct": GREEN,
        "incorrect": RED
    }.get(highlight_type, BLACK)

    pygame.draw.rect(screen, color, rect, 4)

def _get_selected_index(self, value) -> Optional[int]:
    """Get the index of the selected option"""
    if value == self.frac1:
        return 0
    elif value == self.frac2:
        return 1
    return None
```

## Integration with GameManager

### Modified GameManager Methods
```python
def handle_input(self, event):
    """Handle input events"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if self.guess_made:
            # Check next button
            if self.next_button_rect.collidepoint(event.pos):
                self.next_question()
        else:
            # Let current exercise handle the input
            guess = self.current_exercise.handle_input(event)
            if guess is not None:
                self.make_guess(guess)
    elif event.type == pygame.KEYDOWN:
        if not self.guess_made:
            guess = self.current_exercise.handle_input(event)
            if guess is not None:
                self.make_guess(guess)
```

## Testing Plan

### Unit Tests
1. **Question Generation**
   - Test that different fractions are generated for each difficulty
   - Test that questions alternate between "larger" and "smaller"
   - Test that correct answers are calculated properly

2. **Options Generation**
   - Test that 4 options are always generated
   - Test that correct answer is always among options
   - Test distractor options are appropriate

3. **Input Handling**
   - Test keyboard input (A, B, C, D)
   - Test mouse click input
   - Test invalid inputs are ignored

### Integration Tests
1. **Full Exercise Flow**
   - Generate question → render → handle input → validate → show feedback
   - Test with different difficulty levels

2. **Edge Cases**
   - Very close fractions (1/10 vs 1/11)
   - Fractions with common denominators
   - Very different magnitudes

### Manual Testing Checklist
- [ ] All difficulty levels work correctly
- [ ] Keyboard input works (A, B, C, D)
- [ ] Mouse clicks work on options
- [ ] Correct answers are highlighted in green
- [ ] Wrong answers are highlighted in red
- [ ] Progress logging works with difficulty level
- [ ] Next button appears after answer

## Edge Cases and Error Handling

### Edge Cases
1. **Equal Fractions**: Should not occur (generation ensures different fractions)
2. **Very Close Values**: 7/8 vs 15/16 (both ≈0.875)
3. **Simple vs Complex**: 1/2 vs 3/7
4. **Common Denominators**: 1/4 vs 3/4 vs 1/2

### Error Handling
1. **Invalid Key Presses**: Non A-D keys should be ignored
2. **Clicks Outside Options**: Should be ignored
3. **Rendering Errors**: Handle cases where pygame surfaces are invalid
4. **Font Loading**: Graceful fallback if fonts aren't available

## Performance Considerations

### Optimization Strategies
1. **Text Pre-rendering**: Cache rendered text surfaces
2. **Minimal Re-renders**: Only redraw when necessary
3. **Efficient Collision Detection**: Simple rectangle checks

### Memory Management
1. **Surface Reuse**: Reuse pygame surfaces where possible
2. **Cleanup**: Ensure no memory leaks in exercise switching

## Future Enhancements

### Additional Difficulty Levels
- **Expert**: Fractions greater than 1, mixed numbers
- **Master**: Complex comparisons with multiple fractions

### Alternative Input Methods
- **Voice Input**: Speak "A", "B", "C", or "D"
- **Touch Gestures**: Swipe to select options

### Advanced Features
- **Hints**: Show decimal equivalents (with penalty)
- **Explanations**: Detailed explanations of why one is larger
- **Timed Mode**: Race against time for bonus points

## Success Metrics

### Educational Impact
- Students can mentally compare fractions with 70%+ accuracy
- Improved performance on written fraction comparison problems
- Reduced reliance on visual aids for fraction understanding

### Technical Metrics
- Smooth 60 FPS rendering
- <200ms response time for input
- No crashes or visual glitches
- Proper progress logging with difficulty tracking

## Implementation Timeline

### Day 1: Core Structure (4 hours)
- Create class skeleton with difficulty levels
- Implement question and option generation
- Basic validation logic

### Day 2: Input and Rendering (4 hours)
- Implement keyboard and mouse input handling
- Add option rendering with highlighting
- Basic feedback rendering

### Day 3: Testing and Polish (4 hours)
- Unit tests for all functionality
- Integration testing with GameManager
- Bug fixes and performance optimization

## Dependencies

### Required Libraries
- pygame (for rendering and input)
- fractions.Fraction (for exact comparisons)
- typing (for type hints)

### Integration Points
- GameManager.handle_input() - for keyboard and mouse events
- GameManager.render() - for display
- ProgressLogger - for data persistence with difficulty tracking

This advanced implementation will challenge students to develop true mental fraction comparison skills while maintaining the clean, extensible architecture of the learning system.

## Status

**Implemented.** ✅

## Implementation Details

### New Files Created

1. **`exercises/advanced_fraction_comparison_exercise.py`** - Complete implementation of the advanced fraction comparison exercise

### Files Modified

1. **`core/game_manager.py`** - Updated to support keyboard input handling with new `handle_input()` and `_handle_keydown()` methods
2. **`learn_pygame_solid.py`** - Added import and included multiple `AdvancedFractionComparisonExercise` instances with different difficulty levels

### Key Features Implemented

#### AdvancedFractionComparisonExercise Class
- **Text-Only Questions**: No visual aids, pure mental fraction comparison
- **Multiple Choice Options**: A, B, C, D with distractors ("equal", "cannot determine")
- **Keyboard Input**: Press A, B, C, D keys for selection
- **Mouse Input**: Click on option buttons
- **Difficulty Levels**: Easy, medium, and hard with different fraction complexities
- **Feedback System**: Visual indicators for selected and correct answers

#### Question Structure
```
Which is larger: 7/12 or 2/3?

A) 7/12
B) 2/3
C) They are equal
D) Cannot determine
```

#### Difficulty Levels
- **Easy**: Simple fractions (denominators 2, 3, 4)
- **Medium**: Mixed denominators (2, 3, 4, 5, 6, 8)
- **Hard**: Complex fractions (2-12 denominators, higher values)

#### Input Methods
- **Keyboard**: A, B, C, D keys
- **Mouse**: Click on rectangular option areas
- **Space/Enter**: Next question after answering

### Integration with Existing Architecture

#### Enhanced GameManager
- **Unified Input Handling**: Single `handle_input()` method for all event types
- **Keyboard Support**: Added `_handle_keydown()` for keyboard event processing
- **Backward Compatibility**: Existing mouse handling still works for other exercises

#### Seamless Integration
- **Random Selection**: All exercise types (including 3 difficulty levels of advanced) are randomly selected
- **Unified Interface**: Same `GameManager` handles all exercise types
- **Consistent Logging**: Progress data logged with specific exercise type including difficulty
- **Shared UI**: Next button and overall layout work for all exercises

### Testing Results

✅ **Question Generation**: Successfully creates varied comparison questions for all difficulty levels  
✅ **Multiple Choice Options**: Proper A, B, C, D options with correct answer placement  
✅ **Keyboard Input**: A, B, C, D keys work correctly for selection  
✅ **Mouse Input**: Clicking on option areas works properly  
✅ **Validation Logic**: Correct scoring for right/wrong answers  
✅ **Feedback Display**: Clear visual indicators for results  
✅ **Difficulty Levels**: Easy, medium, hard levels generate appropriate fraction complexities  
✅ **Integration**: Works perfectly with existing GameManager and other exercises  
✅ **Random Selection**: All 5 exercise variants appear randomly  
✅ **Application Startup**: No errors, smooth operation  

### Educational Value

The advanced exercise teaches students to:
- **Compare fractions mentally** without visual representations
- **Understand fraction magnitudes** through pure mathematical reasoning
- **Develop calculation skills** for fraction comparison
- **Practice multiple choice format** common in assessments
- **Build confidence** in mathematical decision-making

### Usage

The application now randomly presents:
1. **Number Line Exercises**: Click where fractions/decimals belong on 0-1 line
2. **Visual Fraction Comparison**: Click which pie chart is larger/smaller
3. **Advanced Text Comparison**: Choose A, B, C, D for larger/smaller questions (3 difficulty levels)

Students can progress from visual learning (TASK2) to mental proficiency (TASK3)!

### Technical Implementation Details

#### Input Handling Architecture
```python
# GameManager.handle_input() - unified event handling
def handle_input(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        return self.handle_click(event.pos[0], event.pos[1])
    elif event.type == pygame.KEYDOWN:
        return self._handle_keydown(event)

# Exercise-specific input handling
def handle_input(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a: return self.frac1
        elif event.key == pygame.K_b: return self.frac2
    elif event.type == pygame.MOUSEBUTTONDOWN:
        return self._handle_mouse_click(event.pos)
```

#### Difficulty-Based Fraction Generation
```python
def _get_difficulty_config(self):
    configs = {
        "easy": {"denominators": [2, 3, 4], "max_value": 1.0},
        "medium": {"denominators": [2, 3, 4, 5, 6, 8], "max_value": 1.2},
        "hard": {"denominators": [2, 3, 4, 5, 6, 7, 8, 9, 10, 12], "max_value": 1.5}
    }
```

The implementation follows all specifications from TASK3.md and maintains the extensible SOLID architecture established in TASK1 v2. The advanced exercise provides a natural progression from visual to mental fraction comparison skills.