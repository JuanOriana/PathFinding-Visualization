from abc import ABC, abstractmethod
import numpy as np
from main import maze as mz

INACTIVE = 0
ANALYZING = 1
SUCCESS = 2
FAILURE = 3

neighbourIncs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class PathFindingAlgo(ABC):

    def __init__(self):
        self.flag = INACTIVE
        self.visitCount = 0
        self.maze = None

    def setup(self, maze):
        pass

    def nextStep(self):
        pass


class BFSAlgo(PathFindingAlgo):

    def __init__(self):
        super().__init__()
        self.visited = None
        self.queue = None

    def setup(self, maze):
        self.flag = ANALYZING
        self.visitCount = 0
        self.maze = maze
        self.visited = np.zeros((maze.rows, maze.cols), dtype=bool)
        self.queue = [maze.start]
        self.visited[maze.start[0]][maze.start[1]] = True

    def nextStep(self):
        if self.flag != ANALYZING:
            raise Exception()
        # Empty queue during analysis implies no found solution
        if not self.queue:
            self.flag = FAILURE
            return

        curr = self.queue.pop(0)
        currCell = self.maze.state[curr[0]][curr[1]]
        if currCell == mz.END:
            self.flag = SUCCESS
            return

        elif currCell != mz.START:
            self.maze.state[curr[0]][curr[1]] = mz.PATH

        for inc in neighbourIncs:
            newPos = (curr[0] + inc[0], curr[1] + inc[1])
            if self.maze.inBounds(newPos[0], newPos[1]) and not self.visited[newPos[0]][newPos[1]] and \
                    self.maze.state[newPos[0]][newPos[1]] != mz.BLOCKED:
                self.visited[newPos[0]][newPos[1]] = True
                self.queue.append(newPos)


class DFSAlgo(PathFindingAlgo):

    def __init__(self):
        super().__init__()
        self.visited = None
        self.stack = None

    def setup(self, maze):
        self.flag = ANALYZING
        self.visitCount = 0
        self.maze = maze
        self.stack = [maze.start]
        self.visited = set()
        self.visited.add(maze.start)

    def nextStep(self):
        if self.flag != ANALYZING:
            raise Exception()
        # Empty queue during analysis implies no found solution
        if not self.stack:
            self.flag = FAILURE
            return

        curr = self.stack.pop()
        currCell = self.maze.state[curr[0]][curr[1]]
        if currCell == mz.END:
            self.flag = SUCCESS
            return

        elif currCell != mz.START:
            self.maze.state[curr[0]][curr[1]] = mz.PATH

        for inc in neighbourIncs:
            newPos = (curr[0] + inc[0], curr[1] + inc[1])
            if self.maze.inBounds(newPos[0], newPos[1]) and not newPos in self.visited and self.maze.state[newPos[0]][
                newPos[1]] != mz.BLOCKED:
                self.visited.add(newPos)
                self.stack.append(newPos)
