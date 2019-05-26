# Snake Game with the unicorn hat

#import unicornhat as unicorn
import random
from tkinter import *

class Game():

    def __init__(self):
        GRIDSIZE = 8
        
        self.root = Tk()
        self.root.configure(background='red')
        self.root.title('Status')

        self.paused = StringVar()
        self.paused.set('Welcome!')
        
        self.playingLabel = Label(self.root, width=20, height=10,
                                 bg='red', text=self.paused.get(),
                                 fg='yellow', font=("Helvetica", 30))
        self.playingLabel.bind("<Up>", self.up)
        self.playingLabel.bind("<Down>", self.down)
        self.playingLabel.bind("<Left>", self.left)
        self.playingLabel.bind("<Right>", self.right)
        self.playingLabel.bind("<FocusIn>", self.focusIn)
        self.playingLabel.bind("<FocusOut>", self.focusOut)
        self.playingLabel.bind("<Button-1>", self.clicked)

        self.startButton = Button(self.root, command= lambda: self.startGame(GRIDSIZE),
                             text='Press to start a new game.')
        self.startButton.pack()

        self.playingLabel.pack()

        self.root.mainloop()

    def startGame(self, GRIDSIZE):
        gameGrid = self.makeGrid(GRIDSIZE)
        head = [3, 0]
        gameGrid[head[0]][head[1]] = 'h'
        self.snakeDir = 'right'
        direction = 'right'
        appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]
        gameGrid[appleLoc[0]][appleLoc[1]] = 'a'
        body = 1
        skipRemove = False

        self.startButton.forget()
        self.gameLoop(GRIDSIZE, gameGrid, head, direction,body, appleLoc, skipRemove)

    def makeGrid(self, GRIDSIZE):
        grid = [['.' for i in range(GRIDSIZE)] for i in range(GRIDSIZE)]
        return grid

    def changeDirection(self, gameGrid, head, direction, body):
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

    def checkIfLost(self, grid, head, GRIDSIZE):
        if head[0] > GRIDSIZE-1 or head[1] > GRIDSIZE-1 or head[0] < 0 or head[1] < 0 or type(grid[head[0]][head[1]]) == int:
            return True
        else:
            return False

    def lose(self, body):
        print('You lose! - Your score was %s!' % (body - 1))

    def displayGrid(self, gameGrid, GRIDSIZE, body):
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                print(gameGrid[y][x], end='')
            print('  ', y)
        print ('\n-------%s-------\n' % (body - 1))

    def removeTails(self, gameGrid, GRIDSIZE):
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

    def gameLoop(self, GRIDSIZE, gameGrid, head, direction, body, appleLoc, skipRemove):
        
        lost = False

        if self.paused.get() == 'Playing':

            direction = self.snakeDir

            gameGrid, head = self.changeDirection(gameGrid, head, direction, body)

            if self.checkIfLost(gameGrid, head, GRIDSIZE) == True:
                self.lose(body)
                self.startButton = Button(self.root, command= lambda: self.startGame(GRIDSIZE),
                                          text='Click here to start a new game.')
                self.startButton.pack()
                lost = True
            else:
                if gameGrid[head[0]][head[1]] == 'a':
                    body += 1
                    while True:
                        appleLoc = [random.randint(0, GRIDSIZE-1), random.randint(0, GRIDSIZE-1)]
                        if gameGrid[appleLoc[0]][appleLoc[1]] == '.':
                            gameGrid[appleLoc[0]][appleLoc[1]] = 'a'
                            break
                    skipRemove = True
    
                gameGrid[head[0]][head[1]] = 'h'

                self.displayGrid(gameGrid, GRIDSIZE, body)

                if skipRemove == False:
                    gameGrid = self.removeTails(gameGrid, GRIDSIZE)
                else:
                    skipRemove = False

        if lost == False:
            self.root.after(500, lambda: self.gameLoop(GRIDSIZE, gameGrid, head, direction, body, appleLoc, skipRemove))

game = Game()
