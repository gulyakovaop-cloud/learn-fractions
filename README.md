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

    ## How to Run

    ### Matplotlib Version
    1. Ensure Python and required libraries are installed (matplotlib, tkinter).
    2. Run the script:
    ```
    python learn_fractions.py
    ```
    3. The plot window will appear with a question.
    4. Click on the number line to make your guess.
    5. Review the feedback and click "Next Question" to continue.
    6. Close the window when done.

    ### Pygame Version
    1. Ensure Python and required libraries are installed (pygame).
    2. Run the script:
    ```
    python learn_fractions_pygame.py
    ```
    3. The Pygame window will appear with a question.
    4. Click on the number line to make your guess.
    5. Review the feedback and click "Next Question" to continue.
    6. Close the window when done.

    ## Requirements

    - Python 3.x
    - matplotlib (for original version)
    - tkinter (usually included with Python, for original version)
    - pygame (for Pygame version)

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