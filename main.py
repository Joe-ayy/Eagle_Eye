from tkinter.filedialog import *

###
from user_gui import *
from file_handler import *
###


def main():
    # Hides the original window
    Tk().withdraw()

    # Create a splash screen to display to the user
    #splash_screen = BuildWindow("Welcome to Eagle Eye!", 500, 200, False, False, 400, 500)
    #splash_screen.after(5000, splash_screen.destroy)

    # Prompt the user to select the directory that contains all the necessary map editing files
    cleanup_directory = askdirectory()

    if cleanup_directory != '':
        # Load in the map, info, and trajectory files
        load_files = FilePathHandler(cleanup_directory)

        # Create the application object which automatically opens the gui window
        app = MainPage(cleanup_directory,
                       [load_files.map_file_path, load_files.info_file_path, load_files.trajectory_file_path])

        # Initialize the mouse and keybindings
        app.set_button_bindings()
        app.set_key_bindings()

        # Draw the map and load in relevant data - NOTE: The map needs to be saved so it isn't garbage collected
        app.draw_map()

        # Load the initial images that are able to be updated once mainloop start
        app.update_images()

        # Run the application
        app.app_window.mainloop()


if __name__ == "__main__":
    main()
