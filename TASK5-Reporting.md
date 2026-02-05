# TASK 5: Add a `--report` CLI option

## Objective

Implement a new command-line option, `--report`, to the application. This option will be used to process the existing log files (`progress.log` or `progress_pygame.log`) and generate a report with charts visualizing the user's progress over time.

## Requirements

1.  **CLI Option:**
    *   Add a `--report` flag to one of the main application entry points (e.g., a new `main.py` or an existing one).
    *   When this flag is used, the application should not start the game but instead enter the reporting mode.

2.  **Log Processing:**
    *   The reporting mode should read the data from the relevant log file. The log file is in a CSV-like format:
        `timestamp, thinking_time, distance, label, value, full_question`

3.  **Report Generation:**
    *   The report should be generated as an HTML file or displayed in a new window.
    *   The report should contain charts that visualize the user's progress.

4.  **Charts & Analysis:**
    *   The following charts should be generated for overall progress:
        *   **Progress per Day:** A chart showing the average accuracy (or distance from the correct answer) and average thinking time for each day.
        *   **Progress per Week:** A chart showing the average accuracy and average thinking time for each week.
        *   **Progress per Month:** A chart showing the average accuracy and average thinking time for each month.
    *   **Breakdown by Exercise Type:** For each timescale (Day, Week, Month), provide a detailed breakdown for each exercise type, including:
        *   Number of tasks completed (total attempts).
        *   Number of tasks completed correctly.
        *   Minimum thinking time.
        *   90th percentile thinking time.
        *   Average thinking time.
    *   **Top 5 Incorrect Tasks:**
        *   Generate a list of the top 5 specific questions that are most frequently answered incorrectly. This will help identify areas for improvement or potential issues with the questions themselves.

## Implementation Details

*   **Libraries:** `pandas` would be a good choice for data manipulation and aggregation. `matplotlib` or a library like `plotly` could be used for generating the charts.
*   **File Structure:** The reporting logic should be placed in a new module, for example, `core/reporting.py`.
*   **Entry Point:** A new function in the main script should be created to handle the `--report` option. This function will call the reporting module to generate the report.
