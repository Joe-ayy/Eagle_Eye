import cv2
from tkinter import *
import PIL.Image
import PIL.ImageTk
import numpy as np
from gui_builder import *
import file_and_image_handling as fih
import timestamp_ops
import config as c

# This module serves multiple purposes:
# 1. Provide an interactive GUI to the user
# 2. Retrieve data and files from directories and other .py files
# 3. Does some of the clean up after the program is to be exited


# Class that creates the application
class MainPage:
    #region ### Establish the dimensions for the containers ###
    c1_w = c.width * c.c1_width_ratio  # Container 1 width
    c2_w = c.width * c.c2_width_ratio  # Container 2 width

    img_w = c2_w  # Image width
    img_h = c.height * c.img_height_ratio  # Image height

    map_h = c.height * c.map_height_ratio  # Map height
    util_h = c.height * c.util_height_ratio  # Utility height
    #endregion

    # Hold on to the values for the images so they are not garbage collected
    map_image = None
    store_image_1 = None
    store_image_2 = None
    store_image_3 = None

    def __init__(self):
        # Construct the window
        self.app_window = BuildWindow(c.title, c.width, c.height)

        #region ### Construct all the containers ###
        self.win_con = BuildContainer(self.app_window, c.width, c.height, LEFT, NW)  # Window Container

        self.con1 = BuildContainer(self.win_con, MainPage.c1_w, c.height, LEFT, NW)  #Container 1, left side of window
        self.con2 = BuildContainer(self.win_con, MainPage.c2_w, c.height, RIGHT, NW)  #Container 2, right side of window

        self.map_con = BuildContainer(self.con1, MainPage.c1_w, MainPage.map_h, TOP, NW)  # Map container
        self.util_con = BuildContainer(self.con1, MainPage.c1_w, MainPage.util_h, BOTTOM, NW)  # Utility container

        self.img1_con = BuildContainer(self.con2, MainPage.img_w, MainPage.img_h, TOP, NW)  # Image 1 container
        self.img2_con = BuildContainer(self.con2, MainPage.img_w, MainPage.img_h, TOP, NW)  # Image 2 container
        self.img3_con = BuildContainer(self.con2, MainPage.img_w, MainPage.img_h, BOTTOM, NW)  # Image 3 container
        #endregion

        #region ### Construct all the canvases ###
        self.map_canvas = BuildCanvas(self.map_con, self.c1_w, self.map_h, NW, "Blue")  # Map Canvas

        self.img1_canvas = BuildCanvas(self.img1_con, MainPage.img_w, MainPage.img_h, NW, "Red")  # Image 1 Canvas
        self.img2_canvas = BuildCanvas(self.img2_con, MainPage.img_w, MainPage.img_h, NW, "Yellow")  # Image 2 Canvas
        self.img3_canvas = BuildCanvas(self.img3_con, MainPage.img_w, MainPage.img_h, NW, "Green")  # Image 3 Canvas
        #endregion

        # Set the focus to the map canvas for keybindings
        self.map_canvas.focus_set()

    def draw_map(self, path):
        # Get the map's path
        map_path = fih.get_map_path(path)

        #Save the information for the map, this will be used to change variable values
        temp_map_img = cv2.imread(map_path)
        c.orig_map_height, c.orig_map_width, _ = temp_map_img.shape

        # Set the x and y map ratios
        timestamp_ops.set_map_x_y_ratios(self.c1_w, self.map_h)

        # Format and resize the map image and then draw it on the map canvas
        map_img = cv2.cvtColor(temp_map_img, cv2.COLOR_BGR2RGB)
        resize_map = cv2.resize(map_img, ((int(c.width * .67)), int(self.map_h)))
        new_map = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resize_map))
        self.map_canvas.create_image(int(c.width * .67) / 2, int(self.map_h) / 2, image=new_map)

        self.map_image = new_map

    def update_images(self):
        # Delete the old images
        fih.delete_images(c.cleanup_directory)

        # Create and save the new images - by timestamp
        fih.save_images(c.timestamp, c.cleanup_directory)

        print("timestamp: ", c.timestamp)

        # Load and draw the new images to the gui
        self.load_and_draw_images(c.cleanup_directory)

    def load_and_draw_images(self, path):
        # Load the images
        img1 = cv2.cvtColor(cv2.imread(path + "/image_1.png"), cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(cv2.imread(path + "/image_2.png"), cv2.COLOR_BGR2RGB)
        img3 = cv2.cvtColor(cv2.imread(path + "/image_3.png"), cv2.COLOR_BGR2RGB)

        # Remove anything that may have been on the image canvases
        #self.img1_canvas.delete(ALL)
        #self.img2_canvas.delete(ALL)
        #self.img3_canvas.delete(ALL)

        # Resize the images and draw them on the canvas
        # Image 1
        resize_img1 = cv2.resize(img1, ((int(c.width * c.c2_width_ratio)), int(c.height * c.img_height_ratio)))
        new_img1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resize_img1))
        self.img1_canvas.create_image(((int(c.width * c.c2_width_ratio) / 2),
                                                int(c.height * c.img_height_ratio) / 2), image=new_img1)
        # Image 2
        resize_img2 = cv2.resize(img2, ((int(c.width * c.c2_width_ratio)), int(c.height * c.img_height_ratio)))
        new_img2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resize_img2))
        self.img2_canvas.create_image(((int(c.width * c.c2_width_ratio) / 2),
                                                int(c.height * c.img_height_ratio) / 2), image=new_img2)
        # Image 3
        resize_img3 = cv2.resize(img3, ((int(c.width * c.c2_width_ratio)), int(c.height * c.img_height_ratio)))
        new_img3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resize_img3))
        self.img3_canvas.create_image(((int(c.width * c.c2_width_ratio) / 2),
                                                int(c.height * c.img_height_ratio) / 2), image=new_img3)

        self.store_image_1 = new_img1
        self.store_image_2 = new_img2
        self.store_image_3 = new_img3

    #region ### Mouse and keyboard operations ###

    def mouse_click(self, event):
        # Find the timestamp
        timestamp_ops.find_timestamp(event.x, event.y)

        # Update the images
        self.update_images()

    def arrow_left(self, event):
        # Update the timestamp
        c.timestamp = c.timestamp - 1

        # Update the images
        self.update_images()

    def arrow_right(self, event):
        # Update the timestamp
        c.timestamp = c.timestamp + 1

        # Update the images
        self.update_images()

    def arrow_up(self, event):
        # Update the timestamp
        c.timestamp = c.timestamp + 10

        # Update the images
        self.update_images()

    def arrow_down(self, event):
        # Update the timestamp
        c.timestamp = c.timestamp - 10

        # Update the images
        self.update_images()

    #endregion

    def set_key_bindings(self):
        # Button bindings used to traverse the .avi file via the map
        # Bind the left and right arrow keys to the window to allow the user to go one frame further or one frame back
        self.map_canvas.bind("<Left>", self.arrow_left)
        self.map_canvas.bind("<Right>", self.arrow_right)

        # Bind the up and down arrow keys to the window to allow the user to go 10 frames further or backwards
        self.map_canvas.bind("<Up>", self.arrow_up)
        self.map_canvas.bind("<Down>", self.arrow_down)

    def set_button_bindings(self):
        # Key bindings used to traverse the .avi file via the map (may add additional functionality later on
        # Bind the mouse click event to the map_canvas, this allows the user to click on the map and get the pixel
        # coordinates of the point clicked
        self.map_canvas.bind("<Button-1>", self.mouse_click)
