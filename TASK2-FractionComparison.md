# TASK2: FractionComparisonExercise Implementation Plan

## Overview

This task implements a new exercise type that teaches fraction comparison skills. Students will be presented with two fractions and asked to identify which is larger or smaller. This builds on the refactored architecture from TASK1 v2.

## Requirements Analysis

### Educational Goal
- Help students develop intuition for fraction magnitudes
- Practice comparing fractions with different denominators
- Build understanding that fractions represent parts of a whole

### Functional Requirements
- Generate two random fractions for comparison
- Randomly ask "which is larger" or "which is smaller"
- Provide visual feedback showing the correct answer
- Track accuracy and thinking time
- Log progress data

### Technical Requirements
- Inherit from `Exercise` abstract base class
- Implement custom rendering for side-by-side fraction display
- Handle mouse clicks on fraction choices
- Integrate with existing `GameManager` and logging system

## Design Decisions

### Question Generation Strategy
```python
# Generate fractions with denominators 2-12 to keep it manageable
denominators = [2, 3, 4, 5, 6, 8, 9, 10, 12]
numerators = range(1, max_denominator)  # Avoid improper fractions initially

# Ensure fractions are different
while frac1 == frac2:
    frac1 = Fraction(random.choice(numerators), random.choice(denominators))
    frac2 = Fraction(random.choice(numerators), random.choice(denominators))
```

### UI Layout Design
```
┌─────────────────────────────────────────────────────────────┐
│                Which is larger: 1/3 or 2/5?                 │
│                                                             │
│                ┌─────────────┐         ┌─────────────┐       │
│                │     1/3     │         │     2/5     │       │
│                │             │         │             │       │
│                │  [Visual    │         │  [Visual    │       │
│                │   representation]     │   representation]   │
│                │             │         │             │       │
│                │   (clickable)│         │   (clickable)│       │
│                └─────────────┘         └─────────────┘       │
│                                                             │
│                        [Next Question]                      │
└─────────────────────────────────────────────────────────────┘
```

### Visual Representation Options
1. **Pie Charts**: Show portions of circles
2. **Bar Charts**: Show relative heights
3. **Number Lines**: Show positions on 0-1 line
4. **Rectangles**: Show filled portions of rectangles

**Decision**: Start with pie charts as they're most intuitive for fractions.

### Input Handling
- Mouse click detection on fraction areas
- Visual feedback on hover (highlight clickable areas)
- Clear indication of selected choice before confirmation

## Implementation Steps

### Phase 1: Core Class Structure (2-3 hours)

#### 1.1 Create FractionComparisonExercise Class
```python
class FractionComparisonExercise(Exercise):
    def __init__(self):
        self.frac1 = None
        self.frac2 = None
        self.correct_answer = None
        self.question_type = None  # "larger" or "smaller"
        self.selected_answer = None

        # UI layout constants
        self.FRAC_WIDTH = 150
        self.FRAC_HEIGHT = 150
        self.FRAC1_X = 150
        self.FRAC2_X = 350
        self.FRAC_Y = 200
```

#### 1.2 Implement generate_question()
```python
def generate_question(self) -> Tuple[str, Fraction]:
    # Generate two different fractions
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

    return question, self.correct_answer
```

#### 1.3 Helper Methods
```python
def _generate_fraction_pair(self) -> Tuple[Fraction, Fraction]:
    """Generate two different fractions"""
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
    """Get clickable rectangle for a fraction"""
    if fraction_num == 1:
        return pygame.Rect(self.FRAC1_X, self.FRAC_Y,
                          self.FRAC_WIDTH, self.FRAC_HEIGHT)
    else:
        return pygame.Rect(self.FRAC2_X, self.FRAC_Y,
                          self.FRAC_WIDTH, self.FRAC_HEIGHT)
```

### Phase 2: Rendering Implementation (3-4 hours)

