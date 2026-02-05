    # Learn Fractions

    

    An interactive educational tool to help learn fractions and decimals by estimating their positions on a number line.

    ## Intended Goal

    The goal of this project is to provide an engaging way to practice understanding fractions and decimals. Users are presented with a number line and asked to click where they think a given fraction or decimal falls. The tool provides immediate visual feedback, tracks thinking time and accuracy, and logs progress data for analysis over time. This helps build intuition for numerical values between 0 and 1.

    ## Features

    - **Interactive Number Line**: Displays a number line from 0 to 1 with ticks every 0.1 for precise estimation.
    - **Random Questions**: Generates random fractions (e.g., 1/4, 3/5) or decimals (e.g., 0.25, 0.67) for variety.
    - **Visual Feedback**: After clicking, shows your guess (blue dot) and the correct answer (red dot) with a legend.
    - **Progress Logging**: Records each attempt with:
      - Timestamp
      - Thinking time (seconds)
      - Distance from correct answer
      - Question (fraction/decimal string)
      - Correct answer (numerical value)
      - Full question text
    - **Multiple Rounds**: "Next Question" button to continue practicing without restarting.
    - **Console Output**: Prints guess, correct value, thinking time, and distance to the terminal.

    ## Development Environment Setup

    ### Virtual Environment Setup
    It is highly recommended to use a virtual environment to manage dependencies. This project includes a `.venv` directory.

    **Activate the virtual environment before running the game or tests:**

    On Windows:
    ```bash
    .venv\Scripts\activate
    ```

    On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

    **To deactivate the virtual environment:**
    ```bash
    deactivate
    ```

    ### Installing Dependencies
    After activating the virtual environment, install required packages:
    ```bash
    pip install -r requirements.txt
    ```

    ## How to Run

    ### Matplotlib Version
    1. **Activate the virtual environment** (see above)
    2. Ensure Python and required libraries are installed (matplotlib, tkinter).
    3. Run the script:
    ```bash
    python learn_fractions.py
    ```
    4. The plot window will appear with a question.
    5. Click on the number line to make your guess.
    6. Review the feedback and click "Next Question" to continue.
    7. Close the window when done.

    ### Pygame Version
    1. **Activate the virtual environment** (see above)
    2. Ensure Python and required libraries are installed (pygame).
    3. Run the script:
    ```bash
    python learn_fractions_pygame.py
    ```
    4. The Pygame window will appear with a question.
    5. Click on the number line to make your guess.
    6. Review the feedback and click "Next Question" to continue.
    7. Close the window when done.

    ### SOLID Refactored Edition
    This is the main Pygame version with improved architecture:

    1. **Activate the virtual environment** (see above)
    2. Run the script:
    ```bash
    python learn_pygame_solid.py
    ```
    3. The game window will appear with various fraction exercises.
    4. Follow on-screen instructions for each exercise type.
    5. Click "Next" button to proceed to the next question.

    ## Running Tests
    1. **Activate the virtual environment** (see above)
    2. Run specific test files:
    ```bash
    python test_double_number_line.py
    ```

    ## Requirements

    - Python 3.8 or higher
    - matplotlib (for original version)
    - tkinter (usually included with Python, for original version)
    - pygame (for Pygame version)

    All dependencies are listed in `requirements.txt`.

    ## Data Logging

    All attempts are logged to `progress.log` (matplotlib version) or `progress_pygame.log` (Pygame version) in CSV-like format. Analyze this file to track improvement in speed and accuracy over time.

    Example log entry:
    ```
    2026-01-24T13:52:02.131224, 3.30, 0.007, 1/4, 0.25, Click where you think 1/4 is
    ```

    ## Future Enhancements

    - Scoring system
    - Difficulty levels
    - Statistics dashboard
    - Export progress reports