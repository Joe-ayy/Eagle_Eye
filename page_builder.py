import cv2
import sys
import config as c
import file_handler as fh
import timestamp_ops as t_ops
from tkinter import *
from gui_builder import *
from PIL import ImageTk, Image


# Class used to build a map viewing page
class AppPage:
    # region ### Initialize Objects to prevent garbage collection ###
    map_image = None
    temp_img = None
    store_img1 = None
    store_img2 = None
    store_img3 = None
    park_position = None
    dock_position = None
    trail_position = [None, None, None]
    user_position = None
    #endregion

    # region ### Initialize values for canvas height and widths ###
    canvas_dim_store_images = [0, 0]  # [width, height]
    canvas_dim_map_image = [0, 0]     # [width, height]
    #endregion

    # region ### Create objects to traverse data ###
    avi_data = None
    trajectory_data = None
    #endregion

    # region ### Initialize path variables for files ###
    directory_path = ""
    map_file = ""
    info_file = ""
    trajectory_file = ""
    #endregion

    # region ### Initialize map related data ###
    # Initialize the map ratio
    map_ratio_x = 0.0  # Calculated as original map width / current displayed map width
    map_ratio_y = 0.0  # Calculated as original map height / current displayed map width

    # Save the original map dimensions
    orig_map_w = 0
    orig_map_h = 0

    # Initialize offset values
    x_offset = 0
    y_offset = 0
    #endregion

    # Initialize the timestamp
    timestamp = 1

    def __init__(self, win_title, win_width, win_height, path, loaded_file_paths):
        # Construct the window
        self.page_window = BuildWindow(win_title, win_width, win_height, True, True)

        # region ### Construct and place canvases ###
        # Construct the canvases
        self.map_canvas = Canvas(self.page_window, bg="blue")
        self.img1_canvas = Canvas(self.page_window, bg="red")
        self.img2_canvas = Canvas(self.page_window, bg="pink")
        self.img3_canvas = Canvas(self.page_window, bg="yellow")

        # Place the canvases
        self.map_canvas.place(anchor=NW, relheight=c.map_height_ratio, relwidth=c.c1_width_ratio)
        self.img1_canvas.place(anchor=NE, relheight=c.img_height_ratio, relwidth=c.c2_width_ratio,
                               relx=1)
        self.img2_canvas.place(anchor=NE, relheight=c.img_height_ratio, relwidth=c.c2_width_ratio,
                               relx=1, rely=c.img_height_ratio)
        self.img3_canvas.place(anchor=NE, relheight=c.img_height_ratio, relwidth=c.c2_width_ratio,
                               relx=1, rely=(c.img_height_ratio * 2))
        #endregion

        # region ### Retrieve and store information obtained from files ###
        store_info = fh.get_store_info(path)

        self.directory_path = path
        self.map_file = loaded_file_paths[0]
        self.info_file = loaded_file_paths[1]
        self.trajectory_file = loaded_file_paths[2]

        # Create data structures for the .avi and the trajectory file
        self.avi_data = fh.LoadAviImages(self.directory_path)
        self.trajectory_data = fh.LoadTrajectoryData(self.trajectory_file)

        # Save unmodified trajectory file to determine park and dock coordinates
        self.orig_trajectory_data = self.trajectory_data.list_data

        # Bound the trajectory data with a predetermined offset to the length of the .avi file
        self.trajectory_data.list_data = t_ops.format_trajectory_data(self.trajectory_data.list_data,
                                                                      self.avi_data.num_frames)

        # Set the offset values
        self.x_offset, self.y_offset = t_ops.get_offsets(self.info_file)

        # Set the original map height and width
        self.orig_map_h, self.orig_map_w, _ = cv2.imread(self.map_file).shape
        #endregion

        # region ### Construct and place labels
        # Construct the labels
        self.map_name_label = BuildStaticLabel(self.page_window, "Map: " + store_info, W, 14)
        self.timestamp_label_text = StringVar()
        self.timestamp_label_text.set("Timestamp: " + str(self.timestamp))
        self.timestamp_label = Label(self.page_window, textvariable=self.timestamp_label_text,
                                     font=("Times New Roman", 14), relief=RIDGE, padx=3, bg="light steel blue")

        # Place the labels
        self.map_name_label.place(rely=c.map_height_ratio)
        self.timestamp_label.place(rely=c.map_height_ratio + .035)
        #endregion

        # region ### Set the initial canvas height and widths ###
        self.canvas_dim_store_images[0] = self.img1_canvas.winfo_width()
        self.canvas_dim_store_images[1] = self.img1_canvas.winfo_height()
        self.canvas_dim_map_image[0] = self.map_canvas.winfo_width()
        self.canvas_dim_map_image[1] = self.map_canvas.winfo_height()
        #endregion

        # region ### Start the application by initializing data upon startup ###
        # Set the focus to the window and the map canvas to use keybindings
        self.page_window.focus_set()
        self.map_canvas.focus_set()

        # Set the bindings and display the images and map from the beginning of the .avi file
        self.set_bindings()
        self.draw_map()
        self.update_images()
        #endregion

    def draw_map(self):
        # Save the information for the map
        temp_map_img = cv2.imread(self.map_file)

        # Set the x and y map ratios
        self.map_ratio_x, self.map_ratio_y = t_ops.set_map_x_y_ratios(self.orig_map_w, self.orig_map_h,
                                                                      self.canvas_dim_store_images[0],
                                                                      self.canvas_dim_store_images[1])
        # Format and resize the map image and draw it on map canvas
        new_map = self.resize_image(self.canvas_dim_map_image[0], self.canvas_dim_map_image[1], temp_map_img)

        # Get the mid point of the map canvas to draw the map
        mid_x = int(self.canvas_dim_map_image[0] / 2)
        mid_y = int(self.canvas_dim_map_image[1] / 2)

        self.map_canvas.create_image((mid_x, mid_y), image=new_map)
        self.map_image = new_map

        self.draw_p_and_d()

    def draw_p_and_d(self):
        # Get the park x and y coordinates
        px_position, py_position = t_ops.find_xy_in_pixels(0, self.map_ratio_x, self.map_ratio_y,
                                                           self.x_offset, self.y_offset, self.orig_trajectory_data)

        # Get the timestamp for the dock location
        dock_ts = self.orig_trajectory_data[-1][2]

        # Get the dock x and y coordinates
        dx_position, dy_position = t_ops.find_xy_in_pixels(dock_ts, self.map_ratio_x, self.map_ratio_y,
                                                           self.x_offset, self.y_offset, self.orig_trajectory_data)

        # Find the bounds for the circles for the dock and park
        top_x_p = int(px_position - (.25 / c.m2p))
        top_y_p = int(py_position - (.25 / c.m2p))
        bot_x_p = int(px_position + (.25 / c.m2p))
        bot_y_p = int(py_position + (.25 / c.m2p))

        top_x_d = int(dx_position - (.25 / c.m2p))
        top_y_d = int(dy_position - (.25 / c.m2p))
        bot_x_d = int(dx_position + (.25 / c.m2p))
        bot_y_d = int(dy_position + (.25 / c.m2p))

        # Draw the park and dock circles
        dock_circle = self.map_canvas.create_oval(top_x_d, top_y_d, bot_x_d, bot_y_d, fill="blue")
        park_circle = self.map_canvas.create_oval(top_x_p, top_y_p, bot_x_p, bot_y_p, fill="red")

        # Save the dock and park objects from garbage collection
        self.dock_position = dock_circle
        self.park_position = park_circle

    def draw_position(self, ts, modifier, color):
        # Get the x, y coordinate pair based on the timestamp to determine the location to draw the circle
        x_position, y_position = t_ops.find_xy_in_pixels(ts, self.map_ratio_x, self.map_ratio_y,
                                                         self.x_offset, self.y_offset, self.trajectory_data.list_data)

        # Determine the top left and bottom right coordinates for the circle
        top_x = int(x_position - (modifier / c.m2p))
        top_y = int(y_position - (modifier / c.m2p))
        bot_x = int(x_position + (modifier / c.m2p))
        bot_y = int(y_position + (modifier / c.m2p))

        user_circle = self.map_canvas.create_oval(top_x, top_y, bot_x, bot_y, fill=color)

        return user_circle

    def draw_trail(self):
        # Only add a trail to user's current position if they have been at a minimum of 4 previous positions
        if self.timestamp > 3:
            self.trail_position[2] = self.draw_position(self.timestamp - 4, .10, "pink")
            self.trail_position[1] = self.draw_position(self.timestamp - 3, .15, "pink")
            self.trail_position[0] = self.draw_position(self.timestamp - 2, .25, "pink")

    def del_old_position(self):
        # Attempt to delete the user and trail positions
        try:
            self.map_canvas.delete(self.user_position)
            self.map_canvas.delete(self.trail_position[0])
            self.map_canvas.delete(self.trail_position[1])
            self.map_canvas.delete(self.trail_position[2])
        except:
            return

    def update_images(self):
        # Attempt to delete the old positions
        self.del_old_position()

        # Draw the user's current position and the trail of previous positions
        self.draw_trail()
        self.user_position = self.draw_position(self.timestamp, .4, "orange")

        # Update the timestamp label
        self.update_timestamp_label()

        # Load and draw the new images to the gui
        self.load_and_draw_images()

    def update_timestamp_label(self):
        # Change the timestamp label
        self.timestamp_label_text.set("Timestamp: " + str(self.timestamp))

    def load_and_draw_images(self):
        # Assign the images based on the timestamp
        img1, img2, img3 = self.avi_data.get_3_images(self.timestamp)

        # Determine the center of the image canvas
        mid_x = int(self.canvas_dim_store_images[0] / 2)
        mid_y = int(self.canvas_dim_store_images[1] / 2)

        # Resize the images and draw them on the canvas
        # Image 1
        new_img1 = self.resize_image(self.canvas_dim_store_images[0], self.canvas_dim_store_images[1], img1)
        self.img1_canvas.create_image((mid_x, mid_y), image=new_img1)

        # Image 2
        new_img2 = self.resize_image(self.canvas_dim_store_images[0], self.canvas_dim_store_images[1], img2)
        self.img2_canvas.create_image((mid_x, mid_y), image=new_img2)

        # Image 3
        new_img3 = self.resize_image(self.canvas_dim_store_images[0], self.canvas_dim_store_images[1], img3)
        self.img3_canvas.create_image((mid_x, mid_y), image=new_img3)

        self.store_img1 = new_img1
        self.store_img2 = new_img2
        self.store_img3 = new_img3

    def set_bindings(self):
        # Button bindings used to travers the .avi file on following the user position on the map
        # Bind the left and right arrow keys to the window to allow the user to go 2 frames forward or backwards
        self.map_canvas.bind("<Left>", self.arrow_left)
        self.map_canvas.bind("<Right>", self.arrow_right)

        # Bind the up and down arrow keys to the window to allow the user to go 10 frames forward or backward
        self.map_canvas.bind("<Up>", self.arrow_up)
        self.map_canvas.bind("<Down>", self.arrow_down)

        # Bind the mouse click event to the window, this allows the user to click on the map and get coordinates
        # of the point clicked
        self.map_canvas.bind("<Button-1>", self.mouse_click)

        # Bind the window resizing event
        self.page_window.bind("<Configure>", self.configure)

        # Bind the window close event (x in the top right corner)
        self.page_window.protocol("WM_DELETE_WINDOW", self.quit_program)

    def configure(self, event):
        # Update the size of the canvas to the current size based on the resizing window event
        self.canvas_dim_store_images[0] = event.width
        self.canvas_dim_store_images[1] = event.height

        # Redraw all the objects on the screen
        self.draw_map()
        self.update_images()

    # region ### Mouse, Keyboard, and Window Manipulation Operations ###
    def arrow_left(self, event):
        # Update the timestamp
        if self.timestamp > 2:
            self.timestamp = self.timestamp - 2

        # Update the images
        self.update_images()

    def arrow_right(self, event):
        # Update the timestamp
        if self.timestamp < self.avi_data.num_frames - 3:
            self.timestamp = self.timestamp + 2

        # Update the images
        self.update_images()

    def arrow_up(self, event):
        # Update the timestamp
        if self.timestamp < self.avi_data.num_frames - 11:
            self.timestamp = self.timestamp + 10

        # Update the images
        self.update_images()

    def arrow_down(self, event):
        # Update the timestamp
        if self.timestamp > 10:
            self.timestamp = self.timestamp - 10

        # Update the images
        self.update_images()

    def mouse_click(self, event):
        # Find the timestamp for the click event
        temp_timestamp = t_ops.find_timestamp(event.x, event.y,
                                              self.map_ratio_x, self.map_ratio_y, self.x_offset, self.y_offset,
                                              self.trajectory_data.list_data)
        # Only change the timestamp and update the window elements if a valid timestamp is found
        if temp_timestamp != -1:
            self.timestamp = temp_timestamp

            # Update the images
            self.update_images()
    #endregion

    def quit_program(self):
        self.page_window.destroy()
        sys.exit()

    @staticmethod
    def resize_image(width, height, img):
        resize_map = cv2.resize(img, (width, height), cv2.INTER_AREA)
        new_map = ImageTk.PhotoImage(image=Image.fromarray(resize_map))
        return new_map
