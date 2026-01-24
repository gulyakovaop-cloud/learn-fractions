import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from fractions import Fraction

plt.ion()  # Make interactive

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

# Generate number
value, label = random_number()

fig, ax = plt.subplots(figsize=(8, 2))

# Draw number line
ax.plot([0, 1], [0, 0], linewidth=3)
ax.set_xlim(0, 1)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.set_title(f"Click where you think {label} is")

def onclick(event):
    if event.xdata is None:
        return

    guess = event.xdata

    # Draw guess
    ax.plot(guess, 0, 'bo', label="Your guess")

    # Draw correct answer
    ax.plot(value, 0, 'ro', label="Correct")

    ax.legend()
    plt.draw()

    print(f"Your guess: {round(guess, 3)}")
    print(f"Correct value: {value}")

    fig.canvas.mpl_disconnect(cid)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

# Keep the window open until manually closed
while plt.fignum_exists(fig.number):
    plt.pause(0.1)
