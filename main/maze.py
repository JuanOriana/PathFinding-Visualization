import numpy as np
import random as rand

EMPTY = 0
BLOCKED = 1
PATH = 2
START = 3
END = 4
FINAL_PATH = 5

HORIZONTAL = S = 0
VERTICAL = E = 1


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

    def randMaze(self, threshold):
        self.initMaze()
        for i in range(self.rows):
            for j in range(self.cols):
                currCell = self.getCell(i, j)
                if currCell != START and currCell != END and rand.random() < threshold:
                    self.setCell(i, j, BLOCKED)

    def chooseOrientation(self, rows, cols):
        if cols < rows:
            return HORIZONTAL
        elif rows == cols:
            det = rand.random()
            if det < 0.5:
                return HORIZONTAL
        # if rows < width or height==width and has been randomly selected
        return VERTICAL

    def fillBlocks(self):
        self.state = np.ones((self.rows, self.cols), dtype=int)

    def generateMaze(self):
        self.fillBlocks()
        frontiers = []
        i = rand.randint(0, self.rows - 1)
        j = rand.randint(0, self.cols - 1)
        frontiers.append([i, j, i, j])

        while frontiers:
            front = frontiers.pop(rand.randint(0, len(frontiers) - 1))
            i = front[2]
            j = front[3]
            if self.state[i][j] == BLOCKED:
                self.state[front[0]][front[1]] = self.state[i][j] = EMPTY
                if i >= 2 and self.state[i - 2][j] == BLOCKED:
                    frontiers.append([i - 1, j, i - 2, j])
                if j >= 2 and self.state[i][j - 2] == BLOCKED:
                    frontiers.append([i, j - 1, i, j - 2])
                if i < self.rows - 2 and self.state[i + 2][j] == BLOCKED:
                    frontiers.append([i + 1, j, i + 2, j])
                if j < self.cols - 2 and self.state[i][j + 2] == BLOCKED:
                    frontiers.append([i, j + 1, i, j + 2])

        self.state[self.start[0]][self.start[1]] = START
        self.state[self.end[0]][self.end[1]] = END
