from tkinter import *
import random
import pandas

BACKGROUND_COLOUR = '#FAEACB'
start_counter = 3
test_counter = 60
word_counter = 0
wrong_words_counter = 0
character_counter = 0
timer = ""
active_word = ""

words = pandas.read_csv("words.csv")
word_list = [row.values[0] for (index, row) in words.iterrows()]


def restart():
    global start_counter, test_counter, word_counter, timer, active_word, wrong_words_counter, character_counter
    window.after_cancel(timer)
    canvas.itemconfig(screen_counter, text="")
    user_entry.delete(0, END)
    user_entry.grid_forget()
    restart_button.grid_forget()
    word_counter = 0
    wrong_words_counter = 0
    character_counter = 0
    timer = ""
    active_word = ""
    start_screen()


def start_screen():
    canvas.itemconfig(title, text=" Welcome to Typing Speed Test ", font=("Ariel", 40, "italic"))
    canvas.itemconfig(instructions, text=" Press space to submit and show the next word. ")
    canvas.grid(column=0, row=0, columnspan=3, rowspan=3)
    start_button.grid(column=1, row=2)


def test_screen():
    global test_counter, active_word
    active_word = random.choice(word_list)
    canvas.itemconfig(title, text=f" {active_word} ")
    user_entry.grid(column=1, row=1)
    user_entry.focus()
    counter(test_counter, 'test')


def countdown_screen():
    global start_counter
    canvas.itemconfig(instructions, text="")
    start_button.grid_forget()
    restart_button.grid(column=1, row=2)
    counter(start_counter, 'start')


def counter(count, timer_choice):
    global timer, wrong_words_counter, word_counter
    if timer_choice == 'start':
        if count > 0:
            canvas.itemconfig(title, text=f'{count}')
            timer = window.after(1000, counter, count - 1, 'start')
        else:
            canvas.itemconfig(title, text=' Ready?... ')
            timer = window.after(1000, test_screen)
    else:
        if count > 0:
            canvas.itemconfig(screen_counter, text=f'Time remaining: {count}')
            timer = window.after(1000, counter, count - 1, 'test')
        else:
            percentage = round(((word_counter - wrong_words_counter) / word_counter) * 100, 1)
            if word_counter == 0:
                percentage = 0
            canvas.itemconfig(screen_counter, text='')
            canvas.itemconfig(title,
                              text=f" You typed {word_counter + wrong_words_counter} words but spelt "
                                   f"{wrong_words_counter} incorrectly ({percentage}%). \n Your WPM (Words Per Minute) "
                                   f"is {word_counter}. \n Your CPM (Characters Per Minute) is {character_counter}. ",
                              font=('Ariel', 20, 'bold'))
            user_entry.grid_forget()


def new_word(event=None):
    global word_list, word_counter, active_word, wrong_words_counter, character_counter
    answer = user_entry.get()
    if str(answer) == str(active_word):
        word_counter += 1
        character_counter += len(active_word)
    else:
        wrong_words_counter += 1
    active_word = random.choice(word_list)
    canvas.itemconfig(title, text=f" {active_word} ")
    user_entry.delete(0, END)


def callback(P):  # Block space-key (' ') from being used in 'user_entry'
    if P == " ":
        return False
    else:
        return True


window = Tk()
window.title("Typing Speed Test")
window.minsize()
window.config(padx=20, pady=20, bg=BACKGROUND_COLOUR)

canvas = Canvas(width=800, height=500, highlightthickness=0, bg=BACKGROUND_COLOUR)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
instructions = canvas.create_text(400, 210, text="", font=("Ariel", 15, "italic"), fill="black")
screen_counter = canvas.create_text(650, 50, text="", font=("Ariel", 15, "italic"), fill="black")
start_button = Button(text="Begin Test", font=('Ariel', 20, 'bold'), command=countdown_screen)
restart_button = Button(text="Restart Test", font=('Ariel', 20, 'bold'), command=restart)
user_entry = Entry(font=('Ariel', 15, 'normal'), justify='center', validate='all',
                   validatecommand=(window.register(callback), '%P'))
user_entry.bind("<space>", new_word)

start_screen()

window.mainloop()
