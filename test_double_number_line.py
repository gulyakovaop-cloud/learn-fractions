#!/usr/bin/env python3
"""Test script for DoubleNumberLineExercise class."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exercises.double_number_line_exercise import DoubleNumberLineExercise

def test_exercise_creation():
    """Test that exercise can be created and generates questions."""
    print("Testing DoubleNumberLineExercise...")
    
    # Test creation with different difficulty levels
    for difficulty in ["easy", "medium", "hard"]:
        print(f"\nTesting {difficulty} difficulty:")
        try:
            exercise = DoubleNumberLineExercise(difficulty=difficulty)
            
            # Test question generation
            question, answer = exercise.generate_question()
            print(f"  Question: {question}")
            print(f"  Answer: {answer}")
            print(f"  Problem type: {exercise.current_problem.get('type', 'unknown')}")
            
            # Test coordinate mapping
            test_percent = 50.0
            x = exercise._map_percent_to_x(test_percent)
            recovered_percent = exercise._map_x_to_percent(x)
            print(f"  Coordinate mapping test: {test_percent}% -> x={x} -> {recovered_percent:.1f}%")
            
            # Test validation
            test_guess = answer * 0.9  # 90% of correct answer
            is_correct, accuracy = exercise.validate_guess(test_guess)
            print(f"  Validation test: guess={test_guess:.1f}, correct={is_correct}, accuracy={accuracy:.2f}")
            
            print(f"  ✓ {difficulty} test passed")
            
        except Exception as e:
            print(f"  ✗ {difficulty} test failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*50)
    print("Testing complete!")

def test_problem_types():
    """Test all problem types."""
    print("\nTesting all problem types:")
    exercise = DoubleNumberLineExercise(difficulty="easy")
    
    problem_types = ["find_value", "find_percent", "find_whole", "missing_value"]
    type_counts = {pt: 0 for pt in problem_types}
    
    # Generate multiple questions to see all types
    for _ in range(20):
        exercise.generate_question()
        problem_type = exercise.current_problem.get("type")
        if problem_type in type_counts:
            type_counts[problem_type] += 1
    
    print("Problem type distribution over 20 questions:")
    for pt, count in type_counts.items():
        print(f"  {pt}: {count}")
    
    return all(count > 0 for count in type_counts.values())

if __name__ == "__main__":
    print("="*50)
    print("Double Number Line Exercise Test")
    print("="*50)
    
    test_exercise_creation()
    
    if test_problem_types():
        print("\n✓ All problem types were generated at least once")
    else:
        print("\n⚠ Some problem types were not generated")
    
    print("\n" + "="*50)
    print("All tests completed!")
    print("="*50)