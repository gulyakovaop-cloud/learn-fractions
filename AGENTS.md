# Development Agent Guidelines

## Development Environment Setup

### Virtual Environment Activation
**CRITICAL:** Always activate the virtual environment before running the game or tests!

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Dependency Installation
```bash
# After activating virtual environment
pip install -r requirements.txt
```

## Project Structure

```
learn-fractions/
├── .venv/                  # Virtual environment (DO NOT DELETE)
├── core/                   # Core application modules
│   ├── exercise.py         # Exercise abstract base class
│   ├── game_manager.py     # Game coordination and state management
│   ├── progress_logger.py  # Progress tracking and logging
│   └── reporting.py        # Report generation
├── exercises/              # Exercise implementations
│   ├── number_line_exercise.py
│   ├── fraction_comparison_exercise.py
│   ├── advanced_fraction_comparison_exercise.py
│   ├── multiplication_exercise.py
│   ├── multiplication_exercise_num.py
│   └── double_number_line_exercise.py
├── reports/                # Generated reports
├── main.py                 # CLI entry point
├── learn_pygame_solid.py   # Main Pygame application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Running Applications

### Main Pygame Application
```bash
python learn_pygame_solid.py
```

### Reporting System
```bash
python main.py --report
python main.py --report --log-file progress_pygame.log --output-dir reports
```

### Testing
```bash
# Test specific exercise
python test_double_number_line.py

# Run game with specific exercises
python learn_pygame_solid.py
```

## Development Workflow

### Adding New Exercises
1. Create new exercise class in `exercises/` directory
2. Inherit from `Exercise` abstract base class
3. Implement required methods:
   - `generate_question()` - returns (question_text, correct_answer)
   - `validate_guess(guess)` - returns (is_correct, accuracy_score)
   - `get_type()` - returns exercise type string
   - Optional: `render_question()`, `render_feedback()`, `handle_click()`
4. Add import to `exercises/__init__.py`
5. Add instance to exercise list in `learn_pygame_solid.py`

### Exercise Implementation Guidelines
- Use consistent color scheme (BLACK, WHITE, RED, BLUE, GREEN, GRAY)
- Follow existing coordinate system (800x600 screen)
- Use fonts dictionary from GameManager
- Implement proper mouse interaction via `handle_click()` method
- Provide clear visual feedback

### Testing Guidelines
- Create test files with descriptive names (test_*.py)
- Test all difficulty levels
- Verify question generation randomness
- Test coordinate mapping accuracy
- Validate scoring logic

## Common Issues and Solutions

### Virtual Environment Not Activated
**Symptom:** Import errors or missing packages
**Solution:** Always activate `.venv` before running any Python commands

### Pygame Window Doesn't Open
**Symptom:** Script runs but no window appears
**Solution:** Check pygame installation in virtual environment, ensure display is available

### Import Errors
**Symptom:** "ModuleNotFoundError" when running scripts
**Solution:** Ensure working directory is project root, virtual environment is activated

### Log File Permission Errors
**Symptom:** Cannot write to progress logs
**Solution:** Check file permissions, ensure not running as read-only

## Performance Considerations
- Limit grid sizes in visual exercises (max 8x8)
- Avoid complex calculations in render loops
- Use pygame.Rect for collision detection
- Cache font surfaces when possible

## Code Style
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings to classes and methods
- Use descriptive variable names
- Keep methods focused and under 50 lines

## Version Control Notes
- The `.venv` directory is excluded in `.gitignore`
- Log files are tracked but can be excluded if needed
- Test files should be committed
- Report templates should be committed

## Quick Reference Commands

### Environment Setup
```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Development
```bash
# Run main application
python learn_pygame_solid.py

# Run specific test
python test_double_number_line.py

# Generate reports
python main.py --report
```

### Troubleshooting
```bash
# Check virtual environment activation
python -c "import sys; print(sys.prefix)"

# List installed packages
pip list

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Emergency Recovery
If the virtual environment becomes corrupted:
1. Delete `.venv` directory
2. Recreate: `python -m venv .venv`
3. Activate and reinstall: `pip install -r requirements.txt`

**Warning:** Do not delete `.venv` unless absolutely necessary, as it contains all project dependencies.