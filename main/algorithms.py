from abc import ABC, abstractmethod
import numpy as np
from main import maze as mz
import math
from queue import PriorityQueue

INACTIVE = 0
ANALYZING = 1
SUCCESS = 2
FAILURE = 3

neighbourIncs = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]


class PathFindingAlgo(ABC):

    def __init__(self):
        self.flag = INACTIVE
        self.visitCount = 0
        self.maze = None
        self.parent = None
        self.pathLength = 0

    def setup(self, maze):
        pass

    def nextStep(self):
        pass

    def recoverPath(self):
        self.pathLength = 1
        nextCell = self.parent[self.maze.end]
        while nextCell != self.maze.start:
            self.maze.state[nextCell[0]][nextCell[1]] = mz.FINAL_PATH
            nextCell = self.parent[nextCell]
            self.pathLength += 1
        pass


class BFSAlgo(PathFindingAlgo):

    def __init__(self):
        super().__init__()
        self.visited = None
        self.queue = None

    def setup(self, maze):
        self.flag = ANALYZING
        self.visitCount = 0
        self.pathLength = 0
        self.maze = maze
        self.parent = {}
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
            self.visitCount += 1
            self.flag = SUCCESS
            self.recoverPath()
            return

        elif currCell != mz.START:
            self.visitCount += 1
            self.maze.state[curr[0]][curr[1]] = mz.PATH

        for inc in neighbourIncs:
            newPos = (curr[0] + inc[0], curr[1] + inc[1])
            if self.maze.inBounds(newPos[0], newPos[1]) and not self.visited[newPos[0]][newPos[1]] and \
                    self.maze.state[newPos[0]][newPos[1]] != mz.BLOCKED:
                self.visited[newPos[0]][newPos[1]] = True
                self.queue.append(newPos)
                self.parent[newPos] = curr


class DFSAlgo(PathFindingAlgo):

    def __init__(self):
        super().__init__()
        self.visited = None
        self.stack = None

    def setup(self, maze):
        self.flag = ANALYZING
        self.visitCount = 0
        self.pathLength = 0
        self.maze = maze
        self.parent = {}
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
            self.visitCount += 1
            self.flag = SUCCESS
            self.recoverPath()
            return

        elif currCell != mz.START:
            self.visitCount += 1
            self.maze.state[curr[0]][curr[1]] = mz.PATH

        for inc in neighbourIncs:
            newPos = (curr[0] + inc[0], curr[1] + inc[1])
            if self.maze.inBounds(newPos[0], newPos[1]) and newPos not in self.visited and self.maze.state[newPos[0]][
                newPos[1]] != mz.BLOCKED:
                self.visited.add(newPos)
                self.stack.append(newPos)
                self.parent[newPos] = curr


class AStarAlgo(PathFindingAlgo):

    def __init__(self):
        super().__init__()
        self.g = {}  # Distance to start
        self.f = {}  # Total cost  f = g + h
        self.parent = {}
        self.count = 0  # tie breaker
        self.open = PriorityQueue()
        self.openHash = set()  # PriorityQueue doesnt allow me to check for an element easily

    # heuristic
    def h(self, pointA, pointB):
        return math.sqrt(math.pow(pointA[0] - pointB[0], 2) + math.pow(pointA[1] - pointB[1], 2))

    def setup(self, maze):
        self.flag = ANALYZING
        self.visitCount = 0
        self.count = 0
        self.pathLength = 0
        self.maze = maze
        self.open = PriorityQueue()
        self.openHash = set()
        self.g = {}
        self.f = {}
        self.parent = {}

        self.open.put((0, self.count, maze.start))
        self.openHash.add(maze.start)
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                self.g[(i, j)] = float("inf")
                self.f[(i, j)] = float("inf")
        self.g[maze.start] = 0
        self.f[maze.start] = self.h(maze.start, maze.end)

    def nextStep(self):
        if self.flag != ANALYZING:
            raise Exception()
        # Empty queue during analysis implies no found solution
        if not self.openHash:
            self.flag = FAILURE
            return

        curr = self.open.get()[2]
        self.openHash.remove(curr)
        currCell = self.maze.state[curr[0]][curr[1]]

        if currCell == mz.END:
            self.visitCount += 1
            self.flag = SUCCESS
            self.recoverPath()
            return

        elif currCell != mz.START:
            self.visitCount += 1
            self.maze.state[curr[0]][curr[1]] = mz.PATH

        for inc in neighbourIncs:
            newPos = (curr[0] + inc[0], curr[1] + inc[1])
            if self.maze.inBounds(newPos[0], newPos[1]) and self.maze.state[newPos[0]][newPos[1]] != mz.BLOCKED:
                tempG = self.g[curr] + 1
                if tempG < self.g[newPos]:
                    self.parent[newPos] = curr
                    self.g[newPos] = tempG
                    self.f[newPos] = tempG + self.h(newPos, self.maze.end)
                    if newPos not in self.openHash:
                        self.count += 1
                        self.open.put((self.f[newPos], self.count, newPos))
                        self.openHash.add(newPos)
