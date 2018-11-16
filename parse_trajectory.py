# given a trajectory file this parse strips the x,y,timestamp and returns this informaiton in a map?
import CoordinateMap as Map
def strip_parts(line):
    delim_location = line.find(' ')
    xcord = line[:delim_location]

    line = line[delim_location + 1:]
    delim_location = line.find(' ')
    ycord = line[:delim_location]

    line = line[delim_location + 1:]

    for x in range(0, 4):
        delim_location = line.find(' ')
        line = line[delim_location + 1:]

    delim_location = line.find(' ')
    time_stamp = line[:delim_location]
    line = xcord + " " + ycord + " " + time_stamp

    return line


def get_x_y_timestamp(table):
    parsed_table = []
    for line in table:
        parsed_table.append(strip_parts(line))

    return [1, 2]


def parse_traj(filename):
    file = open(filename, 'r')
    line_table = []
    x_y_timestamp_table = []
    line = file.readline()
    # hard code skip the header in the file
    for x in range(0, 14):
        line = file.readline()

    while line:
        line_table.append(line)
        line = file.readline()

    x_y_timestamp_table = get_x_y_timestamp(line_table)
    return x_y_timestamp_table


if __name__ == "__main__":
    parse_traj("trajectory_2018-10-30-14-12-06_leveled.ply")

else:
    print(__name__ + "being called as a module")
