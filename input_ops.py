# Mouse and Keyboard Operations

import config
import timestamp_ops
import file_and_image_handling
import user_gui


def update_images(path, width, height, img1_canvas, img2_canvas, img3_canvas):
    # Delete the old images
    file_and_image_handling.delete_images(config.cleanup_directory)

    print("Timestamp: ", config.timestamp)
    print("Cleanup Directory: ", config.cleanup_directory)

    # Create and save the new images - by timestamp
    file_and_image_handling.save_images(config.timestamp, config.cleanup_directory)

    # Load and draw the new images to the gui
    user_gui.load_and_draw_images(path, width, height, img1_canvas, img2_canvas, img3_canvas)


def mouse_click(event):
    # Find the timestamp
    timestamp_ops.find_timestamp(event.x, event.y)

    # Update the images
    path, width, height, = config.cleanup_directory, config.width * .67, config.height * .9
    img1_canvas, img2_canvas, img3_canvas = 1, 2, 3
    update_images(path, width, height, img1_canvas, img2_canvas, img3_canvas)


def arrow_left(event):
    # Update the timestamp
    config.timestamp = config.timestamp - 1

    # Update the images
    update_images()


def arrow_right(event):
    # Update the timestamp
    config.timestamp = config.timestamp + 1

    # Update the images
    update_images()


def arrow_up(event):
    # Update the timestamp
    config.timestamp = config.timestamp + 10

    # Update the images
    update_images()


def arrow_down(event):
    # Update the timestamp
    config.timestamp = config.timestamp - 10

    # Update the images
    update_images()
