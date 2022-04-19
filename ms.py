# Author: Julian Kober

from tkinter import Tk, StringVar, Radiobutton, IntVar, Button, PhotoImage, Frame
from tkinter import ttk
from PIL import Image, ImageTk
import random

# Main Window
root = Tk()
root.title("Minesweeper")

game = Frame(root, bg="#444", pady=5, padx=5)
game.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


modes = {"Beginner": [9, 9, 10],
         "Intermediate": [16, 16, 40],
         "Expert": [30, 16, 99]}
rows = 9
cols = 9
button_size = 30
button_border = 8
mines = 10
fields = []
buttons = []

button_all = button_size + 2 * button_border


for field in range(rows*cols):
    if field < mines:
        fields.append(1)
    else:
        fields.append(0)

random.shuffle(fields)
print(fields)

flag_img = Image.open("./img/Minesweeper_flag.png")
flag_img = flag_img.resize((button_size, button_size))
one_img = Image.open("./img/Minesweeper_1.png")
one_img = one_img.resize((button_all, button_all))
two_img = Image.open("./img/Minesweeper_2.png")
two_img = two_img.resize((button_all, button_all))
three_img = Image.open("./img/Minesweeper_3.png")
three_img = three_img.resize((button_all, button_all))
four_img = Image.open("./img/Minesweeper_4.png")
four_img = four_img.resize((button_all, button_all))
five_img = Image.open("./img/Minesweeper_5.png")
five_img = five_img.resize((button_all, button_all))
six_img = Image.open("./img/Minesweeper_6.png")
six_img = six_img.resize((button_all, button_all))
seven_img = Image.open("./img/Minesweeper_7.png")
seven_img = seven_img.resize((button_all, button_all))
eight_img = Image.open("./img/Minesweeper_8.png")
eight_img = eight_img.resize((button_all, button_all))
mine_img = Image.open("./img/Minesweeper_mine.png")
mine_img = mine_img.resize((button_all, button_all))

empty = PhotoImage()
flag = ImageTk.PhotoImage(flag_img)
one = ImageTk.PhotoImage(one_img)
two = ImageTk.PhotoImage(two_img)
three = ImageTk.PhotoImage(three_img)
four = ImageTk.PhotoImage(four_img)
five = ImageTk.PhotoImage(five_img)
six = ImageTk.PhotoImage(six_img)
seven = ImageTk.PhotoImage(seven_img)
eight = ImageTk.PhotoImage(eight_img)
mine = ImageTk.PhotoImage(mine_img)

def show_result(button):
    button.config(borderwidth=0,
                  width=button_all-2,
                  height=button_all-2)

def toggle_flag(button):
    if button["image"] == str(empty):
        button.config(image=flag)
        button.unbind("<Button-1>")
    elif button["image"] == str(flag):
        button.config(image=empty)
        button.bind("<Button-1>", lambda event, button=button: show_result(button))

for row in range(rows):
    for col in range(cols):
        button = Button(game, image=empty, padx=0, pady=0)

        button.config(bd=button_border, width=button_size, height=button_size)
        button.grid(column=col, row=row)
        button.bind("<Button-1>", lambda event, button=button: show_result(button))
        button.bind("<Button-3>", lambda event, button=button: toggle_flag(button))
        game.columnconfigure(col, minsize=button_all+4)
    game.rowconfigure(row, minsize=button_all+4)


# Start mainloop
for child in game.winfo_children():
    child.grid_configure(padx=0, pady=0)

root.mainloop()
