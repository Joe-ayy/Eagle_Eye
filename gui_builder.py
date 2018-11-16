from tkinter import *


class BuildContainer(Frame):
    # Build a frame that acts as container with specified master container (could be a window also)
    # and values for its dimensions and placement
    def __init__(self, master, width, height, side, anchor, bg=None):
        Frame.__init__(self, master=master, width=width, height=height, bg=bg)
        self.pack(side=side, anchor=anchor)


class BuildCanvas(Canvas):
    # Build a canvas that goes into a master container and has the purpose of displaying an image
    def __init__(self, master, width, height, anchor, bg=None):
        Canvas.__init__(self, master=master, width=width, height=height, bg=bg)
        self.pack(anchor=anchor)


class BuildLabel(Label):
    # Build a label that will be used to display information - to be updated later
    def __init__(self, master, anchor):
        Label.__init__(self, master=master)
        self.pack(anchor=anchor)


class BuildWindow(Toplevel):
    # Build a window that will hold the container frames and values for its dimensions and placement
    def __init__(self, title, width, height, r_width=False, r_height=False, tl_x=10, tl_y=10):
        Toplevel.__init__(self, master=None)
        geometry_string = str(width) + "x" + str(height) + "+" + str(tl_x) + "+" + str(tl_y)
        self.geometry(geometry_string)
        self.resizable(width=r_width, height=r_height)
        self.title(string=title)