#### 2.1 Implement render_question()
```python
def render_question(self, screen, fonts):
    # Draw question text
    question_surf = fonts['large'].render(self.question_text, True, BLACK)
    screen.blit(question_surf, (WIDTH//2 - question_surf.get_width()//2, 80))

    # Draw fraction 1
    self._draw_fraction_visual(screen, self.frac1, self.FRAC1_X, self.FRAC_Y)
    self._draw_fraction_text(screen, fonts, str(self.frac1), self.FRAC1_X, self.FRAC_Y)

    # Draw fraction 2
    self._draw_fraction_visual(screen, self.frac2, self.FRAC2_X, self.FRAC_Y)
    self._draw_fraction_text(screen, fonts, str(self.frac2), self.FRAC2_X, self.FRAC_Y)

    # Draw hover effects
    mouse_pos = pygame.mouse.get_pos()
    if self._get_fraction_rect(1).collidepoint(mouse_pos):
        self._draw_highlight(screen, self.FRAC1_X, self.FRAC_Y)
    if self._get_fraction_rect(2).collidepoint(mouse_pos):
        self._draw_highlight(screen, self.FRAC2_X, self.FRAC_Y)
```

#### 2.2 Pie Chart Visualization
```python
def _draw_fraction_visual(self, screen, fraction, x, y):
    """Draw pie chart representation of fraction"""
    center_x = x + self.FRAC_WIDTH // 2
    center_y = y + self.FRAC_HEIGHT // 2
    radius = min(self.FRAC_WIDTH, self.FRAC_HEIGHT) // 2 - 10

    # Draw circle outline
    pygame.draw.circle(screen, BLACK, (center_x, center_y), radius, 2)

    # Draw filled portion
    if fraction > 0:
        # Calculate angle for the fraction
        angle = 2 * math.pi * float(fraction)

        # Draw filled arc
        points = [(center_x, center_y)]
        for i in range(0, int(angle * 180 / math.pi) + 1):
            rad = math.radians(i)
            px = center_x + int(radius * math.cos(rad - math.pi/2))
            py = center_y + int(radius * math.sin(rad - math.pi/2))
            points.append((px, py))

        if len(points) > 2:
            pygame.draw.polygon(screen, BLUE, points)
```

#### 2.3 Text and Highlight Rendering
```python
def _draw_fraction_text(self, screen, fonts, text, x, y):
    """Draw fraction text below visual"""
    text_surf = fonts['medium'].render(text, True, BLACK)
    text_x = x + (self.FRAC_WIDTH - text_surf.get_width()) // 2
    text_y = y + self.FRAC_HEIGHT + 10
    screen.blit(text_surf, (text_x, text_y))

def _draw_highlight(self, screen, x, y):
    """Draw highlight border around clickable area"""
    rect = pygame.Rect(x, y, self.FRAC_WIDTH, self.FRAC_HEIGHT)
    pygame.draw.rect(screen, GREEN, rect, 3)
```

### Phase 3: Input and Validation (2-3 hours)

#### 3.1 Handle Mouse Input
```python
def handle_click(self, pos) -> Any:
    """Process mouse click and return selected fraction or None"""
    if self._get_fraction_rect(1).collidepoint(pos):
        return self.frac1
    elif self._get_fraction_rect(2).collidepoint(pos):
        return self.frac2
    return None
```

#### 3.2 Implement validate_guess()
```python
def validate_guess(self, guess) -> Tuple[bool, float]:
    """Validate the selected fraction"""
    if guess is None:
        return False, 0.0

    is_correct = (guess == self.correct_answer)
    accuracy = 1.0 if is_correct else 0.0

    return is_correct, accuracy
```

#### 3.3 Implement get_type()
```python
def get_type(self) -> str:
    return "fraction_comparison"
```

### Phase 4: Feedback Rendering (2-3 hours)

#### 4.1 Implement render_feedback()
```python
def render_feedback(self, screen, guess, correct, fonts):
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
```

#### 4.2 Selection Indicators
```python
def _draw_selection_indicator(self, screen, x, y, indicator_type):
    """Draw visual indicator around fraction"""
    color = {
        "selected": ORANGE,
        "correct": GREEN,
        "incorrect": RED
    }.get(indicator_type, BLACK)

    rect = pygame.Rect(x-5, y-5, self.FRAC_WIDTH+10, self.FRAC_HEIGHT+10)
    pygame.draw.rect(screen, color, rect, 4)

def _draw_result_text(self, screen, fonts, is_correct):
    """Draw result message"""
    if is_correct:
        text = "Correct! ✓"
        color = GREEN
    else:
        text = "Incorrect ✗"
        color = RED

    text_surf = fonts['large'].render(text, True, color)
    screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, 450))
```

## Integration with GameManager

