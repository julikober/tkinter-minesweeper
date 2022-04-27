# Author: Julian Kober

from tkinter import Tk, Button, PhotoImage, Frame, Label, Toplevel, Menu, IntVar
from PIL import Image, ImageTk
import random
import math
from tkinter import ttk

# Main Window
root = Tk()
root.resizable(False, False)
root.title("Minesweeper")

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

modes = [{"mode": "Beginner", "rows": 9, "cols": 9, "mines": 10},
         {"mode": "Intermediate", "rows": 16, "cols": 16, "mines": 40},
         {"mode": "Expert", "rows": 16, "cols": 30, "mines": 99}]
mode_var = IntVar()
rows = 10
cols = 9
button_size = 16
button_border = 3
mines = 10

button_all = button_size + 2 * button_border

buttons = []

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
digits = {}

for i in range(8):
    img = Image.open(f"./img/pixel_{i+1}.png")
    img = img.resize((button_all, button_all))

    icons.append(ImageTk.PhotoImage(img))

for i in range(10):
    img = Image.open(f"./img/pixel_digit_{i}.png")
    img = img.resize((round(button_all*(13/16)), round(button_all*(23/16))))

    digits[str(i)] = ImageTk.PhotoImage(img)

digit_minus_img = Image.open("./img/pixel_digit_minus.png")
digit_minus_img = digit_minus_img.resize((round(button_all*(13/16)), round(button_all*(23/16))))
digits["-"] = ImageTk.PhotoImage(digit_minus_img)

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
    label = Label(mine_counter, image=digits["{0:03d}".format(mines)[digit]], bd=0)
    label.grid(column=digit, row=0)
    mine_counter_digits.append(label)

for digit in range(3):
    label = Label(timer, image=digits["0"], bd=0)
    label.grid(column=digit, row=0)
    timer_digits.append(label)

class GameButton(Button):
    def __init__(self, master=None, cnf={}, **kw):
        self.button = super().__init__(master, cnf, **kw)
        self.neighbours = []
        self.value = None
        self.flag = False
        self.pressed = False

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
            timer_digits[digit].config(image=digits["{0:03d}".format(self.time % 1000)[digit]])
    
        self.timer = root.after(1000, self.update)

    def stop(self):
        root.after_cancel(self.timer)

    def reset(self):
        if self.timer:
            root.after_cancel(self.timer)
        self.time = 0
        for digit in range(3):
            timer_digits[digit].config(image=digits["0"])

def set_numbers(button):
    if button.value != 0:
        mine_count = 0

        for neighbour in button.neighbours:
            if neighbour.value == 0:
                mine_count += 1

        if mine_count > 0:
            button.value = mine_count

def check_mouse_position(button):
    bx = button.winfo_rootx()
    by = button.winfo_rooty()
    mx = game.winfo_pointerx()
    my = game.winfo_pointery()
    size = button["width"] + button["bd"] * 2
    if mx - bx in range(size+2) and my - by in range(size+2):
        return True

def update_cheat(button):
    if button.value == 0:
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

    if len([col.pressed for col in [row for row in buttons] if col.pressed]) == 0 and e:
        timer.start()
        if button.value == 0:
            for i, value in enumerate([button.value for button in buttons]):
                if value != 0:
                    buttons[i].value = 0
                    for neighbour in buttons[i].neighbours:
                        set_numbers(buttons[i])

                    button.value = None
                    set_numbers(button)
                    break
    
    if e:
        smiley_button.config(image=smiley)

    if button.value is not None:
        button.config(image=icons[button.value])

        if button.value == 0:
            if e:
                timer.stop()
                smiley_button.config(image=smiley_lose)
                for i, value in enumerate([button.value for button in buttons]):
                    if value == 0:
                        show_result(buttons[i])
                    if buttons[i]["image"] == str(flag):
                        if value == 0:
                            buttons[i].config(image=mine)
                        else:
                            buttons[i].config(image=wrong_mine)

                    for b in buttons:
                        b.bind("<Button-1>", lambda _: "break")
                        b.unbind("<ButtonRelease-1>")
                        b.unbind("<Button-3>")

                button.config(bg="#f00", activebackground="#f00")
        else:
            button.pressed = True
        
    else:
        button.pressed = True
        for neighbour in button.neighbours:
            if not neighbour.pressed:
                show_result(neighbour)
                    
    if len([button.pressed for button in buttons if button.pressed]) == rows*cols - mines:
        for b in buttons:
            if not b.pressed:
                b.config(image=flag)

        for b in buttons:
            b.bind("<Button-1>", lambda _: "break")
            b.unbind("<ButtonRelease-1>")
            b.unbind("<Button-3>")

        for digit in range(3):
            mine_counter_digits[digit].config(image=digits["0"])

        timer.stop()
        smiley_button.config(image=smiley_win)

