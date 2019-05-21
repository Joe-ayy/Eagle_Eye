# Configuration File - Used to set and (possibly) store values and variables in the program

#region ### Settings for the window gui ###
title = "Eagle Eye Micro v1.0.0"
width = 960
height = 540

print("updated config width: " + str(width))
print("updated config height: " + str(height))

# Do not allow the window to be resizable right now (may change)
r_width = False
r_height = False

#Values for the top left pixel location of the window when it opens
top_lx = 10
top_ly = 10
#endregion

#region ### Ratios ###
# Meter to pixel ratio
m2p = .05

# Timestamp Pad Amount
pad_amount = 5

# Container ratios
map_height_ratio = .9
util_height_ratio = .1
img_height_ratio = .34
c1_width_ratio = .67
c2_width_ratio = .33
#endregion
