from tkinter.filedialog import *

###
from file_handler import *
from page_builder import *
import config as c
###


def main():
    # Hides the original Tk window
    Tk().withdraw()

    # Prompt the user to select the directory that contains all the necessary map editing files
    cleanup_directory = askdirectory()

    if cleanup_directory != '':
        # Load in the map, info, and trajectory files
        load_files = FilePathHandler(cleanup_directory)

        # Create the application object which automatically opens the gui window
        #app = MainPage(cleanup_directory,
        #               [load_files.map_file_path, load_files.info_file_path, load_files.trajectory_file_path])

        # Initialize the mouse, key, and window bindings
        #app.set_bindings()

        # Draw the map and load in relevant data - NOTE: The map needs to be saved so it isn't garbage collected
        #app.draw_map()

        # Load the initial images that are able to be updated once mainloop start
        #app.update_images()

        # Run the application
        #app.app_window.mainloop()

        # Create a page window
        app = AppPage(c.title, c.width, c.height, cleanup_directory,
                      [load_files.map_file_path, load_files.info_file_path, load_files.trajectory_file_path])

        # Run the page
        app.page_window.mainloop()


if __name__ == "__main__":
    main()
