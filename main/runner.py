import pygame
import sys
import math

from main import maze as mz, button as btn, algorithms as algo

pygame.init()
size = width, height = 600, 800
gridSize = gridWidth, gridHeight = 480, 600
xOffset = (width - gridWidth) // 2

# cell
CELL_SIZE = 20
X_CELL = gridWidth // CELL_SIZE
Y_CELL = gridHeight // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (140, 140, 140)
ORANGE = (255, 100, 100)
RED = (255, 60, 30)
GREEN = (45, 255, 20)
BLUE = (90, 10, 255)

# Cell-color correspondence
colors = [BLACK, BLUE, ORANGE, GREEN, RED]

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("resources/OpenSans-Regular.ttf", 14)
mediumFont = pygame.font.Font("resources/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("resources/OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("resources/OpenSans-Regular.ttf", 60)

maze = mz.Maze(X_CELL, Y_CELL)

# Non changing graphics

# Background
screen.fill(BLACK)


# Title
# title = mediumFont.render("Algo-Vis", True, WHITE)
# titleRect = title.get_rect()
# titleRect.center = ((width / 2), 50)
# screen.blit(title, titleRect)


# Buttons
def untoggleAll(buttons):
    for button in buttons:
        button.untoggle()


def drawButtons():
    for button in cellButtons:
        button.draw(screen)
    for button in algoButtons:
        button.draw(screen)
    buttonCalculate.draw(screen)
    buttonClear.draw(screen)


def drawMaze():
    for i in range(X_CELL):
        for j in range(Y_CELL):
            cell = maze.getCell(i, j)
            cellColor = colors[cell]
            # Paths change color as they get further from start
            if cell == mz.PATH:
                dist = math.floor(math.sqrt(math.pow(maze.start[0] - i, 2) + math.pow(maze.start[1] - j, 2))) * 5
                cellColor = (cellColor[0] - dist, cellColor[1] + dist // 5, cellColor[2] + dist // 1.5)
            pygame.draw.rect(screen, cellColor, (xOffset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (xOffset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                             width=1)


buttonSize = buttonWidth, buttonHeight = 80, 30
buttonCalculate = btn.Button(460, 70, buttonWidth, buttonHeight, GREEN, smallFont.render('Calculate!', True, BLACK))
buttonClear = btn.Button(460, 750, buttonWidth, buttonHeight, WHITE, smallFont.render("Clear", True, BLACK))

buttonStart = btn.Button(60, 750, buttonWidth, buttonHeight, GREEN, smallFont.render('Start', True, BLACK))
buttonEnd = btn.Button(150, 750, buttonWidth, buttonHeight, RED, smallFont.render("End", True, BLACK))
buttonBlock = btn.Button(240, 750, buttonWidth, buttonHeight, BLUE, smallFont.render("Block", True, WHITE))
buttonErase = btn.Button(330, 750, buttonWidth, buttonHeight, GREY, smallFont.render("Erase", True, BLACK))

buttonBFS = btn.Button(60, 70, buttonWidth, buttonHeight, ORANGE, smallFont.render("BFS", True, BLACK))
buttonDFS = btn.Button(150, 70, buttonWidth, buttonHeight, ORANGE, smallFont.render("DFS", True, BLACK))
buttonAStar = btn.Button(240, 70, buttonWidth, buttonHeight, ORANGE, smallFont.render("A-Star", True, BLACK))

cellButtons = {
    buttonStart: 3,
    buttonEnd: 4,
    buttonBlock: 1,
    buttonErase: 0
}
algoButtons = {
    buttonBFS: algo.BFSAlgo(),
    buttonDFS: algo.DFSAlgo(),
    buttonAStar: algo.AStarAlgo()
}

buttonBlock.toggle()
buttonBFS.toggle()
drawButtons()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            # Redundant code!
            for button in cellButtons.keys():
                if button.collides(mouse):
                    untoggleAll(cellButtons.keys())
                    button.toggle()
                    drawButtons()
            for button in algoButtons.keys():
                if button.collides(mouse):
                    untoggleAll(algoButtons.keys())
                    button.toggle()
                    drawButtons()
            if buttonClear.collides(mouse):
                maze = mz.Maze(X_CELL, Y_CELL)
            if buttonCalculate.collides(mouse):
                for button in algoButtons.keys():
                    if button.pressed:
                        analyzer = algoButtons[button]
                maze.clearPath()
                analyzer.setup(maze)
                while analyzer.flag == algo.ANALYZING:
                    analyzer.nextStep()
                    drawMaze()
                    pygame.display.flip()

    # Not using event.get() allows for dragging
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if xOffset <= mouse[0] <= width - xOffset and 125 <= mouse[1] <= 125 + gridHeight:
            cellX = (mouse[0] - xOffset) // CELL_SIZE
            cellY = (mouse[1] - 125) // CELL_SIZE
            for button in cellButtons.keys():
                if button.pressed:
                    cell = cellButtons[button]
            maze.setCell(cellX, cellY, cell)
            #Add and remove in chunks of 4
            if cell == mz.BLOCKED or cell == mz.EMPTY:
                maze.setCell(cellX+1, cellY, cell)
                maze.setCell(cellX, cellY+1, cell)
                maze.setCell(cellX+1, cellY+1, cell)

    drawMaze()
    pygame.display.flip()
