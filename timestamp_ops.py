import config
import math


def get_offsets(offset_file):
    # Open the file for reading and read a line
    file = open(offset_file, 'r')
    line = file.readline()

    # Read 5 more lines, this will stop on the line that contains the desired x and y offsets
    for i in range(0, 5):
        line = file.readline()

    # Locate the position of x and y based on the first instance of the character :
    x_start_pos = line.find(": ")
    y_start_pos = line.find(' ', x_start_pos + 2)
    y_end_pos = line.find('\n', y_start_pos + 1)

    # Close the file
    file.close()

    x_offset = int(line[x_start_pos + 2: y_start_pos])
    y_offset = int(line[y_start_pos + 1: y_end_pos])

    return x_offset, y_offset


def set_map_x_y_ratios(orig_w, orig_h, resize_x, resize_y):
    # Set the ratio values in the config file - May need to be adjusted later on depending on program functionality
    map_ratio_x = orig_w / resize_x
    map_ratio_y = orig_h / resize_y

    return map_ratio_x, map_ratio_y


def convert_pixel_location(gui_map_coords, map_ratio_x, map_ratio_y):
    # Convert the pixel location (x, y) in the resized map in the gui to the actual (x, y) in the original store map
    gui_map_x = int(gui_map_coords[0])
    gui_map_y = int(gui_map_coords[1])

    # Switch the origin from top left to bottom left
    gui_map_y = (config.height * config.map_height_ratio) - gui_map_y

    # Round the floating pixel values using int
    actual_map_x = int(gui_map_x * map_ratio_x)
    actual_map_y = int(gui_map_y * map_ratio_y)

    # Convert the new pixel values to meters
    map_x_meters = actual_map_x * config.m2p
    map_y_meters = actual_map_y * config.m2p

    # Package as a list
    map_coords_meters = [map_x_meters, map_y_meters]

    return map_coords_meters


def find_timestamp(x, y, ratio_x, ratio_y, x_offset, y_offset, trajectory_list):
    # Get the x and y coordinates in meters
    map_x_y_meters = convert_pixel_location([x, y], ratio_x, ratio_y)

    # Debugging purposes
    print("Map x (meters): ", map_x_y_meters[0], "Map y (meters): ", map_x_y_meters[1])

    # Subtract the offset to the coordinates
    map_x_y_meters[0] = map_x_y_meters[0] - x_offset * config.m2p
    map_x_y_meters[1] = map_x_y_meters[1] - y_offset * config.m2p

    # Loop through the trajectory list
    for i in range(0, len(trajectory_list)):
        x_val = float(trajectory_list[i][0])
        y_val = float(trajectory_list[i][1])

        if (abs(x_val - map_x_y_meters[0]) < .5) and (abs(y_val - map_x_y_meters[1]) < .5):
            timestamp = int(round(float(trajectory_list[i][2]), 0))
            return timestamp

    # Temporary fix, just return -1 as the timestamp
    return -1


def find_xy_in_pixels(timestamp, ratio_x, ratio_y, x_offset, y_offset, trajectory_list):
    # Initialize the x value and y value
    x_val_meters = 0.0
    y_val_meters = 0.0

    # Set a count for how many positions have the same floored timestamp
    num_timestamps = 0

    # Loop through the trajectory list looking for the timestamp, once found, find the midpoint of all timestamps with
    # the same floored value, save the x and y values, and break out of the loop
    for i in range(0, len(trajectory_list)):
        ts_in_list = float(trajectory_list[i][2])
        if timestamp == math.floor(ts_in_list):
            for j in range(0, len(trajectory_list) - i):
                if timestamp == math.floor(trajectory_list[i + j][2]):
                    num_timestamps = num_timestamps + 1
                else:
                    break
            # Set the midpoint for the timestamps
            mid_pt = num_timestamps // 2

            # Assign the value of x and y to the first found position plus the midpoint of the floored timestamps
            x_val_meters = float(trajectory_list[i + mid_pt][0])
            y_val_meters = float(trajectory_list[i + mid_pt][1])
            break

    # Convert the x and y values from meters to pixels
    actual_map_x = x_val_meters / config.m2p
    actual_map_y = y_val_meters / config.m2p

    # Add the offset to the coordinates
    actual_map_x = actual_map_x + x_offset
    actual_map_y = actual_map_y + y_offset

    # Convert the x and y values from actual map pixels to gui sized map pixels
    gui_map_x = actual_map_x / ratio_x
    gui_map_y = actual_map_y / ratio_y

    # Switch the origin from the bottom left to the top right
    gui_map_y = (config.height * config.map_height_ratio) - gui_map_y

    # Convert the values for the gui pixel values to ints and return them
    #print("gui_map_x: ", int(gui_map_x), "gui_map_y: ", int(gui_map_y))
    return int(gui_map_x), int(gui_map_y)


def format_trajectory_data(traj_list_data, avi_length):
    # Create a padding to add to the beginning of the trajectory list data
    padding = []

    for i in range(config.pad_amount):
        padding.append([0, 0, i])

    # Increase the timestamp values of the original trajectory list data by the pad amount
    for j in range(len(traj_list_data)):
        traj_list_data[j][2] = traj_list_data[j][2] + config.pad_amount

    # Pad the trajectory data list at the beginning with the pad amount
    padded_traj_data = padding + traj_list_data

    # Find the ratio of the last timestamp in the trajectory data to the avi file length
    ts_ratio = avi_length / padded_traj_data[-1][2]

    # Apply the ratio to the data
    for k in range(len(padded_traj_data)):
        padded_traj_data[k][2] = padded_traj_data[k][2] * ts_ratio

    return padded_traj_data
