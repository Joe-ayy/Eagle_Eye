from tkinter.filedialog import *

###
from user_gui import *
import config as c
from timestamp_ops import *
import file_and_image_handling as fih
###

# AT SOME POINT IN THE MAIN BEFORE THE PROGRAM GETS GOING, CHECK TO MAKE SURE ALL NEEDED FILES ARE THERE


def main():
    # Prompt the user to select the directory that contains all the necessary map editing files
    c.cleanup_directory = askdirectory()

    if c.cleanup_directory != '':
        # Load in the necessary files to set config values
        get_offsets(c.cleanup_directory)
        fih.get_trajectory_path(c.cleanup_directory)

        # Create the application object which automatically opens the gui window
        app = MainPage()

        # Initialize the mouse and keybindings
        app.set_button_bindings()
        app.set_key_bindings()

        # Run the application
        app.app_window.mainloop()

        # Delete any images after program is terminated
        delete_images(c.cleanup_directory)


if __name__ == "__main__":
    main()
