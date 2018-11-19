import cv2
import re
import os


class LoadAviImages:
    # Create a dictionary to hold the timestamp and the image
    avi_images = {}

    def __init__(self, path):
        # When the class is initialized, create and fill a dictionary
        # Define the path to the .avi file
        avi_dir = path + '/'

        # Initialize the .avi filename
        avi_name = ""

        # Initialize the timestamp
        timestamp = 0

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
                    self.avi_images[timestamp] = image
                    print("Image obtained, timestamp: ", timestamp)
                else:
                    break

                # Increment the timestamp
                timestamp = timestamp + 1

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