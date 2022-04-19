# Author: Julian Kober

from tkinter import Tk, StringVar, Radiobutton, IntVar, Button, PhotoImage
from tkinter import ttk
import random

def show_result(button):
    button.config(fg = '#444',
                      highlightthickness=2, 
                      highlightcolor="#444", 
                      highlightbackground="#444", 
                      borderwidth=0,
                      width=44,
                      height=44)

# Main Window
root = Tk()
root.title("lol")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

modes = {"Beginner": [9, 9, 10],
         "Intermediate": [16, 16, 40],
         "Expert": [30, 16, 99]}
rows = 9
cols = 9
mines = 10
fields = []
buttons = []
image = PhotoImage()

for field in range(rows*cols):
    if field < mines:
        fields.append(1)
    else:
        fields.append(0)

random.shuffle(fields)
print(fields)

for row in range(rows):
    for col in range(cols):
        button = Button(mainframe, image=image, padx=0, pady=0)

        button.config(bd=8, width=30, height=30, command=lambda button=button: show_result(button))
        button.grid(column=col, row=row)


# Start mainloop
for child in mainframe.winfo_children():
    child.grid_configure(padx=0, pady=0)

root.mainloop()
