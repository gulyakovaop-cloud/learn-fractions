# TASK6: Double Number Line Exercise Implementation Plan


# Double Number Line Exercise - Implementation Plan

Based on my analysis of the existing codebase and your requirements, I've created a comprehensive plan for implementing a Double Number Line exercise. This feature will help students understand percentages and proportional relationships through visual parallel number lines.

## Overview and Educational Goals

### Core Concept
A double number line is a visual representation of proportional relationships, featuring two parallel lines:
- **Quantity Line**: Shows actual numbers (e.g., 0 to 120)
- **Percentage Line**: Shows percentages (0% to 100%)

Key points align vertically, allowing students to see equivalences like "60 is 50% of 120."

### Educational Objectives
1. **Percentage Understanding**: Connect percentages to their numerical equivalents
2. **Proportional Reasoning**: Develop intuition for proportional relationships
3. **Problem Solving**: Solve percentage problems visually
4. **Real-World Applications**: Apply to discounts, tips, taxes, and scaling

## Functional Requirements

### Core Question Types
1. **Find the Value**: "What is 25% of 120?" (Given percentage, find number). Note: Make sure, we should show 120 on the matching place to 100% is such case. 
2. **Find the Percentage**: "60 is what percent of 120?" (Given number, find percentage)
Note: MAke sure same thing, when max number - 120, we should show it near 100% marker.
3. **Find the Whole**: "25% is 30, what is 100%?" (Given part and percentage, find whole)
Note: when we asking about 25% for 30 - we should draw 30 on the matching place where is 25%, and ? on new 100% and provide 4 options to choose.

4. **Missing Value**: "If 60 is 50%, what is 75%?" (Complete the proportion)
Note: Same as previous, 60 should have corresponding place near 50% , 75% with corresponding ? and nothing at the left from it, only 100% and number near it.

Summary note: In most cases I would prefer keep picture as noted above, but ask number as option to choose from 4 items. 

### Interactive Features
- Click/drag points on either line to set values
- Visual feedback showing vertical alignment between lines
- Step-by-step solution display
- Multiple difficulty levels

### Visual Components
- Two parallel horizontal lines with appropriate scales
- Tick marks and labels on both lines
- Movable markers for user answers
- Vertical connecting lines for matched points
- Color-coded feedback (green for correct, blue for user answer, red for correct answer)

## Technical Requirements

### Class Structure
```python
class DoubleNumberLineExercise(Exercise):
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.line_top_y = 150    # Percentage line
        self.line_bottom_y = 300 # Quantity line
        self.line_start_x = 100
        self.line_end_x = 700
        self.quantity_max = 100  # Default, varies by difficulty
        self.current_problem = None
```

### Problem Generation
```python
def generate_question(self):
    problem_type = random.choice(["find_value", "find_percent", "find_whole", "missing_value"])
    
    if problem_type == "find_value":
        # "What is X% of Y?"
        whole = self._generate_whole_number()
        percent = self._generate_percentage()
        part = whole * percent / 100
        question = f"What is {percent}% of {whole}?"
        answer = part
```

### Difficulty Levels
- **Easy**: Whole numbers, simple percentages (25%, 50%, 75%, 100%)
- **Medium**: Whole numbers, any percentage, multiples of 5
- **Hard**: Decimals, fractions, complex percentages

### Validation Logic
```python
def validate_guess(self, guess_value, guess_type):
    # guess_type: "quantity" or "percent"
    # Calculate accuracy based on proximity
    # Provide partial credit for close answers
```

## Design Decisions

### UI Layout
```
┌─────────────────────────────────────────────────────────────┐
│         What is 25% of 120? (Click on the lines)            │
│                                                             │
│  Percentage Line:                                           │
│  0%─────25%─────50%─────75%─────100%                        │
│    │     │      │       │       │                           │
│    │     └──────┼───────┼───────┼─────► User clicked here   │
│    │            │       │       │                           │
│  Quantity Line: │       │       │                           │
│  0──────30─────60──────90──────120                          │
│                                                             │
│  Your answer: 30 (25% of 120)                              │
│  Correct answer will be shown in red                        │
└─────────────────────────────────────────────────────────────┘
```

### Coordinate System
- Both lines share the same horizontal scale
- Vertical alignment through linear mapping: `quantity = (percent/100) * max_quantity`
- Mouse position mapping to both line values

### Interaction Model
1. **Click to Set**: Single click sets value on either line
2. **Drag to Adjust**: Click and drag to fine-tune
3. **Auto-align**: Setting value on one line shows corresponding value on other line

