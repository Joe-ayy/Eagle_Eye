import cv2
import sys
from tkinter import *
import PIL.Image
import PIL.ImageTk
import numpy as np
from gui_builder import *
from file_handler import *
import file_handler as fh
import timestamp_ops as t_ops
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

    # region ### Initialize data and objects ###
    # Save and update ratios and original map dimensions
    map_ratio_x = 0.0  # Calculated as original map width / displayed map width
    map_ratio_y = 0.0  # Calculated as original map height / displayed map height

    orig_map_w = 0  # Original map width
    orig_map_h = 0  # Original map height

    # Hold on to the values for the images and objects so they are not garbage collected
    map_image = None
    user_position = None
    store_image_1 = None
    store_image_2 = None
    store_image_3 = None

    # Save the directory path to be used by class
    directory_path = ""

    # Create the object used to traverse the data structure used for the .avi file
    avi_data = None

    # Create the object used to traverse the data structure used for the trajectory file
    trajectory_data = None

    # Initialize the paths for the map, info, and trajectory files
    map_file = ""
    info_file = ""
    trajectory_file = ""

    # Initialize offset values
    x_offset = 0
    y_offset = 0

    # Initialize the timestamp to 1
    timestamp = 1
    #endregion

    def __init__(self, path, loaded_file_paths):
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
        self.map_canvas = BuildCanvas(self.map_con, self.c1_w, self.map_h, NW)  # Map Canvas

        self.img1_canvas = BuildCanvas(self.img1_con, MainPage.img_w, MainPage.img_h, NW)  # Image 1 Canvas
        self.img2_canvas = BuildCanvas(self.img2_con, MainPage.img_w, MainPage.img_h, NW)  # Image 2 Canvas
        self.img3_canvas = BuildCanvas(self.img3_con, MainPage.img_w, MainPage.img_h, NW)  # Image 3 Canvas
        #endregion

        # Get the store's name and number - used to display in a label
        store_info = fh.get_store_info(path)

        #region ### Construct and display labels ###
        self.map_name_label = BuildStaticLabel(self.util_con, "Map: " + store_info, NW, 14)
        self.timestamp_label_text = StringVar()
        self.timestamp_label_text.set("Timestamp: " + str(self.timestamp))

        self.timestamp_label = Label(self.util_con, textvariable=self.timestamp_label_text,
                                     font=("Times New Roman", 14), relief=RIDGE, padx=3, bg="light steel blue")
        self.timestamp_label.pack(anchor=SW)
        #endregion

        # Set the focus to the window and the map canvas for keybindings
        self.app_window.focus_set()
        self.map_canvas.focus_set()

        # region ### Set values for files and initialized variables belonging to MainPage ###
        # Set the directory path
        self.directory_path = path

        # Set the values for the paths to the map, info, and trajectory files
        self.map_file = loaded_file_paths[0]
        self.info_file = loaded_file_paths[1]
        self.trajectory_file = loaded_file_paths[2]

        # Create the .avi data structure
        self.avi_data = fh.LoadAviImages(path)

        # Create the trajectory file data structure
        self.trajectory_data = fh.LoadTrajectoryData(self.trajectory_file)

        # Set the offset values
        self.x_offset, self.y_offset = t_ops.get_offsets(self.info_file)
        #endregion

    def draw_map(self):
        # Save the information for the map, this will be used to change variable values
        temp_map_img = cv2.imread(self.map_file)
        self.orig_map_h, self.orig_map_w, _ = temp_map_img.shape  # Can probably sneak this into this class

        # Set the x and y map ratios
        self.map_ratio_x, self.map_ratio_y = t_ops.set_map_x_y_ratios(self.orig_map_w, self. orig_map_h,
                                                                      self.c1_w, self.map_h)

        # Format and resize the map image and then draw it on the map canvas
        map_img = cv2.cvtColor(temp_map_img, cv2.COLOR_BGR2RGB)
        resize_map = cv2.resize(map_img, ((int(c.width * .67)), int(self.map_h)))
        new_map = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(resize_map))
        self.map_canvas.create_image(int(c.width * .67) / 2, int(self.map_h) / 2, image=new_map)

        self.map_image = new_map

    def draw_position(self):
        # Try to delete the circle before drawing a new one
        try:
            self.map_canvas.delete(self.user_position)
        except:
            pass

        # Get an x,y coordinate pair based on the timestamp to determine the location to draw the circle
        x_position, y_position = t_ops.find_xy_in_pixels(self.timestamp, self.map_ratio_x, self.map_ratio_y,
                                                     self.x_offset, self.y_offset, self.trajectory_data.list_data)

        # Determine the top left and bottom right coordinates for the circle
        top_x = int(x_position - (.4 / c.m2p))
        top_y = int(y_position - (.4 / c.m2p))
        bot_x = int(x_position + (.4 / c.m2p))
        bot_y = int(y_position + (.4 / c.m2p))

        #print("Bounding box: ", top_x, top_y, "|", bot_x, bot_y)

        user_circle = self.map_canvas.create_oval(top_x, top_y, bot_x, bot_y, fill="orange")

        self.user_position = user_circle

    def update_images(self):
        # Print out the timestamp - debugging purposes
        print("timestamp: ", self.timestamp)

        self.draw_position()
        self.update_timestamp_label()

        # Load and draw the new images to the gui
        self.load_and_draw_images()

    def update_timestamp_label(self):
        # Change the time stamp label text
        self.timestamp_label_text.set("Timestamp: " + str(self.timestamp))

    def load_and_draw_images(self):
        # Assign the images based on the timestamp
        img1, img2, img3 = self.avi_data.get_3_images(self.timestamp)

        # Resize the images and draw them on the canvas
        #  Image 1
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
        temp_timestamp = t_ops.find_timestamp(event.x, event.y,
                                              self.map_ratio_x, self.map_ratio_y, self.x_offset, self.y_offset,
                                              self.trajectory_data.list_data)
        # Only change the timestamp and update the window elements if a valid one is found
        if temp_timestamp != -1:
            self.timestamp = temp_timestamp

            # Update the images
            self.update_images()

    def arrow_left(self, event):
        # Update the timestamp
        if self.timestamp > 2:
            self.timestamp = self.timestamp - 2

        # Update the images
        self.update_images()

    def arrow_right(self, event):
        # Update the timestamp
        if self.timestamp < self.avi_data.num_frames - 2:
            self.timestamp = self.timestamp + 2

        # Update the images
        self.update_images()

    def arrow_up(self, event):
        # Update the timestamp
        if self.timestamp < self.avi_data.num_frames - 10:
            self.timestamp = self.timestamp + 10

        # Update the images
        self.update_images()

    def arrow_down(self, event):
        # Update the timestamp
        if self.timestamp > 10:
            self.timestamp = self.timestamp - 10

        # Update the images
        self.update_images()

    #endregion

    def quit_program(self):
        sys.exit()

    def set_key_bindings(self):
        # Button bindings used to traverse the .avi file via the map
        # Bind the left and right arrow keys to the window to allow the user to go one frame further or one frame back
        self.map_canvas.bind("<Left>", self.arrow_left)
        self.map_canvas.bind("<Right>", self.arrow_right)

        # Bind the up and down arrow keys to the window to allow the user to go 10 frames further or backwards
        self.map_canvas.bind("<Up>", self.arrow_up)
        self.map_canvas.bind("<Down>", self.arrow_down)

        # Bind the window close event (x in top right corner)
        self.app_window.protocol("WM_DELETE_WINDOW", self.quit_program)

    def set_button_bindings(self):
        # Key bindings used to traverse the .avi file via the map (may add additional functionality later on
        # Bind the mouse click event to the map_canvas, this allows the user to click on the map and get the pixel
        # coordinates of the point clicked
        self.map_canvas.bind("<Button-1>", self.mouse_click)
