import cv2
import re
import os
import numpy as np
import config


# This module takes the timestamp found from <insert filename here>.py and uses it to find the frames in the .avi file
# to save to a temporary directory

# This function navigates to the desired directory that contains the .avi file and saves up to 3 images in that same
# directory
def save_images(timestamp, dir_path):
    # Define the path to the .avi file
    avi_dir = dir_path + '/'

    # Initialize the .avi filename
    avi_name = ""

    # Find the .avi file in the directory using a regular expression
    for file in os.listdir(avi_dir):
        match_found = re.match(r'.*?.avi', file)
        if match_found:
            avi_name = file
            break

    # If the .avi file is not found, problem will have to be handled by what called this function
    if avi_name == "":
        return 1

    # .avi full file path
    avi_full_path = avi_dir + avi_name

    # Open the .avi file
    avi_file = cv2.VideoCapture(avi_full_path)

    #region ### Save 3 frames from the .avi ###
    # Read the .avi file until 1 second after the timestamp - This provides a frame at the timestamp and frames
    # 1 second before and after the timestamp
    for i in range(0, timestamp + 2):
        ret, image = avi_file.read()

        if ((timestamp - i) == 1) and ret:
            cv2.imwrite(avi_dir + "image_1.png", image)

        elif ((timestamp - i) == 0) and ret:
            cv2.imwrite(avi_dir + "image_2.png", image)

        elif ((timestamp - i) == -1) and ret:
            cv2.imwrite(avi_dir + "image_3.png", image)

    #endregion

    # Release the VideoCapture object
    avi_file.release()

    # Return to the main function
    return 0


def get_map_path(path):
    # Find the store map (should be the only .png file in the directory)
    map_file = ""

    # Look through the files in the directory to try to find the store map
    for file in os.listdir(path):
        match_found = re.match(r'.*?.png', file)
        if match_found:
            map_file = file
            break

    # Return the original path if the store map isn't found, this will be handled by the calling function
    if map_file == "":
        return path
    else:
        map_full_path = path + '/' + map_file
        return map_full_path


def get_info_path(path):
    # Find the .info file (should be the only .info file in the directory)
    info_file = ""

    # Look through the files in the directory to try to find the .info file
    for file in os.listdir(path):
        match_found = re.match(r'.*?.info', file)
        if match_found:
            info_file = file
            break

    # Return the original path if the .info file isn't found, this will be handled by the calling function
    if info_file == "":
        return path
    else:
        info_full_path = path + '/' + info_file
        return info_full_path


def get_trajectory_path(path):
    # Find the trajectory file (should be the only .ply file in the directory)
    trajectory_file = ""

    # Look through the files in the directory to try to find the trajectory file
    for file in os.listdir(path):
        match_found = re.match(r'.*?.ply', file)
        if match_found:
            trajectory_file = file
            break

    # Return the original path if the trajectory file isn't found, this will be handled by the calling function
    if trajectory_file == "":
        config.traj_file = trajectory_file
    else:
        trajectory_full_path = path + '/' + trajectory_file
        config.traj_file = trajectory_full_path


# This function checks the .avi directory (where the images are temporarily saved) and deletes all the image_#.png files
# if they are there
def delete_images(dir_path):
    # Try to delete the 3 image files if they exist
    try:
        os.remove(dir_path + "/image_1.png")
    except OSError:
        print("Can't delete image_1.png")
    try:
        os.remove(dir_path + "/image_2.png")
    except OSError:
        print("Can't delete image_2.png")
    try:
        os.remove(dir_path + "/image_3.png")
    except OSError:
        print("Can't delete image_3.png")