## Implementation Plan

### Phase 1: Core Infrastructure (2-3 days)
1. Create `DoubleNumberLineExercise` class inheriting from `Exercise`
2. Implement problem generation for all question types
3. Add basic line drawing and coordinate mapping
4. Unit tests for problem generation and validation

### Phase 2: Visual Rendering (2 days)
1. Implement parallel line drawing with tick marks
2. Add movable marker rendering (circles/dots)
3. Create vertical connecting line visualization
4. Handle different difficulty level visual scaling

### Phase 3: Interaction Handling (2 days)
1. Implement mouse click detection for both lines
2. Add drag-and-drop functionality for markers
3. Create real-time value display during interaction
4. Add input validation and boundary checking

### Phase 4: Feedback and Polish (1-2 days)
1. Implement visual feedback (correct vs user answer)
2. Add step-by-step solution display
3. Integrate with existing `GameManager` and logging
4. Performance optimization and bug fixes

## Recommended Additional Features

### 1. Real-World Context Problems
- **Shopping Discounts**: "Item costs $80, 25% off, what's the sale price?"
- **Restaurant Tips**: "Bill is $60, 15% tip, what's total?"
- **Tax Calculations**: "Price is $90, plus 8% tax, what's final cost?"

### 2. Progressive Difficulty System
- Level 1: Simple whole numbers (25%, 50%, 75%, 100%)
- Level 2: Any percentage with whole numbers
- Level 3: Decimals and fractions (12.5%, 33.3%)
- Level 4: Word problems with real-world context

### 3. Enhanced Visualization
- **Animation**: Show proportional scaling between lines
- **Multiple Markers**: Compare different percentages on same base
- **Custom Ranges**: Allow teacher to set custom number ranges
- **Grid Overlay**: Add background grid for better estimation

### 4. Learning Support Features
- **Step-by-Step Hints**: Show calculation process
- **Common Mistakes**: Highlight frequent errors
- **Visual Aids**: Highlight quarter, half, three-quarter points
- **Practice Mode**: Unlimited practice with immediate feedback

### 5. Analytics Integration
- **Common Error Patterns**: Track which percentage values cause most mistakes
- **Time Analysis**: Measure solving time vs. accuracy
- **Progress Tracking**: Monitor improvement across difficulty levels
- **Personalized Recommendations**: Suggest practice based on weak areas

## Integration with Existing System

### File Structure
```
exercises/
├── double_number_line_exercise.py
└── __init__.py (update to include new exercise)
```

### Game Manager Integration
```python
# In learn_pygame_solid.py
exercises = [
    NumberLineExercise(),
    DoubleNumberLineExercise(difficulty="easy"),
    DoubleNumberLineExercise(difficulty="medium"),
    # ... other exercises
]
```

### Progress Logging
- New exercise type: "double_number_line"
- Track: problem type, difficulty, accuracy, solving time
- Integration with existing reporting system

## Testing Strategy

### Unit Tests
- Problem generation produces valid questions
- Coordinate mapping works correctly
- Validation logic handles edge cases
- Difficulty levels adjust parameters appropriately

### Integration Tests
- Exercise integrates with `GameManager`
- UI rendering doesn't conflict with other exercises
- Mouse interaction works with existing event system
- Progress logging captures all relevant data

### User Acceptance Tests
- Visual clarity of parallel lines
- Intuitive click/drag interaction
- Clear feedback on correct/incorrect answers
- Appropriate difficulty progression

## Future Enhancements

### Advanced Features
1. **Triple Number Line**: Add fraction line for complete proportional representation
2. **Dynamic Scaling**: Lines that adjust based on problem requirements
3. **Custom Problems**: Teacher/student created problems
4. **Multi-step Problems**: Combine with other exercise types

### Educational Extensions
1. **Ratio Problems**: Extend to ratio and rate problems
2. **Scale Drawings**: Connect to map scales and scale factors
3. **Similarity**: Introduce geometric similarity concepts
4. **Unit Conversion**: Apply to measurement conversions

## Next Steps

1. **Review this plan** - Let me know if you'd like any adjustments
2. **Switch to ACT Mode** - I'll implement the plan by:
   - Creating the TASK6-DoubleNumberLine.md file with this detailed plan
   - Implementing the `DoubleNumberLineExercise` class
   - Integrating it into the existing game system

What are your thoughts on this plan? Would you like me to elaborate on any specific aspect or adjust the feature recommendations?