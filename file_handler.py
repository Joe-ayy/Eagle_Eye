import cv2
import re
import os


class LoadAviImages:
    # Create a dictionary to hold the timestamp and the image
    avi_images = {}

    # Initialize timestamp to count how many seconds long the .avi file is (1 frame = 1 second)
    timestamp = 0

    def __init__(self, path):
        # When the class is initialized, create and fill a dictionary
        # Define the path to the .avi file
        avi_dir = path + '/'

        # Initialize the .avi filename
        avi_name = ""

        # Find the .avi file in the directory using a regular expression
        for file in os.listdir(avi_dir):
            match_found = re.match(r'.*?.avi', file)
            if match_found:
                avi_name = file
                break

        # If the .avi file isn't found, do something...
        if avi_name == "":
            print(".avi file not found!")
        else:
            # .avi file full path
            avi_full_path = avi_dir + avi_name

            # Open the .avi file
            avi_file = cv2.VideoCapture(avi_full_path)

            # Read each frame in the video until it is complete
            while avi_file.isOpened():
                # Obtain each image
                ret, image = avi_file.read()

                # If the frame of the video (the image) returns correctly, add it to the list
                if ret:
                    self.avi_images[self.timestamp] = image
                    print("Image obtained, timestamp: ", self.timestamp)
                else:
                    break

                # Increment the timestamp
                self.timestamp = self.timestamp + 1

            # Release the VideoCapture object
            avi_file.release()

    def get_3_images(self, timestamp):
        # Initialize 3 images
        image_1 = None
        image_2 = None
        image_3 = None

        # Iterate until the timestamp is reached, then access the image at the timestamp store in the dictionary
        for i in range(0, timestamp + 2):
            # Create the 3 images based on the time stamp
            if (timestamp - i) == 1:
                image_1 = self.avi_images[timestamp]
            elif (timestamp - i) == 0:
                image_2 = self.avi_images[timestamp]
            elif (timestamp - i) == -1:
                image_3 = self.avi_images[timestamp]

        return image_1, image_2, image_3


class LoadTrajectoryData:
    # Create a list to hold the x, y, and the timestamp
    list_data = []

    def __init__(self, path):
        # Open the trajectory file
        file = open(path, 'r')

        # Read the first 14 lines, with the 15th line being the first data entry in the file
        for i in range(0, 15):
            line = file.readline()

        # Loop through the trajectory file until the eof has been reached
        while not line.isspace():
            data_list = line.split(' ')

            # The data_list list has 8 components, they are as follows:
            # data_list[0] = float x, data_list[1] = float y, data_list[2] = float z, data_list[3] = float roll
            # data_list[4] = float pitch, data_list[5] = float yaw
            # data_list[6] = float time, data_list[7] = float scm

            try:
                x_val = float(data_list[0])
                y_val = float(data_list[1])
                timestamp = int(round(float(data_list[6]), 0))
            except ValueError:
                break

            # Save the data to the list
            self.list_data.append([x_val, y_val, timestamp])

            # Read in the next line
            line = file.readline()

        # Close the file
        file.close()


class FilePathHandler:
    # Initialize the files needed for the application
    map_file_path = ""
    info_file_path = ""
    trajectory_file_path = ""

    def __init__(self, path):  # This should automatically get the full file paths for the map, info, traj files
        # Initialize variables to hold file names
        map_file = ""
        info_file = ""
        trajectory_file = ""

        # Look through the files in the directory to try to find each of the files required
        for file in os.listdir(path):
            map_match_found = re.match(r'.*?.png', file)
            info_match_found = re.match(r'.*?.info', file)
            trajectory_match_found = re.match(r'.*?.ply', file)

            # Check to see if any of the files are found for each pass through the directory
            # If they are found, assign them to their proper variable
            if map_match_found:
                map_file = file
            elif info_match_found:
                info_file = file
            elif trajectory_match_found:
                trajectory_file = file

        # Create and assign the path to the files
        if map_file == "":
            self.map_file_path = path
        else:
            self.map_file_path = path + '/' + map_file
        if info_file == "":
            self.info_file_path = path
        else:
            self.info_file_path = path + '/' + info_file
        if trajectory_file == "":
            self.trajectory_file_path = path
        else:
            self.trajectory_file_path = path + '/' + trajectory_file

    # If there is a problem getting the map path, this allows the user/app to try a different directory
    def set_map_path(self, path):
        # Find the store map (should be the only .png file in the directory)
        map_file = ""

        # Look through the files in the directory to try to find the store map
        for file in os.listdir(path):
            match_found = re.match(r'.*?.png', file)
            if match_found:
                map_file = file
                break

        # Create and assign the path to the file
        if map_file == "":
            self.map_file_path = path
        else:
            self.map_file_path = path + '/' + map_file

    # If there is a problem getting the info file path, this allows the user/app to try a different directory
    def set_info_path(self, path):
        # Find the .info file (should be the only .info file in the directory)
        info_file = ""

        # Look through the files in the directory to try to find the .info file
        for file in os.listdir(path):
            match_found = re.match(r'.*?.info', file)
            if match_found:
                info_file = file
                break

        # Create and assign the path to the file
        if info_file == "":
            self.info_file_path = path
        else:
            self.map_file_path = path + '/' + info_file

    # If there is a problem getting the trajectory file path, this allows the user/app to try a different directory
    def set_trajectory_path(self, path):
        # Find the trajectory file (should be the only .ply file in the directory)
        trajectory_file = ""

        # Look through the files in the directory to try to find the trajectory file
        for file in os.listdir(path):
            match_found = re.match(r'.*?.ply', file)
            if match_found:
                trajectory_file = file
                break

        # Create and assign the path to the file
        if trajectory_file == "":
            self.trajectory_file_path = path
        else:
            self.trajectory_file_path = path + '/' + trajectory_file


def get_store_info(path):
    # Look at the path name and find the store name from the directory
    store_name_start_pos = path.find(r'Documents')
    store_name_start_pos = store_name_start_pos + len("Documents") + 1

    # Save the short hand for the store name and number
    store_acronym = path[store_name_start_pos:]

    # Determine if the store is a Stop & Shop or Giant Martin
    if store_acronym[:3].upper() == "SNS":
        store_name = "Stop & Shop "

        # Parse out the store number
        store_number = store_acronym[3:]

    elif store_acronym[:2].upper() == "GM":
        store_name = "Giant Martin "

        # Parse out the store number
        store_number = store_acronym[2:]

    else:
        store_name = "Unknown Store "
        store_number = ""

    return store_name + store_number