def toggle_flag(button):
    if button["image"] == str(empty) and not button.pressed:
        button.config(image=flag)
        button.unbind("<ButtonRelease-1>")
        button.bind("<Button-1>", lambda _: "break")
        button.flag = True
    elif button["image"] == str(flag):
        button.config(image=empty)
        button.unbind("<Button-1>")
        button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))
        button.flag = False
    
    mine_count = len([button.flag for button in buttons if button.flag])
    for digit in range(3):
        mine_counter_digits[digit].config(image=digits["{0:03d}".format(mines - 100 - mine_count % -100)[digit]])

def start_game():
    global rows, cols, mines
    rows = modes[mode_var.get()]["rows"]
    cols = modes[mode_var.get()]["cols"]
    mines = modes[mode_var.get()]["mines"]
    timer.reset()

    smiley_button.config(image=smiley)

    for button in [row for row in buttons]:
        button.destroy()
    buttons.clear()

    for digit in range(3):
        mine_counter_digits[digit].config(image=digits["{0:03d}".format(mines)[digit]])

    for row in range(rows):
        for col in range(cols):
            button = GameButton(game, image=empty, padx=0, pady=0)
            buttons.append(button)
            button.config(bd=button_border, width=button_size, height=button_size, bg="#c0c0c0", activebackground="#c0c0c0", highlightthickness=0)
            button.grid(column=col, row=row)
            button.bind("<ButtonRelease-1>", lambda event, button=button: show_result(button, event) if check_mouse_position(button) else smiley_button.config(image=smiley))
            button.bind("<Button-3>", lambda event, button=button: toggle_flag(button))
            button.bind("<Enter>", lambda event, button=button: update_cheat(button))
            button.bind("<Button-1>", lambda _: smiley_button.config(image=smiley_click))
            game.columnconfigure(col, minsize=button_all+2)
        game.rowconfigure(row, minsize=button_all+2)
    

    mine_fields = random.sample(range(rows*cols), mines)
    for row in range(rows):
        for col in range(cols):
            for x in range(max(row-1, 0), min(row+1, rows - 1) + 1):
                for y in range(max(col-1, 0), min(col+1, cols - 1) + 1):
                    if buttons[x*cols + y] != buttons[row*cols + col]:
                        buttons[row*cols + col].neighbours.append(buttons[x*cols + y])

            if (row*cols + col) in mine_fields:
                buttons[row*cols + col].value = 0

    for button in buttons:
        set_numbers(button)

if __name__ == "__main__":
    timer = Timer()
    start_game()
    menubar = Menu(root)
    menubar.config(bd=0, )
    game_menu=Menu(menubar, tearoff=0)
    game_menu.config(bd=0)
    game_menu.add_command(label="New", accelerator="F2", command=start_game)
    game_menu.add_separator()
    for mode in modes:
        game_menu.add_checkbutton(label=mode["mode"], command=lambda: start_game(), onvalue=modes.index(mode), offvalue=modes.index(mode), variable=mode_var)
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