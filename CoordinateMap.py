import operator


class CoordinateMap:

    def __init__(self):
        self.map = dict()
        self.key = ''
        self.timestamp_found = ''

    def  findTime(self, x, y):
        self.key = str(x) + ' ' + str(y)
        self.timestamp_found = self.map.get(self.key, None)
        if self.timestamp_found == None:
            return "Time stamp for values was not found"
        else:
            return self.timestamp_found

    def addKeyandValue(self, x, y, time):
        self.map[x + ' ' + y] = time
        return

    def printMap(self):
        print(self.map)
