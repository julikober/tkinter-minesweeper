# Author: Julian Kober

from tkinter import Tk, Button, PhotoImage, Frame, Label, Toplevel, Menu
from PIL import Image, ImageTk
import random
import math
from tkinter import ttk

# Main Window
root = Tk()
root.resizable(False, False)

cheat = Toplevel(root)
cheat.overrideredirect(True)
cheat.geometry("1x1")

mainframe = Frame(root, bg = "#c0c0c0", padx=5, pady=5)
mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

top = Frame(mainframe, bg="#c0c0c0", bd=3, relief="sunken", pady=3, padx=3)
top.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
top.columnconfigure(1, weight=1)

game_border = Frame(mainframe, bg="#c0c0c0", bd=3, relief="sunken")
game_border.grid(column=0, row=1, sticky=("N", "W", "E", "S"))
game = Frame(game_border, bg="#737373")
game.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

modes = {"Beginner": [9, 9, 10],
         "Intermediate": [16, 16, 40],
         "Expert": [30, 16, 99]}
rows = 9
cols = 9
button_size = 12
button_border = 2
mines = 10

button_all = button_size + 2 * button_border

fields = []
buttons = []
pressed = []
flags = []

flag_img = Image.open("./img/pixel_flag.png")
flag_img = flag_img.resize((button_all, button_all))
mine_img = Image.open("./img/pixel_mine.png")
mine_img = mine_img.resize((button_all, button_all))
wrong_mine_img = Image.open("./img/pixel_wrong_mine.png")
wrong_mine_img = wrong_mine_img.resize((button_all, button_all))
smiley_img = Image.open("./img/pixel_smiley.png")
smiley_img = smiley_img.resize((int(button_all*(3/2)), int(button_all*(3/2))))
smiley_lose = Image.open("./img/pixel_smiley_lose.png")
smiley_lose = smiley_lose.resize((int(button_all*(3/2)), int(button_all*(3/2))))
smiley_win = Image.open("./img/pixel_smiley_win.png")
smiley_win = smiley_win.resize((int(button_all*(3/2)), int(button_all*(3/2))))
smiley_click = Image.open("./img/pixel_smiley_click.png")
smiley_click = smiley_click.resize((int(button_all*(3/2)), int(button_all*(3/2))))

empty = PhotoImage()

flag = ImageTk.PhotoImage(flag_img)
mine = ImageTk.PhotoImage(mine_img)
smiley = ImageTk.PhotoImage(smiley_img)
smiley_lose = ImageTk.PhotoImage(smiley_lose)
smiley_win = ImageTk.PhotoImage(smiley_win)
smiley_click = ImageTk.PhotoImage(smiley_click)
wrong_mine = ImageTk.PhotoImage(wrong_mine_img)

icons = [mine]
digits = []

for i in range(8):
    img = Image.open(f"./img/pixel_{i+1}.png")
    img = img.resize((button_all, button_all))

    icons.append(ImageTk.PhotoImage(img))

for i in range(10):
    img = Image.open(f"./img/pixel_digit_{i}.png")
    img = img.resize((round(button_all*(13/16)), round(button_all*(23/16))))

    digits.append(ImageTk.PhotoImage(img))

mine_counter_border = Frame(top, bg="#c0c0c0", bd=1, relief="sunken")
mine_counter_border.grid(column=0, row=0)

mine_counter = Frame(mine_counter_border, bg="#000")
mine_counter.grid(column=0, row=0)

smiley_button = Button(top, image=smiley, bd=button_border, width=int(button_all*(3/2) - button_border*2 - 2), height=int(button_all*(3/2) - button_border*2 - 2))
smiley_button.config(bg="#c0c0c0", activebackground="#c0c0c0", highlightbackground="#737373", highlightthickness=1)
smiley_button.grid(column=1, row=0)
smiley_button.bind("<ButtonRelease-1>", lambda event, button=smiley_button, current=smiley_button["image"]: start_game() if check_mouse_position(button) else None)

timer_border = Frame(top, bg="#c0c0c0", bd=1, relief="sunken")
timer_border.grid(column=2, row=0)

timer = Frame(timer_border, bg="#000")
timer.grid(column=0, row=0)


for child in mainframe.winfo_children():
    child.grid_configure(padx=3, pady=3)

mine_counter_digits = []
timer_digits = []

for digit in range(3):
    label = Label(mine_counter, image=digits[int("{0:03d}".format(mines)[digit])], bd=0)
    label.grid(column=digit, row=0)
    mine_counter_digits.append(label)

