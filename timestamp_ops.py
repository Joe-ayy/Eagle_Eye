import config


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
    map_x_meters = actual_map_x * config.p2m
    map_y_meters = actual_map_y * config.p2m

    # Package as a list
    map_coords_meters = [map_x_meters, map_y_meters]

    return map_coords_meters


def find_timestamp(x, y, ratio_x, ratio_y, x_offset, y_offset, trajectory_list):
    # Get the x and y coordinates in meters
    map_x_y_meters = convert_pixel_location([x, y], ratio_x, ratio_y)

    print("Map x (meters): ", map_x_y_meters[0], "Map y (meters): ", map_x_y_meters[1])

    # Subtract the offset to the coordinates
    map_x_y_meters[0] = map_x_y_meters[0] - x_offset * config.p2m
    map_x_y_meters[1] = map_x_y_meters[1] - y_offset * config.p2m

    # Loop through the trajectory list
    for i in range(0, len(trajectory_list)):
        x_val = float(trajectory_list[i][0])
        y_val = float(trajectory_list[i][1])

        if (abs(x_val - map_x_y_meters[0]) < .5) and (abs(y_val - map_x_y_meters[1]) < .5):
            timestamp = int(round(float(trajectory_list[i][2]), 0))
            return timestamp

    # Temporary fix, just return 1 as the timestamp
    return -1