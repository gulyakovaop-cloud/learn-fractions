import pygame
import random
import sys
import datetime
from fractions import Fraction

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
LINE_Y = HEIGHT // 2
LINE_START_X = 100
LINE_END_X = WIDTH - 100
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_X = WIDTH - 200
BUTTON_Y = HEIGHT - 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Fractions - Pygame Edition")

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def random_number():
    """Return a number between 0 and 1 as float and display text"""
    if random.choice([True, False]):
        # fraction
        numerator = random.randint(1, 14)
        denominator = random.randint(numerator + 1, 15)
        frac = Fraction(numerator, denominator)
        return float(frac), str(frac)
    else:
        # decimal
        value = round(random.uniform(0.1, 0.9), 2)
        return value, str(value)

def draw_number_line():
    """Draw the number line from 0 to 1"""
    # Main line
    pygame.draw.line(screen, BLACK, (LINE_START_X, LINE_Y), (LINE_END_X, LINE_Y), 3)

    # Tick marks and labels
    for i in range(11):
        x = LINE_START_X + (LINE_END_X - LINE_START_X) * i // 10
        pygame.draw.line(screen, BLACK, (x, LINE_Y - 10), (x, LINE_Y + 10), 2)

        # Label
        label = small_font.render(str(i/10), True, BLACK)
        screen.blit(label, (x - label.get_width()//2, LINE_Y + 15))

def draw_button(text, x, y, width, height, color=GRAY):
    """Draw a button"""
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

    text_surf = font.render(text, True, BLACK)
    text_x = x + (width - text_surf.get_width()) // 2
    text_y = y + (height - text_surf.get_height()) // 2
    screen.blit(text_surf, (text_x, text_y))

def get_click_position():
    """Convert mouse x position to value between 0 and 1"""
    mouse_x = pygame.mouse.get_pos()[0]
    if mouse_x < LINE_START_X:
        return 0.0
    elif mouse_x > LINE_END_X:
        return 1.0
    else:
        return (mouse_x - LINE_START_X) / (LINE_END_X - LINE_START_X)

def main():
    global value, label, start_time, guess_made, show_result

    # Initialize game state
    value, label = random_number()
    start_time = datetime.datetime.now()
    guess_made = False
    show_result = False
    guess = None
    thinking_time = None
    distance = None

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw number line
        draw_number_line()

        # Draw question
        question = f"Click where you think {label} is"
        question_surf = font.render(question, True, BLACK)
        screen.blit(question_surf, (WIDTH//2 - question_surf.get_width()//2, 50))

        # Draw next button
        draw_button("Next", BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if next button clicked
                if (BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and
                    BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT):
                    if guess_made:
                        # Generate new question
                        value, label = random_number()
                        start_time = datetime.datetime.now()
                        guess_made = False
                        show_result = False
                        guess = None
                        thinking_time = None
                        distance = None
                elif not guess_made and LINE_START_X <= mouse_x <= LINE_END_X:
                    # Make a guess
                    end_time = datetime.datetime.now()
                    thinking_time = (end_time - start_time).total_seconds()
                    guess = get_click_position()
                    distance = abs(guess - value)
                    guess_made = True
                    show_result = True

                    # Log to file
                    full_question = f"Click where you think {label} is"
                    with open('progress_pygame.log', 'a') as f:
                        f.write(f"{datetime.datetime.now().isoformat()}, {thinking_time:.2f}, {distance:.3f}, {label}, {value}, {full_question}\n")

        # Draw guess and correct answer if made
        if show_result:
            # Draw guess (blue circle)
            guess_x = LINE_START_X + (LINE_END_X - LINE_START_X) * guess
            pygame.draw.circle(screen, BLUE, (int(guess_x), LINE_Y), 8)

            # Draw correct answer (red circle)
            correct_x = LINE_START_X + (LINE_END_X - LINE_START_X) * value
            pygame.draw.circle(screen, RED, (int(correct_x), LINE_Y), 8)

            # Display results
            result_text = [
                f"Your guess: {round(guess, 3)}",
                f"Correct value: {value}",
                f"Thinking time: {thinking_time:.2f} seconds",
                f"Distance: {distance:.3f}"
            ]

            for i, text in enumerate(result_text):
                color = GREEN if distance < 0.1 else BLACK
                text_surf = small_font.render(text, True, color)
                screen.blit(text_surf, (50, HEIGHT - 150 + i * 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()