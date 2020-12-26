import numpy as np

EMPTY = 0
BLOCKED = 1
PATH = 2
START = 3
END = 4
FINAL_PATH = 5


class Maze:
    def __init__(self, rows, cols):
        if rows < 0 or cols < 0:
            raise Exception()
        self.state = None
        self.rows = rows
        self.cols = cols
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)
        self.initMaze()

    def initMaze(self):
        self.state = np.zeros((self.rows, self.cols), dtype=int)
        self.state[self.start[0]][self.start[1]] = START
        self.state[self.end[0]][self.end[1]] = END

    def setCell(self, i, j, cell):
        # Cant insert a cell where a start/end cell is
        if self.inBounds(i, j) and 0 <= cell <= END and self.state[i][j] != START and self.state[i][j] != END:
            if cell == START:
                self.changeStart((i, j))
            elif cell == END:
                self.changeEnd((i, j))
            else:
                self.state[i][j] = cell

    def inBounds(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def getCell(self, i, j):
        if self.inBounds(i, j):
            return self.state[i][j]

    def changeStart(self, newStart):
        if self.inBounds(newStart[0], newStart[1]):
            self.state[self.start[0]][self.start[1]] = EMPTY
            self.state[newStart[0]][newStart[1]] = START
            self.start = newStart

    def changeEnd(self, newEnd):
        if self.inBounds(newEnd[0], newEnd[1]):
            self.state[self.end[0]][self.end[1]] = EMPTY
            self.state[newEnd[0]][newEnd[1]] = END
            self.end = newEnd

    def clearPath(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.state[i][j] == PATH or self.state[i][j] == FINAL_PATH:
                    self.state[i][j] = EMPTY