### Modified GameManager Methods
```python
def handle_input(self, event):
    """Handle input events - override in GameManager"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if self.guess_made:
            # Check next button
            if self.next_button_rect.collidepoint(event.pos):
                self.next_question()
        else:
            # Let current exercise handle the click
            guess = self.current_exercise.handle_click(event.pos)
            if guess is not None:
                self.make_guess(guess)

def render(self):
    """Render current exercise"""
    self.current_exercise.render_question(self.screen, self.fonts)
    if self.guess_made:
        self.current_exercise.render_feedback(self.screen, self.last_guess,
                                            self.correct_answer, self.fonts)
    self._render_next_button()
```

## Testing Plan

### Unit Tests
1. **Question Generation**
   - Test that different fractions are generated
   - Test that questions alternate between "larger" and "smaller"
   - Test that correct answers are calculated properly

2. **Validation**
   - Test correct selections return (True, 1.0)
   - Test incorrect selections return (False, 0.0)
   - Test invalid inputs

3. **Rendering**
   - Test that fractions are drawn in correct positions
   - Test hover effects work
   - Test feedback indicators appear correctly

### Integration Tests
1. **Full Exercise Flow**
   - Generate question → render → handle click → validate → show feedback
   - Test with GameManager integration

2. **Edge Cases**
   - Very close fractions (1/10 vs 1/11)
   - Fractions with common denominators
   - Very different magnitudes (1/12 vs 11/12)

### Manual Testing Checklist
- [ ] Both "larger" and "smaller" questions work
- [ ] Clicking correct fraction shows green feedback
- [ ] Clicking wrong fraction shows red feedback
- [ ] Next button appears after answer
- [ ] Progress logging works correctly
- [ ] Visual representations are clear and accurate

## Edge Cases and Error Handling

### Edge Cases
1. **Equal Fractions**: Ensure different fractions are always generated
2. **Very Close Values**: 7/8 vs 15/16 (both ≈0.875)
3. **Simple vs Complex**: 1/2 vs 3/7
4. **Common Denominators**: 1/4 vs 3/4 vs 1/2

### Error Handling
1. **Invalid Clicks**: Clicks outside fraction areas should be ignored
2. **Rendering Errors**: Handle cases where pygame surfaces are invalid
3. **Font Loading**: Graceful fallback if fonts aren't available

## Performance Considerations

### Optimization Strategies
1. **Pre-calculate Visuals**: Cache pie chart calculations
2. **Limit Re-renders**: Only redraw when necessary
3. **Font Reuse**: Cache rendered text surfaces

### Memory Management
1. **Surface Reuse**: Reuse pygame surfaces where possible
2. **Cleanup**: Ensure no memory leaks in exercise switching

## Future Enhancements

### Difficulty Levels
- **Easy**: Simple fractions (halves, thirds, quarters)
- **Medium**: Mixed denominators, close values
- **Hard**: Very close fractions, larger numbers

### Alternative Visualizations
- **Bar Charts**: Horizontal bars showing relative sizes
- **Number Line**: Position both fractions on 0-1 line
- **Grid Representation**: Show as portions of a grid

### Additional Features
- **Hints**: Show decimal equivalents
- **Explanations**: Explain why one fraction is larger
- **Multiple Choice**: More than 2 options for advanced levels

## Success Metrics

### Educational Impact
- Students can correctly compare fractions 80%+ of the time
- Improved performance on fraction comparison problems
- Reduced time to answer comparison questions

### Technical Metrics
- Smooth 60 FPS rendering
- <100ms response time for input
- No crashes or visual glitches
- Proper progress logging

## Implementation Timeline

### Day 1: Core Structure (4 hours)
- Create class skeleton
- Implement question generation
- Basic validation logic

### Day 2: Rendering (4 hours)
- Implement pie chart visualization
- Add text rendering
- Basic input handling

### Day 3: Feedback & Polish (4 hours)
- Implement feedback rendering
- Add hover effects
- Integration testing

### Day 4: Testing & Refinement (4 hours)
- Unit tests
- Bug fixes
- Performance optimization

## Dependencies

### Required Libraries
- pygame (for rendering)
- fractions.Fraction (for exact comparisons)
- math (for pie chart calculations)

### Integration Points
- GameManager.render() - for display
- GameManager.handle_input() - for mouse clicks
- ProgressLogger - for data persistence

This implementation will provide a solid foundation for teaching fraction comparison skills while maintaining the extensible architecture established in TASK1.</content>
<parameter name="filePath">c:\Users\gulya\src\fractions\learn-fractions\TASK2-FractionComparison.md