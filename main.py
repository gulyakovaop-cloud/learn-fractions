import argparse
from pathlib import Path
from core.reporting import generate_report

def main():
    """
    Main entry point for the application.
    Handles command-line arguments for different modes (game vs. reporting).
    """
    parser = argparse.ArgumentParser(description="Learn Fractions Application")
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate a progress report from the log files.'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default='progress_pygame.log',
        help='Specify the log file to process for the report.'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='reports',
        help='Specify the directory to save the report files.'
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent
    
    if args.report:
        log_file_path = project_root / args.log_file
        output_dir_path = project_root / args.output_dir
        print(f"Generating report from {log_file_path} into {output_dir_path}...")
        generate_report(str(log_file_path), str(output_dir_path))
    else:
        # TODO: Add the logic to run the game here
        print("Starting the game... (Not implemented yet)")
        # For now, you can run the game directly using:
        # python learn-fractions/learn_fractions_pygame.py

if __name__ == '__main__':
    main()
