'''Seven segment display of hex digits.'''
import tkinter as tk
root = tk.Tk()
screen = tk.Canvas(root)
screen.grid()

# Order 7 segments clockwise from top left, with crossbar last.
# Coordinates of each segment are (x0, y0, x1, y1) 
# given as offsets from top left measured in segment lengths.
offsets = (
    (0, 0, 1, 0),  # top
    (1, 0, 1, 1),  # upper right
    (1, 1, 1, 2),  # lower right
    (0, 2, 1, 2),  # bottom
    (0, 1, 0, 2),  # lower left
    (0, 0, 0, 1),  # upper left
    (0, 1, 1, 1),  # middle
)
# Segments used for each digit; 0, 1 = off, on.
digits = (
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
    (1, 1, 1, 0, 1, 1, 1),  # 10=A
    (0, 0, 1, 1, 1, 1, 1),  # 11=b
    (1, 0, 0, 1, 1, 1, 0),  # 12=C
    (0, 1, 1, 1, 1, 0, 1),  # 13=d
    (1, 0, 0, 1, 1, 1, 1),  # 14=E
    (1, 0, 0, 0, 1, 1, 1),  # 15=F
)


class Digit:
    def __init__(self, canvas, *, x=10, y=10, length=20, width=3):
        self.canvas = canvas
        l = length
        self.segs = []
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x + x0*l, y + y0*l, x + x1*l, y + y1*l,
                width=width, state = 'hidden'))
    def show(self, num):
        for iid, on in zip(self.segs, digits[num]):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')



dig = Digit(screen)
n = 0
def update():
    global n
    dig.show(n)
    n = (n+1) % 16
    root.after(1000, update)
root.after(1000, update)
root.mainloop()