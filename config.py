# Configuration File - Used to set and (possibly) store values and variables in the program

#region ### Settings for the window gui ###
title = "Eagle Eye v0.3"
width = 1366
height = 768

# Do not allow the window to be resizable right now (may change)
r_width = False
r_height = False

#Values for the top left pixel location of the window when it opens
top_lx = 10
top_ly = 10
#endregion

#region ### Offset values and other ratios ###
# The offsets are initialized to 0, but will be changes upon read .info file
x_offset = 0
y_offset = 0

# Pixel to meter ratio
p2m = .05

# Container ratios
map_height_ratio = .9
util_height_ratio = .1
img_height_ratio = .34
c1_width_ratio = .67
c2_width_ratio = .33
#endregion

### UNSURE IF BELOW IS NEED OR NOT ###

# Holds the values of the current map image being displayed (Currently the program needs to be terminated before
# loading another map
orig_map_width = 0
orig_map_height = 0

# Hold the ratio of the original map to rescaled
map_ratio_x = 0.0
map_ratio_y = 0.0

# Clean-up directory
cleanup_directory = ""

# Trajectory file full path
traj_file = ""

# Save the timestamp
timestamp = 1
