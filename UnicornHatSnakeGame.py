#!/usr/bin/env python3
# Snake Game with the unicorn hat

import unicornhat as unicorn
import random
from tkinter import *

unicorn.brightness(0.02)
unicorn.rotation(90)

class Game():

    def __init__(self):
        GRIDSIZE = 8        # Changeable constant - Grid size
        
        self.root = Tk()
        self.root.configure(background='red')
        self.root.title('Menu')

        self.paused = StringVar() # Create the variable for 'paused' or 'playing'
        self.paused.set('Welcome!')
        
        # Creates the label, so tkinter knows which arrow key you pressed.
        self.playingLabel = Label(self.root, width=20, height=10,
                                 bg='red', text=self.paused.get(),
                                 fg='yellow', font=("Helvetica", 30))
        self.playingLabel.bind("<Up>", self.up)
        self.playingLabel.bind("<Down>", self.down)
        self.playingLabel.bind("<Left>", self.left)
        self.playingLabel.bind("<Right>", self.right) # Binds certain keys to functions
        self.playingLabel.bind("<FocusIn>", self.focusIn)
        self.playingLabel.bind("<FocusOut>", self.focusOut)
        self.playingLabel.bind("<Button-1>", self.clicked)

        self.playingLabel.pack()

        self.gameMenu(GRIDSIZE)

        self.root.mainloop() # Starts the tkinter mainloop

    def gameMenu(self, GRIDSIZE):
        self.startButton = Button(self.root, command= lambda: self.startGame(GRIDSIZE),
                                  text='Press to start a new game.')
        self.startButton.pack(side=TOP) # Creates the start button
        self.speedScale = Scale(self.root, from_=50, to=600, resolution=50, orient=HORIZONTAL,
                                length=450, label='Game Speed (ms)', bg='light green',
                                troughcolor='green')
        self.speedScale.set(200) # Default Speed Value
        self.speedScale.pack(side=BOTTOM)
        
    def startGame(self, GRIDSIZE):
        gameGrid = self.makeGrid(GRIDSIZE) # Creates the grid
        head = [0, 3]                      # Positioning for the head to start
        gameGrid[head[0]][head[1]] = 'h'   # Places head on the grid

        self.snakeDir = 'right'            # Starting direction is always 'right'
        direction = 'right' # Have to change both of them in case the user does not press a key.

        appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]
        gameGrid[appleLoc[0]][appleLoc[1]] = 'a' # Random apple location put on the grid.
        body = 1 # Snake starts with a body of one
        skipRemove = False

        speed = self.speedScale.get()
        self.startButton.forget() # Removes the start button
        self.speedScale.forget()
        self.gameLoop(GRIDSIZE, gameGrid, head, direction,body, appleLoc, skipRemove, speed)

    def makeGrid(self, GRIDSIZE):
        grid = [['.' for i in range(GRIDSIZE)] for i in range(GRIDSIZE)]
        return grid

    def checkArrow(self, direction):
        newDirection = self.snakeDir    # Makes sure you cannot go back onto yourself (and lose)
        if newDirection == 'up' and direction == 'down':
            return direction
        elif newDirection == 'down' and direction == 'up':
            return direction
        elif newDirection == 'left' and direction == 'right':
            return direction
        elif newDirection == 'right' and direction == 'left':
            return direction
        else:
            return newDirection

    def changeDirection(self, gameGrid, head, direction, body):
        if direction == 'up':
            gameGrid[head[0]][head[1]] = body
            head[1] += 1
        elif direction == 'down':
            gameGrid[head[0]][head[1]] = body
            head[1] -= 1
        elif direction == 'left':
            gameGrid[head[0]][head[1]] = body
            head[0] -= 1
        elif direction == 'right':
            gameGrid[head[0]][head[1]] = body
            head[0] += 1
        return gameGrid, head

    def checkIfLost(self, grid, head, body, GRIDSIZE): 
        if head[0] > GRIDSIZE-1 or head[1] > GRIDSIZE-1 or head[0] < 0 or head[1] < 0 or type(grid[head[0]][head[1]]) == int:
            self.lose(body)
            return True 
        else:
            return False # If the snake is outside the grid or touches itself then you lose

    def lose(self, body):
        print('You lose! - Your score was %s!' % (body - 1))

    def displayGrid(self, gameGrid, GRIDSIZE, body): # Displays the grid on the HAT
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                if gameGrid[y][x] == 'h':
                    unicorn.set_pixel(x, y, 0, 255, 255)
                elif type(gameGrid[y][x]) == int:
                    unicorn.set_pixel(x, y, 255, 255, 0)
                elif gameGrid[y][x] == 'a':
                    unicorn.set_pixel(x, y, 255, 0, 0)
                else:
                    unicorn.set_pixel(x, y, 0, 0, 0)
        unicorn.show()

    def removeTail(self, gameGrid, GRIDSIZE): # Removes the tail of the snake
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                if type(gameGrid[x][y]) == int:
                    gameGrid[x][y] -= 1
                    if gameGrid[x][y] == 0:
                        gameGrid[x][y] = '.'
        return gameGrid

    def up(self, event):
        self.snakeDir = 'up'
    def down(self, event):
        self.snakeDir = 'down'
    def left(self, event):
        self.snakeDir = 'left'
    def right(self, event):
        self.snakeDir = 'right'
    def focusIn(self, event):
        self.paused.set('Playing')
        self.playingLabel.config(text=self.paused.get())
    def focusOut(self, event):
        self.paused.set('Paused')
        self.playingLabel.config(text=self.paused.get())
    def clicked(self, event):
        self.playingLabel.focus_set()

    def gameLoop(self, GRIDSIZE, gameGrid, head, direction, body, appleLoc, skipRemove, speed):
        
        lost = False

        if self.paused.get() == 'Playing': # If the game is not paused then it continues

            direction = self.checkArrow(direction) # Get the players direction

            gameGrid, head = self.changeDirection(gameGrid, head, direction, body)

            if self.checkIfLost(gameGrid, head, body, GRIDSIZE) == True:
                self.gameMenu(GRIDSIZE)
                lost = True
            else:
                if gameGrid[head[0]][head[1]] == 'a': # Check if the snake hit an apple
                    body += 1
                    while True:
                        appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]
                        if gameGrid[appleLoc[0]][appleLoc[1]] == '.':   # Only put on empty spaces
                            gameGrid[appleLoc[0]][appleLoc[1]] = 'a'
                            break
                    skipRemove = True    # If so do not remove the bodies for a turn
    
                gameGrid[head[0]][head[1]] = 'h'   # Places the new snake head

                self.displayGrid(gameGrid, GRIDSIZE, body)

                if skipRemove == False:
                    gameGrid = self.removeTail(gameGrid, GRIDSIZE) # Removes the tail of the snake
                else:
                    skipRemove = False

        if lost == False:
            self.root.after(speed, lambda: self.gameLoop(GRIDSIZE, gameGrid, head, direction, body, appleLoc, skipRemove, speed))

game = Game()
