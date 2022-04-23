# Author: Julian Kober

from configparser import Interpolation
from tkinter import Tk, StringVar, Radiobutton, IntVar, Button, PhotoImage, Frame, Label, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk
import random
import sys
import cv2
from pygments import highlight

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
top.columnconfigure(1, weight=1)

game_border = Frame(mainframe, bg="#d9d9d9", bd=6, relief="sunken")
game_border.grid(column=0, row=1, sticky=("N", "W", "E", "S"))
game = Frame(game_border, bg="#828282")
game.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


modes = {"Beginner": [9, 9, 10],
         "Intermediate": [16, 16, 40],
         "Expert": [30, 16, 99]}
rows = 9
cols = 9
button_size = 16
button_border = 3
mines = 10
fields = []
buttons = []
pressed = []

button_all = button_size + 2 * button_border

flag_img = Image.open("./img/pixel_flag.png")
flag_img = flag_img.resize((button_all, button_all))
mine_img = Image.open("./img/pixel_mine.png")
mine_img = mine_img.resize((button_all, button_all))
smiley_img = Image.open("./img/pixel_smiley.png")
smiley_img = smiley_img.resize((int(button_size*(3/2) + button_border*2), int(button_size*(3/2) + button_border*2)))
smiley_lose = Image.open("./img/pixel_smiley_lose.png")
smiley_lose = smiley_lose.resize((int(button_size*(3/2) + button_border*2), int(button_size*(3/2) + button_border*2)))
smiley_win = Image.open("./img/pixel_smiley_win.png")
smiley_win = smiley_win.resize((int(button_size*(3/2) + button_border*2), int(button_size*(3/2) + button_border*2)))
smiley_click = Image.open("./img/pixel_smiley_click.png")
smiley_click = smiley_click.resize((int(button_size*(3/2) + button_border*2), int(button_size*(3/2) + button_border*2)))

empty = PhotoImage()

flag = ImageTk.PhotoImage(flag_img)
mine = ImageTk.PhotoImage(mine_img)
smiley = ImageTk.PhotoImage(smiley_img)
smiley_lose = ImageTk.PhotoImage(smiley_lose)
smiley_win = ImageTk.PhotoImage(smiley_win)
smiley_click = ImageTk.PhotoImage(smiley_click)

icons = [mine]
digits = []

for i in range(8):
    img = Image.open(f"./img/pixel_{i+1}.png")
    img = img.resize((button_all, button_all))

    icons.append(ImageTk.PhotoImage(img))

for i in range(10):
    img = Image.open(f"./img/pixel_digit_{i}.png")
    img = img.resize((int((button_all*(3/2) - 4)*(11/19)), int(button_all*(3/2) - 4)))

    digits.append(ImageTk.PhotoImage(img))

timer_border = Frame(top, bg="#d9d9d9", bd=1, relief="sunken")
timer_border.grid(column=0, row=0)

timer = Frame(timer_border, bg="#000")
timer.grid(column=0, row=0)

smiley_button = Button(top, image=smiley, bd=button_border, width=int(button_size*(3/2)), height=int(button_size*(3/2)))
smiley_button.config(highlightthickness=0, bg="#d9d9d9", activebackground="#d9d9d9")
smiley_button.grid(column=1, row=0)
smiley_button.bind("<ButtonRelease-1>", lambda event, button=smiley_button: start_game() if check_mouse_position(button) else None)

mine_counter_border = Frame(top, bg="#d9d9d9", bd=1, relief="sunken")
mine_counter_border.grid(column=2, row=0)

mine_counter = Frame(mine_counter_border, bg="#000")
mine_counter.grid(column=0, row=0)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

for digit in range(3):
    label = Label(mine_counter, image=digits[int("{0:03d}".format(mines)[digit])], bd=0)
    label.grid(column=digit, row=0)


for digit in range(3):
    label = Label(timer, image=digits[int("{0:03d}".format(mines)[digit])], bd=0)
    label.grid(column=digit, row=0)


def check_mouse_position(button):
    bx = button.winfo_rootx()
    by = button.winfo_rooty()
    mx = game.winfo_pointerx()
    my = game.winfo_pointery()
    size = button["width"] + button["bd"] * 2
    if mx - bx in range(size+2) and my - by in range(size+2):
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
    
    if e:
        smiley_button.config(image=smiley)

    if button["image"] == str(flag):
        button.config(image=empty)

    icon = fields[index]
    if icon is not None:
        button.config(image=icons[icon])

        if icon == 0:
            if e:
                smiley_button.config(image=smiley_lose)
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
                if not pressed[x+y*cols]:
                    show_result(buttons[x+y*cols])
                    
    if len([x for x in pressed if x]) == rows*cols - mines:
        for i, b in enumerate(buttons):
            if not pressed[i]:
                b.config(image=flag)

        for b in buttons:
            b.bind("<Button-1>", lambda _: "break")
            b.unbind("<ButtonRelease-1>")
            b.unbind("<Button-3>")

        smiley_button.config(image=smiley_win)

def toggle_flag(button):
    if button["image"] == str(empty) and not pressed[buttons.index(button)]:
        button.config(image=flag)
        button.unbind("<ButtonRelease-1>")
        button.bind("<Button-1>", lambda _: "break")
    elif button["image"] == str(flag):
        button.config(image=empty)
        button.unbind("<Button-1>")
        button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))

def start_game():
    smiley_button.config(image=smiley)
    fields.clear()
    pressed.clear()
    for button in buttons:
        button.unbind("<Button-1>")
        button.unbind("<ButtonRelease-1>")
        button.unbind("<Button-3>")
        button.unbind("<Enter>")
    buttons.clear()
    for field in range(rows*cols):
        pressed.append(False)
        if field < mines:
            fields.append(0)
        else:
            fields.append(None)

    random.shuffle(fields)

    for col in range(cols):
        for row in range(rows):
            if fields[col+row*cols] == None:
                mine_count = 0
                for x in range(max(col-1, 0), min(col+1, cols - 1) + 1):
                    for y in range(max(row-1, 0), min(row+1, rows - 1) + 1):
                        if fields[x+y*cols] == 0:
                            mine_count += 1
                if mine_count > 0:
                    fields[col+row*cols] = mine_count

    for row in range(rows):
        for col in range(cols):
            button = Button(game, image=empty, padx=0, pady=0)
            buttons.append(button)
            button.config(bd=button_border, width=button_size, height=button_size, bg="#d9d9d9", activebackground="#d9d9d9", highlightthickness=0)
            button.grid(column=col, row=row)
            button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))
            button.bind("<Button-3>", lambda event, button=button: toggle_flag(button))
            button.bind("<Enter>", lambda event, button=button: update_cheat(button))
            button.bind("<Button-1>", lambda _: smiley_button.config(image=smiley_click))
            game.columnconfigure(col, minsize=button_all+2)
        game.rowconfigure(row, minsize=button_all+2)

if __name__ == "__main__":
    start_game()
    root.mainloop()