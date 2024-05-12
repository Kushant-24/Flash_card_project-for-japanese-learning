from tkinter import Button,Tk
from tkinter import PhotoImage,Canvas
from turtle import title
import pandas
from random import choice
import os
import shutil


os.system('cls')



# File and Word Storage area
try:
    data = pandas.read_csv("leave_to_learn.csv")
    total_words = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("japanese_data.csv")
    total_words = data.to_dict(orient="records")


# Global VAriables
background_color = "#B1DDC6"
current_word = {}



def next_card():
    global current_word, timer
    current_word = choice(total_words)
    root.after_cancel(timer)
    french_word = current_word["Japanese"]
    canvas.itemconfig(language_text,text="Japanese",fill="black")
    canvas.itemconfig(word_text,text=french_word,fill="black")
    canvas.itemconfig(card_images,image=front_image)
    timer = root.after(3000,func=flip_card)


def flip_card():
    canvas.itemconfig(word_text,text=current_word["English"],fill="white")
    canvas.itemconfig(language_text,text="English",fill="white")
    canvas.itemconfig(card_images,image=back_image)


def known_word():
    if len(total_words)-1 == 0:
        root.after_cancel(timer)
        os.remove("leave_to_learn.csv")
        canvas.itemconfig(language_text,text="Congratulations!",font=("arial",25,"bold"))
        canvas.itemconfig(word_text,text="You have finished lessons.",font=("arial",20,"normal"))
        cross_button.config(command=root.destroy)
        tick_button.config(command=root.destroy)
        shutil.rmtree("leave_to_learn.csv",ignore_errors=True)
        pass
    else:
        total_words.remove(current_word)
        data = pandas.DataFrame(total_words)
        data.to_csv("leave_to_learn.csv",index=False)
        next_card()

# Window 
root = Tk()
root.title("Flash Card(Japanese)")
root.config(padx=50,pady=50,bg=background_color)
timer = root.after(3000,func=flip_card)


# Front and Back Images work
canvas = Canvas(root,width=800,height=526,highlightthickness=0,bg=background_color)
front_image = PhotoImage(file="flash_card_2.0\\images\\card_front.png")
back_image = PhotoImage(file="flash_card_2.0\\images\\card_back.png")
card_images = canvas.create_image(400,263,image=front_image)
canvas.grid(row=0,column=0,columnspan=2)


# Text on images stuff
language_text = canvas.create_text(400,150,text="Title",font=("arial",35,"italic"))
word_text = canvas.create_text(400,263,text="Japanese",font=("arial",45,"normal"))

# Tick and Cross Buttons
tick_image = PhotoImage(file="flash_card_2.0\\images\\right.png")
cross_image = PhotoImage(file="flash_card_2.0\\images\\wrong.png")

tick_button = Button(image=tick_image,command=known_word)
tick_button.grid(row=1,column=1)
cross_button = Button(image=cross_image,command=next_card)
cross_button.grid(row=1,column=0)

# Function call
next_card()

root.mainloop()
