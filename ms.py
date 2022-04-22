# Author: Julian Kober

from tkinter import Tk, StringVar, Radiobutton, IntVar, Button, PhotoImage, Frame, Label, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk
import random
import sys

# Main Window
root = Tk()
root.resizable(False, False)

cheat = Toplevel(root)
cheat.overrideredirect(True)
cheat.geometry("1x1")

mainframe = Frame(root, bg = "#d9d9d9", padx=5, pady=5)
mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

top = Frame(mainframe, bg="#d9d9d9", bd=3, relief="sunken", pady=5, padx=5)
top.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

counter_border = Frame(top, bg="#d9d9d9", bd=1, relief="sunken")
counter_border.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

counter = Frame(counter_border, bg="#000")
counter.grid(column=0, row=0, sticky=("N", "W", "E", "S"))


game_border = Frame(mainframe, bg="#d9d9d9", bd=6, relief="sunken")
game_border.grid(column=0, row=1, sticky=("N", "W", "E", "S"))
game = Frame(game_border, bg="#888")
game.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


modes = {"Beginner": [9, 9, 10],
         "Intermediate": [16, 16, 40],
         "Expert": [30, 16, 99]}
rows = 9
cols = 9
button_size = 20
button_border = 3
mines = 9
fields = []
buttons = []
pressed = []

button_all = button_size + 2 * button_border


for field in range(rows*cols):
    pressed.append(False)
    if field < mines:
        fields.append(0)
    else:
        fields.append(None)

random.shuffle(fields)

for col in range(cols):
    for row in range(rows):
        if fields[col+row*rows] == None:
            mine_count = 0
            for x in range(max(col-1, 0), min(col+1, cols - 1) + 1):
                for y in range(max(row-1, 0), min(row+1, rows - 1) + 1):
                    if fields[x+y*rows] == 0:
                        mine_count += 1
            if mine_count > 0:
                fields[col+row*rows] = mine_count

flag_img = Image.open("./img/Minesweeper_flag.png")
flag_img = flag_img.resize((button_size, button_size))
mine_img = Image.open("./img/Minesweeper_mine.png")
mine_img = mine_img.resize((button_all, button_all))

empty = PhotoImage()

flag = ImageTk.PhotoImage(flag_img)
mine = ImageTk.PhotoImage(mine_img)

icons = [mine]
digits = []

for i in range(8):
    img = Image.open(f"./img/Minesweeper_{i+1}.png")
    img = img.resize((button_all, button_all))

    icons.append(ImageTk.PhotoImage(img))

for i in range(9):
    img = Image.open(f"./img/digit_{i}.png")
    img = img.resize((18, 36))

    digits.append(ImageTk.PhotoImage(img))

def check_mouse_position(button):
    bx = button.winfo_rootx()
    by = button.winfo_rooty()
    mx = game.winfo_pointerx()
    my = game.winfo_pointery()
    if mx - bx in range(button_all+5) and my - by in range(button_all+5):
        return True

def update_cheat(button):
    if fields[buttons.index(button)] == 0:
        cheat.config(bg="#000")
    else:
        cheat.config(bg="#fff")

def show_result(button, e = None):
    button.config(borderwidth=0,
                  width=button_all-1,
                  height=button_all-1,
                  activebackground="#d9d9d9")
    button.unbind("<ButtonRelease-1")
    button.bind("<Button-1>", lambda _: "break")
    index = buttons.index(button)
    
    if button["image"] == str(flag):
        button.config(image=empty)

    icon = fields[index]
    if icon is not None:
        button.config(image=icons[icon])

        if icon == 0:
            if e:
                print("lost!")
                for i, field in enumerate(fields):
                    if field == 0:
                        show_result(buttons[i])
                    if buttons[i]["image"] == str(flag):
                        buttons[i].config(bg="#f00", activebackground="#f00")

                    for b in buttons:
                        b.bind("<Button-1>", lambda _: "break")
                        b.unbind("<ButtonRelease-1>")
                        b.unbind("<Button-3>")

                button.config(bg="#f00", activebackground="#f00")
        else:
            pressed[index] = True
        
    else:
        pressed[index] = True
        col = index % cols
        row = index // cols
        for x in range(max(col-1, 0), min(col+1, cols - 1) + 1):
            for y in range(max(row-1, 0), min(row+1, rows - 1) + 1):
                if not pressed[x+y*rows]:
                    show_result(buttons[x+y*rows])
                    
    if len([x for x in pressed if x]) == rows*cols - mines:
        print("won!")
        root.destroy()

def toggle_flag(button):
    if button["image"] == str(empty) and not pressed[buttons.index(button)]:
        button.config(image=flag)
        button.unbind("<ButtonRelease-1>")
        button.bind("<Button-1>", lambda _: "break")
    elif button["image"] == str(flag):
        button.config(image=empty)
        button.unbind("<Button-1>")
        button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else None)

for row in range(rows):
    for col in range(cols):
        button = Button(game, image=empty, padx=0, pady=0)
        buttons.append(button)
        button.config(bd=button_border, width=button_size, height=button_size, bg="#d9d9d9", activebackground="#d9d9d9")
        button.grid(column=col, row=row, sticky=("N", "W"))
        button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else None)
        button.bind("<Button-3>", lambda event, button=button: toggle_flag(button))
        button.bind("<Enter>", lambda event, button=button: update_cheat(button))
        game.columnconfigure(col, minsize=button_all+4)
    game.rowconfigure(row, minsize=button_all+4)

Label(counter, image=digits[4], bd=0).grid(column=0, row=0, padx=2, pady=2)
Label(counter, image=digits[2], bd=0).grid(column=1, row=0, padx=2, pady=2)
Label(counter, image=digits[0], bd=0).grid(column=2, row=0, padx=2, pady=2)
# Start mainloop
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
