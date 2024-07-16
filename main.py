from tkinter import *
import pandas
from random import *

BACKGROUND_COLOR = "#B1DDC6"
word = {}

# Try to load the words to learn from a CSV file
try:
    data = pandas.read_csv("./data/word_to_learn.csv")
except FileNotFoundError:

    # If the file doesn't exist, use the original French words CSV file
    data = pandas.read_csv("./data/french_words.csv")

    # Convert the data to a list of dictionaries (records)
    deck = data.to_dict(orient="records")
else:
    # If the file exists, convert the data to a list of dictionaries (records)
    deck = data.to_dict(orient="records")


# Function to flip the flashcard to show the English word
def flip():
    card_canvas.itemconfig(image, image=card_back_img)
    card_canvas.itemconfig(front_word, text=word["English"], fill="white")
    card_canvas.itemconfig(front_title, text="English", fill="white")


# Function to display the next word on the flashcard
def next_word():
    global word, timer

    # Cancel the previous timer to avoid multiple calls to flip
    window.after_cancel(timer)

    # Choose a random word from the deck
    word = choice(deck)
    # Update the flashcard with the new word
    card_canvas.itemconfig(image, image=card_front_img)
    card_canvas.itemconfig(front_word, text=word["French"], fill="black")
    card_canvas.itemconfig(front_title, text="French", fill="black")
    # Set a timer to flip the card after 3 seconds
    timer = window.after(3000, flip)


# Function to handle the action when the user knows the word
def easy_words():
    # Remove the word from the deck
    deck.remove(word)

    # Save the updated deck to the CSV file
    new_data = pandas.DataFrame(deck)
    new_data.to_csv("./data/word_to_learn.csv", index=False)

    # Display the next word if there are any words left
    if len(deck) > 0:
        next_word()


# Create the main window
window = Tk()

window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.title("FlashCard")

# Load images for the flashcard
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
right_answer_img = PhotoImage(file="./images/right.png")
wrong_answer_img = PhotoImage(file="./images/wrong.png")

# Create the canvas for the flashcard
card_canvas = Canvas(width=800, height=526)
image = card_canvas.create_image(400, 265, image=card_front_img)
card_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
front_title = card_canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_canvas.grid(column=0, row=0, columnspan=2)
front_word = card_canvas.create_text(400, 265, text="", font=("Ariel", 60, "bold"))

# Create buttons for right and wrong answers
right_answer_button = Button(image=right_answer_img, highlightthickness=0, bd=0, command=easy_words)
right_answer_button.grid(column=1, row=1)
wrong_answer_button = Button(image=wrong_answer_img, highlightthickness=0, bd=0, command=next_word)
wrong_answer_button.grid(column=0, row=1)

# Set a timer to flip the card after 3 seconds
timer = window.after(3000, flip)

# Display the first word
next_word()
window.mainloop()
