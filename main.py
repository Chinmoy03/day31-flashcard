from tkinter import *
import pandas
import random as r

BACKGROUND_COLOR = "#B1DDC6"


# To create the words to learn file
def create_file():
    new_dict = {key:[value2 for (key2, value2) in value.items()] for (key, value) in french_dict.items()}
    print(new_dict)
    save_data = pandas.DataFrame.from_dict(new_dict)
    with open("./data/words_to_learn.csv", "w", encoding='utf-8', newline='\r\n') as data_file:
        save_data.to_csv(data_file, index=False)
    window.destroy()


# update function for the buttons
def wrong_update():
    create_flashcard()


def right_update():
    global index
    del french_dict["French"][index]
    del french_dict["English"][index]
    index_list.remove(index)
    create_flashcard()


# Get a random index
def get_index():
    global index
    index = r.choice(index_list)


# Show the back side of the card
def show_back():
    global index
    flash_card.itemconfig(back, state="normal")
    flash_card.itemconfig(language, text="English")
    flash_card.itemconfig(word, text=french_dict["English"][index])


# Create new flashcard
def create_flashcard():
    flash_card.itemconfig(back, state="hidden")
    global index
    get_index()
    french_word = french_dict["French"][index]
    flash_card.itemconfig(language, text="French")
    flash_card.itemconfig(word, text=french_word)
    window.after(3000, func=show_back)


# Create the Dictionary of flashcards
data = {}
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")

data_frame = pandas.DataFrame(data)
french_dict = data_frame.to_dict(orient='dict')
index_list = [key for (key, value) in french_dict["French"].items()]

# Create the UI
index = -1
window = Tk()
window.title("Flashy")
window.configure(bg=BACKGROUND_COLOR, padx=50, pady=50)

# create the canvas
flash_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
front = flash_card.create_image(400, 263, image=front_image)
back = flash_card.create_image(400, 263, image=back_image)
flash_card.itemconfig(back, state="hidden")
language = flash_card.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word = flash_card.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
flash_card.grid(row=0, column=0, columnspan=2)

# create buttons
right = PhotoImage(file="./images/right.png")
right_button = Button(image=right, highlightthickness=0, borderwidth=0, command=right_update)
right_button.grid(row=1, column=1)
wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, borderwidth=0, command=wrong_update)
wrong_button.grid(row=1, column=0)
window.protocol("WM_DELETE_WINDOW", create_file)
create_flashcard()

window.mainloop()
