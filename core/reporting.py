import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def generate_report(log_file: str, output_dir: str):
    """
    Generates a report from the progress log file.

    Args:
        log_file (str): The path to the log file.
        output_dir (str): The directory to save the report to.
    """
    log_path = Path(log_file)
    output_path = Path(output_dir)

    if not log_path.exists():
        print(f"Error: Log file not found at {log_path}")
        return

    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(
            log_path,
            header=None,
            names=[
                "timestamp",
                "exercise_type",
                "thinking_time",
                "distance",
                "accuracy",
                "question",
                "correct",
                "guess",
            ],
            parse_dates=["timestamp"],
        )
    except Exception as e:
        print(f"Error reading log file: {e}")
        return

    # Basic data cleaning
    data["thinking_time"] = pd.to_numeric(data["thinking_time"], errors="coerce")
    data["distance"] = pd.to_numeric(data["distance"], errors="coerce")
    data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")
    data.dropna(subset=["thinking_time", "distance", "accuracy"], inplace=True)
    
    # Strip whitespace from string columns
    string_columns = ["exercise_type", "question", "correct", "guess"]
    for col in string_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).str.strip()
    
    # Determine correctness based on accuracy (1.0 = correct)
    data['is_correct'] = data['accuracy'] == 1.0

    # Calculate key metrics for dashboard
    total_attempts = len(data)
    correct_attempts = data['is_correct'].sum()
    overall_accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
    avg_thinking_time = data['thinking_time'].mean()
    
    # Calculate daily progress
    daily_stats = data.groupby(data['timestamp'].dt.date).agg({
        'is_correct': ['count', 'sum'],
        'thinking_time': 'mean'
    })
    daily_stats.columns = ['total', 'correct', 'avg_time']
    daily_stats['accuracy'] = (daily_stats['correct'] / daily_stats['total'] * 100)
    
    # Find best day
    if not daily_stats.empty:
        best_day = daily_stats['accuracy'].idxmax()
        best_accuracy = daily_stats.loc[best_day, 'accuracy']
        fastest_day = daily_stats['avg_time'].idxmin()
        fastest_time = daily_stats.loc[fastest_day, 'avg_time']
    else:
        best_day = fastest_day = None
        best_accuracy = fastest_time = 0

    report_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Math Progress Report 🎯</title>
    <style>
        body {{ font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif; margin: 2em; background-color: #f9f9f9; }}
        h1 {{ color: #FF6B6B; text-align: center; font-size: 2.5em; }}
        h2 {{ color: #4ECDC4; border-bottom: 3px solid #FFD166; padding-bottom: 0.3em; }}
        .dashboard {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .metric {{ 
            text-align: center; 
            padding: 15px; 
            border-radius: 10px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }}
        .metric-value {{ 
            font-size: 2.5em; 
            font-weight: bold; 
            margin: 10px 0;
            color: #2C3E50;
        }}
        .metric-label {{ 
            font-size: 1.1em; 
            color: #7F8C8D;
        }}
        .emoji {{ font-size: 2em; margin-bottom: 10px; }}
        img {{ max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; border-radius: 10px; overflow: hidden; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4ECDC4; color: white; }}
        .good {{ color: #2ECC71; }}
        .ok {{ color: #F39C12; }}
        .needs-improvement {{ color: #E74C3C; }}
        .date {{ font-size: 0.9em; color: #95A5A6; }}
    </style>
</head>
<body>
    <h1>🎯 Math Progress Report 🎯</h1>
    <p class="date">Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>📊 Analyzed <strong>{total_attempts}</strong> math problems from your practice sessions!</p>
    
    <div class="dashboard">
        <div class="metric">
            <div class="emoji">🎯</div>
            <div class="metric-value">{overall_accuracy:.1f}%</div>
            <div class="metric-label">Overall Accuracy</div>
        </div>
        <div class="metric">
            <div class="emoji">⏱️</div>
            <div class="metric-value">{avg_thinking_time:.1f}s</div>
            <div class="metric-label">Average Time per Problem</div>
        </div>
        <div class="metric">
            <div class="emoji">⭐</div>
            <div class="metric-value">{correct_attempts}</div>
            <div class="metric-label">Problems Solved Correctly</div>
        </div>
        <div class="metric">
            <div class="emoji">📅</div>
            <div class="metric-value">{len(daily_stats)}</div>
            <div class="metric-label">Days Practiced</div>
        </div>
    </div>
    
    <div style="background: #FFEAA7; padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #D35400;">🏆 Best Day: {best_day if best_day else 'N/A'}</h3>
        <p>Your best accuracy was <strong>{best_accuracy:.1f}%</strong> on {best_day if best_day else 'no day yet'}! 🎉</p>
        <p>Your fastest average time was <strong>{fastest_time:.1f} seconds</strong> on {fastest_day if fastest_day else 'no day yet'}! ⚡</p>
    </div>
"""


    # Time-based analysis
    for timescale, timescale_name in [("D", "Daily"), ("W", "Weekly"), ("ME", "Monthly")]:
        report_html += f"<h2>{timescale_name} Progress</h2>\n"
        
        grouped = data.groupby(pd.Grouper(key='timestamp', freq=timescale))
        
        if grouped.ngroups == 0:
            report_html += "<p>No data for this period.</p>\n"
            continue
        
        avg_accuracy = grouped['accuracy'].mean() * 100  # Convert to percentage
        avg_time = grouped['thinking_time'].mean()
        
        # Calculate accuracy rating and color
        def get_accuracy_rating(acc_percent):
            if acc_percent >= 90:
                return 'EXC', '#4CAF50'  # Green for excellent
            elif acc_percent >= 70:
                return 'GOOD', '#FFC107'  # Yellow for good
            else:
                return 'PRAC', '#F44336'  # Red for needs practice
        
        def get_speed_rating(time_sec):
            if time_sec < 5:
                return 'FAST', '#2196F3'  # Blue for fast
            elif time_sec < 15:
                return 'MED', '#3F51B5'  # Indigo for medium
            else:
                return 'SLOW', '#9C27B0'  # Purple for slow

        # Create plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        # Plot accuracy as bars
        bars = ax1.bar(avg_accuracy.index, avg_accuracy.values, alpha=0.7, label='Accuracy %', 
                      color=[get_accuracy_rating(val)[1] for val in avg_accuracy.values])
        
        # Plot time as line
        line = ax2.plot(avg_time.index, avg_time.values, 'o-', linewidth=3, markersize=8, 
                       label='Thinking Time (s)', color='#FF5722')
        
        # Add emoji annotations on bars
        for i, (idx, acc_val) in enumerate(avg_accuracy.items()):
            rating, _ = get_accuracy_rating(acc_val)
            ax1.text(idx, acc_val + 1, rating, ha='center', fontsize=10, fontweight='bold')
        
        # Add emoji annotations on line points
        for i, (idx, time_val) in enumerate(avg_time.items()):
            rating, _ = get_speed_rating(time_val)
            ax2.text(idx, time_val + 0.5, rating, ha='center', fontsize=10, fontweight='bold')

        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Accuracy %', fontsize=12, color='#333')
        ax2.set_ylabel('Thinking Time (seconds)', fontsize=12, color='#FF5722')
        ax1.set_title(f'{timescale_name} Progress Chart', fontsize=16, fontweight='bold', pad=20)
        
        # Add grid and legend
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 110)  # Leave room for emojis above 100%
        
        # Add legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        fig.tight_layout()
        
        chart_path = output_path / f"{timescale_name.lower()}_progress.png"
        plt.savefig(chart_path)
        plt.close(fig)
        
        report_html += f'<img src="{chart_path.name}" alt="{timescale_name} Progress" />\n'
        
        # Breakdown by exercise type - simplified for kids
        report_html += f"<h3>{timescale_name} Exercise Summary 📝</h3>\n"
        
        exercise_grouped = data.groupby([pd.Grouper(key='timestamp', freq=timescale), 'exercise_type'])
        
        total_completed = exercise_grouped.size().unstack(fill_value=0)
        correctly_completed = exercise_grouped['is_correct'].sum().unstack(fill_value=0)
        avg_time_exercise = exercise_grouped['thinking_time'].mean().unstack(fill_value=np.nan)

        if not total_completed.empty:
            report_html += '''
            <table>
            <thead>
            <tr>
                <th>Date</th>
                <th>Exercise Type</th>
                <th>Attempts</th>
                <th>Correct ✅</th>
                <th>Accuracy</th>
                <th>Avg Time</th>
                <th>Rating</th>
            </tr>
            </thead>
            <tbody>
            '''
            for period, period_data in total_completed.iterrows():
                for exercise_type, total in period_data.items():
                    if total > 0:
                        correct = correctly_completed.loc[period, exercise_type] if period in correctly_completed.index and exercise_type in correctly_completed.columns else 0
                        avg_t = avg_time_exercise.loc[period, exercise_type] if period in avg_time_exercise.index and exercise_type in avg_time_exercise.columns else np.nan
                        accuracy_pct = (correct / total * 100) if total > 0 else 0
                        
                        # Determine rating emoji
                        if accuracy_pct >= 90:
                            rating = '😊 Excellent!'
                            rating_class = 'good'
                        elif accuracy_pct >= 70:
                            rating = '😐 Good job!'
                            rating_class = 'ok'
                        else:
                            rating = '😞 Keep practicing!'
                            rating_class = 'needs-improvement'
                        
                        report_html += f'''
                        <tr>
                            <td>{period.strftime("%Y-%m-%d")}</td>
                            <td><strong>{exercise_type.replace('_', ' ').title()}</strong></td>
                            <td>{total}</td>
                            <td>{correct}</td>
                            <td>{accuracy_pct:.1f}%</td>
                            <td>{avg_t:.1f}s</td>
                            <td class="{rating_class}">{rating}</td>
                        </tr>
                        '''
            report_html += '</tbody>\n</table>\n'
        else:
            report_html += '<p>No exercise data for this period.</p>\n'

    # Challenging Problems - reframed positively
    report_html += "<h2>🎯 Challenging Problems to Practice</h2>\n"
    incorrect_tasks = data[data['is_correct'] == False]
    if not incorrect_tasks.empty:
        top_5_incorrect = incorrect_tasks['question'].value_counts().nlargest(5)
        report_html += '''
        <div style="background: #FFF3CD; padding: 20px; border-radius: 10px; border-left: 5px solid #FFC107;">
            <p>These problems were a bit tricky. Try them again to improve! 💪</p>
            <table>
            <thead>
            <tr>
                <th>Problem</th>
                <th>Times Practiced</th>
                <th>Suggestion</th>
            </tr>
            </thead>
            <tbody>
        '''
        for question, count in top_5_incorrect.items():
            # Add encouraging suggestions based on count
            if count >= 3:
                suggestion = "⭐ Keep working on this!"
            elif count == 2:
                suggestion = "✨ Almost got it!"
            else:
                suggestion = "💡 Try one more time!"
            
            # Shorten long questions for display
            display_question = question
            if len(display_question) > 50:
                display_question = display_question[:47] + "..."
                
            report_html += f'''
            <tr>
                <td><strong>{display_question}</strong></td>
                <td>{count}</td>
                <td>{suggestion}</td>
            </tr>
            '''
        report_html += '''
            </tbody>
            </table>
            <p style="margin-top: 15px; font-style: italic;">Remember: Practice makes perfect! 🏆</p>
        </div>
        '''
    else:
        report_html += '''
        <div style="background: #D4EDDA; padding: 20px; border-radius: 10px; border-left: 5px solid #28A745;">
            <h3 style="color: #155724; margin-top: 0;">🎉 Amazing! 🎉</h3>
            <p>You got <strong>all problems correct</strong> in this session! You're a math superstar! 🌟</p>
            <p>Keep up the great work! 💫</p>
        </div>
        '''


    # Add footer with encouragement
    report_html += '''
    <div style="margin-top: 40px; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
         border-radius: 15px; color: white; text-align: center;">
        <h2 style="color: white; margin-top: 0;">🌟 You're Doing Great! 🌟</h2>
        <p style="font-size: 1.2em;">Every problem you solve makes you better at math!</p>
        <p>Come back tomorrow for more practice and watch your scores improve! 📈</p>
        <div style="font-size: 2em; margin: 15px 0;">
            🏆 🎯 ⭐ 💪 🌈
        </div>
    </div>
    </body>
    </html>
    '''

    # Save the report
    report_file_path = output_path / "report.html"
    with open(report_file_path, "w", encoding='utf-8') as f:
        f.write(report_html)

    print(f"Report successfully generated at {report_file_path.resolve()}")

if __name__ == '__main__':
    # This allows running the reporting script directly for testing
    # In the final implementation, this will be called from main.py
    generate_report('learn-fractions/progress_pygame.log', 'learn-fractions/reports')