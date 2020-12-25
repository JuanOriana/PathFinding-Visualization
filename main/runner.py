import pygame
import sys

from main import maze as mz, button as btn

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
GREY = (140,140,140)
ORANGE = (255, 100, 100)
RED = (255, 60, 30)
GREEN = (45, 255, 20)
BLUE = (90, 10, 255)

# Cell-color correspondence
colors = [BLACK, BLUE, ORANGE, GREEN, RED]

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("OpenSans-Regular.ttf", 14)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

maze = mz.Maze(X_CELL, Y_CELL)

# Non changing graphics

# Background
screen.fill(BLACK)

# Title
title = mediumFont.render("Algo-Vis", True, WHITE)
titleRect = title.get_rect()
titleRect.center = ((width / 2), 50)
screen.blit(title, titleRect)


# Buttons
def untoggleAll():
    for button in cellButtons.keys():
        button.untoggle()


def drawButtons():
    for button in cellButtons.keys():
        button.draw(screen)
    buttonClear.draw(screen)


buttonSize = buttonWidth, buttonHeight = 80, 30
buttonStart = btn.Button(60, 750, buttonWidth, buttonHeight, GREEN, smallFont.render('Start', True, BLACK))
buttonEnd = btn.Button(150, 750, buttonWidth, buttonHeight, RED, smallFont.render("End", True, BLACK))
buttonBlock = btn.Button(240, 750, buttonWidth, buttonHeight, BLUE, smallFont.render("Block", True, WHITE))
buttonErase = btn.Button(330, 750, buttonWidth, buttonHeight, GREY, smallFont.render("Erase", True, BLACK))
buttonClear = btn.Button(460,750,buttonWidth, buttonHeight, WHITE, smallFont.render("Clear", True, BLACK))
cellButtons = {
    buttonStart: 3,
    buttonEnd: 4,
    buttonBlock: 1,
    buttonErase: 0
}
buttonBlock.toggle()
drawButtons()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for button in cellButtons.keys():
                if button.collides(mouse):
                    untoggleAll()
                    button.toggle()
                    drawButtons()
            if buttonClear.collides(mouse):
                maze = mz.Maze(X_CELL, Y_CELL)

    # Not using event.get() allows for dragging
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if xOffset <= mouse[0] <= width - xOffset and 125 <= mouse[1] <= 125 + gridHeight:
            cellX = (mouse[0] - xOffset) // CELL_SIZE
            cellY = (mouse[1] - 125) // CELL_SIZE
            for button in cellButtons.keys():
                if button.pressed:
                    maze.setCell(cellX,cellY,cellButtons[button])

    for i in range(X_CELL):
        for j in range(Y_CELL):
            cell = maze.getCell(i, j)
            cellColor = colors[cell]
            pygame.draw.rect(screen, cellColor, (xOffset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (xOffset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                             width=1)
    pygame.display.flip()
