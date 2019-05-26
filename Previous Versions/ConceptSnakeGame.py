# Snake Game without the unicorn hat

import random

GRIDSIZE = 8


def makeGrid(GRIDSIZE):
    grid = [['.' for i in range(GRIDSIZE)] for i in range(GRIDSIZE)]
    return grid

def checkArrow(direction):
    keyboardArrow = input('Arrow Direction?')
    return keyboardArrow

def changeDirection(gameGrid, head, direction, body):
    if direction == 'up':
        gameGrid[head[0]][head[1]] = body
        head[0] += 1
    elif direction == 'down':
        gameGrid[head[0]][head[1]] = body
        head[0] -= 1
    elif direction == 'left':
        gameGrid[head[0]][head[1]] = body
        head[1] -= 1
    elif direction == 'right':
        gameGrid[head[0]][head[1]] = body
        head[1] += 1
    return gameGrid, head

def checkIfLost(grid, head, GRIDSIZE):
    if head[0] > GRIDSIZE-1 or head[1] > GRIDSIZE-1 or head[0] < 0 or head[1] < 0 or type(grid[head[0]][head[1]]) == int:
        return True
    else:
        return False

def lose():
    print('You lose!')

def displayGrid(gameGrid, GRIDSIZE):
    for i in range(GRIDSIZE):
        print(i, '  ', gameGrid[i])
    print ('\n--------------\n')

def removeTails(gameGrid, GRIDSIZE):
    for y in range(GRIDSIZE):
        for x in range(GRIDSIZE):
            if type(gameGrid[x][y]) == int:
                gameGrid[x][y] -= 1
                if gameGrid[x][y] == 0:
                    gameGrid[x][y] = '.'
    return gameGrid


### -------------------- Start of Game -------------------- ###


gameGrid = makeGrid(GRIDSIZE)

head = [3, 3]
gameGrid[head[0]][head[1]] = 'h'

direction = 'right'
appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]

gameGrid[appleLoc[0]][appleLoc[1]] = 'a'
body = 1
skipRemove = False

while True:
    gameGrid, head = changeDirection(gameGrid, head, direction, body)

    if checkIfLost(gameGrid, head, GRIDSIZE) == True:
        lose()
        break

    if gameGrid[head[0]][head[1]] == 'a':
        body += 1
        while True:
            appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]
            if gameGrid[appleLoc[0]][appleLoc[1]] == '.':
                gameGrid[appleLoc[0]][appleLoc[1]] = 'a'
                break
        skipRemove = True
    
    gameGrid[head[0]][head[1]] = 'h'

    displayGrid(gameGrid, GRIDSIZE)

    if skipRemove == False:
        gameGrid = removeTails(gameGrid, GRIDSIZE)
    else:
        skipRemove = False

    direction = checkArrow(direction)