for digit in range(3):
    label = Label(timer, image=digits[0], bd=0)
    label.grid(column=digit, row=0)
    timer_digits.append(label)

class Timer():
    def __init__(self):
        self.time = 0
        self.running = False
        self.timer = None

    def start(self):
        self.time = 0
        self.timer = root.after(1000, self.update)
    
    def update(self):
        self.time += 1
        for digit in range(3):
            timer_digits[digit].config(image=digits[int("{0:03d}".format(self.time)[digit])])
    
        self.timer = root.after(1000, self.update)

    def stop(self):
        root.after_cancel(self.timer)

    def reset(self):
        if self.timer:
            root.after_cancel(self.timer)
        self.time = 0
        for digit in range(3):
            timer_digits[digit].config(image=digits[0])

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
    if button["image"] == str(flag):
        return 
    button.config(borderwidth=0,
                  width=button_all-1,
                  height=button_all-1,
                  activebackground="#c0c0c0")
    button.unbind("<ButtonRelease-1")
    button.bind("<Button-1>", lambda _: "break")
    index = buttons.index(button)

    if len([x for x in pressed if x]) == 0 and e:
        timer.start()
    
    if e:
        smiley_button.config(image=smiley)

    icon = fields[index]
    if icon is not None:
        button.config(image=icons[icon])

        if icon == 0:
            if e:
                timer.stop()
                smiley_button.config(image=smiley_lose)
                for i, field in enumerate(fields):
                    if field == 0:
                        show_result(buttons[i])
                    if buttons[i]["image"] == str(flag):
                        if field == 0:
                            buttons[i].config(image=mine)
                        else:
                            buttons[i].config(image=wrong_mine)

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

        for digit in range(3):
            mine_counter_digits[digit].config(image=digits[0])

        timer.stop()
        smiley_button.config(image=smiley_win)

def toggle_flag(button):
    if button["image"] == str(empty) and not pressed[buttons.index(button)]:
        button.config(image=flag)
        button.unbind("<ButtonRelease-1>")
        button.bind("<Button-1>", lambda _: "break")
        flags[buttons.index(button)] = True
    elif button["image"] == str(flag):
        button.config(image=empty)
        button.unbind("<Button-1>")
        button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))
        flags[buttons.index(button)] = False
    
    mine_count = mines - len([x for x in flags if x])
    for digit in range(3):
        mine_counter_digits[digit].config(image=digits[int("{0:03d}".format(mine_count)[digit])])

def start_game():
    timer.reset()
    smiley_button.config(image=smiley)
    fields.clear()
    pressed.clear()
    flags.clear()
    for button in buttons:
        button.destroy()
    buttons.clear()
    for digit in range(3):
        mine_counter_digits[digit].config(image=digits[int("{0:03d}".format(mines)[digit])])

    for field in range(rows*cols):
        pressed.append(False)
        flags.append(False)
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
            button.config(bd=button_border, width=button_size, height=button_size, bg="#c0c0c0", activebackground="#c0c0c0", highlightthickness=0)
            button.grid(column=col, row=row)
            button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))
            button.bind("<Button-3>", lambda event, button=button: toggle_flag(button))
            button.bind("<Enter>", lambda event, button=button: update_cheat(button))
            button.bind("<Button-1>", lambda _: smiley_button.config(image=smiley_click))
            game.columnconfigure(col, minsize=button_all+2)
        game.rowconfigure(row, minsize=button_all+2)

if __name__ == "__main__":
    timer = Timer()
    start_game()
    menubar = Menu(root)
    menubar.config(bd=0, )
    game_menu=Menu(menubar, tearoff=0)
    game_menu.config(bd=0)
    game_menu.add_command(label="New", accelerator="F2", command=start_game)
    game_menu.add_separator()
    game_menu.add_radiobutton(label="Beginner", command=lambda: start_game(), value=0)
    game_menu.add_radiobutton(label="Intermediate", command=lambda: start_game(), value=1)
    game_menu.add_radiobutton(label="Expert", command=lambda: start_game(), value=2)
    game_menu.add_separator()
    game_menu.add_checkbutton(label="Marks (?)")
    game_menu.add_checkbutton(label="Color")
    game_menu.add_checkbutton(label="Sound")
    game_menu.add_separator()
    game_menu.add_command(label="Best Times...")
    game_menu.add_separator()
    game_menu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="Game", menu=game_menu)
    root.config(menu=menubar)
    root.mainloop()