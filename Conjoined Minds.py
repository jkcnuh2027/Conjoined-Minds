import pygame, sys, os
from pygame.locals import *
import copy

#CONJOINED MINDS: By Juan (jutjuan) Eizaguerri

#Color constants
WHITE = (255,255,255)
BLUE = (50,50,255)
RED = (255,50,50)
BLACK = (0,0,0)
BROWN = (165, 42, 42)

#Size of the window
WIDTH = 500
HEIGHT = 500
SIZE = (WIDTH, HEIGHT)

#Position and state of the portals
FINISH_CELLS = [(0,0), (0,0)]
FINISH_CELLS_STATE = [False, False] #true - player on it

#Level maps:
    # 0 - Floor
    # 1 - Wall
    # 2 - Portal
    # 3, 4 - Player
    # 5 - Box
LEVEL1 =     [[1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,0,0,0,0,0,1],
              [1,0,3,0,1,0,0,2,0,1],
              [1,0,0,0,1,0,0,0,0,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,1,0,0,0,0,1],
              [1,0,4,0,1,0,0,2,0,1],
              [1,0,0,0,0,0,0,0,0,1],
              [1,1,1,1,1,1,1,1,1,1]]

LEVEL2 =     [[1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,0,1,0,1,0,1],
              [1,0,3,0,0,1,2,0,2,1],
              [1,0,0,0,0,1,1,0,1,1],
              [1,1,1,1,5,1,1,0,1,1],
              [1,0,0,1,0,1,0,0,0,1],
              [1,0,0,1,0,1,5,5,5,1],
              [1,0,4,1,0,1,0,0,0,1],
              [1,0,0,0,0,0,0,1,0,1],
              [1,1,1,1,1,1,1,1,1,1]]

LEVEL3 =     [[1,1,1,1,1,1,1,1,1,1],
              [1,2,0,1,1,0,1,0,0,1],
              [1,0,0,0,0,0,1,0,3,1],
              [1,0,1,0,1,0,5,0,0,1],
              [1,0,0,0,1,0,1,1,1,1],
              [1,0,1,1,1,0,1,0,1,1],
              [1,0,0,0,1,5,1,0,0,1],
              [1,1,5,1,1,0,1,0,1,1],
              [1,4,0,0,0,0,0,0,2,1],
              [1,1,1,1,1,1,1,1,1,1]]

LEVEL4 =     [[1,1,1,1,1,1,1,1,1,1],
              [1,3,0,0,0,0,0,0,1,1],
              [1,0,1,1,1,0,1,0,0,1],
              [1,5,0,0,1,0,1,5,1,1],
              [1,0,1,0,1,0,1,0,0,1],
              [1,4,0,5,0,0,5,0,1,1],
              [1,1,1,1,5,1,1,0,0,1],
              [1,1,1,0,0,0,1,0,0,1],
              [1,2,0,2,1,0,0,0,0,1],
              [1,1,1,1,1,1,1,1,1,1]]

LEVEL5 =     [[1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,0,0,0,0,0,1],
              [1,0,6,9,9,9,9,9,0,1],
              [1,0,9,9,9,9,9,9,0,1],
              [1,0,9,9,9,9,9,9,0,1],
              [1,5,9,9,9,9,9,9,5,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,0,0,0,0,0,1],
              [1,0,3,5,0,0,5,4,0,1],
              [1,1,1,1,1,1,1,1,1,1]]



currentMap = []
cellSize = 50

LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5]
LEVELS_TEMPLATE = copy.deepcopy(LEVELS)
CURRENT_LEVEL = 0

#Making constants to have quick access to the images
dirname = os.path.dirname(__file__)
wallImgPath = os.path.join(dirname, 'Wall.jpeg')
boxImgPath = os.path.join(dirname, 'Box.jpeg')
floorImgPath = os.path.join(dirname, 'Floor.jpeg')
portalImgPath = os.path.join(dirname, 'Portal.jpeg')
player1ImgPath = os.path.join(dirname, 'Player1.jpeg')
player2ImgPath = os.path.join(dirname, 'Player2.jpeg')
thanksImgPath = os.path.join(dirname, 'Thanks.jpeg')

WALL_IMG = pygame.image.load(wallImgPath)
BOX_IMG = pygame.image.load(boxImgPath)
FLOOR_IMG = pygame.image.load(floorImgPath)
PORTAL_IMG = pygame.image.load(portalImgPath)
PLAYER1_IMG = pygame.image.load(player1ImgPath)
PLAYER2_IMG = pygame.image.load(player2ImgPath)
THANKS_IMG = pygame.image.load(thanksImgPath)

PLAYERiMG = [0,0, PLAYER1_IMG, PLAYER2_IMG]

#Function to draw rectangles (Not used)
def DrawRect(display, color, rect):
    pygame.draw.rect(display, color, rect)

#Defining Player class
class playerClass:
    #Variables inside the Player Class:
    tag = 0
    x = 0
    y = 0
    color = (0,0,0)
    rectTransformX = 0
    rectTransformY = 0
    display = None

    #Methods of the player class:
    #Init is called when an object of this class is summoned
    def __init__(self, x, y, color, display, tag):
        self.x = x
        self.y = y
        self.color = color
        self.display = display
        self.tag = tag
    #Set the positon of the player, used in the DrawMap function
    def SetPos(self, x, y):
        self.x = x
        self.y = y
        self.Draw(self.color)

    #Move the player in the desired direction given by the x and y values
    def Move(self, xValue, yValue):
        global FINISH_CELLS_STATE, LEVELS, LEVEL1, LEVEL2

        if(LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] != 1): #Check if there is a wall in front of the player
            move = 1
            if(LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] == 4 or LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] == 3): #Check if there is another character in front of the player
                if(LEVELS[CURRENT_LEVEL][self.y + yValue * 2][self.x + xValue * 2] == 1):
                    move = 0
                if(LEVELS[CURRENT_LEVEL][self.y + yValue * 2][self.x + xValue * 2] == 5):
                    if(LEVELS[CURRENT_LEVEL][self.y + yValue * 3][self.x + xValue * 3] == 1):
                        move = 0
            
            if(LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] == 5): #Check if there is a box in front of the player, in which case the MoveBox method is called
                if(LEVELS[CURRENT_LEVEL][self.y + yValue * 2][self.x + xValue * 2] == 0 or LEVELS[CURRENT_LEVEL][self.y + yValue * 2][self.x + xValue * 2] == 2):
                    self.MoveBox(xValue, yValue)
                move = 0
            
            if(move == 1): # If there isn't anything that prevents the player from moving it will update its position
                self.rectTransformX = self.x * cellSize
                self.rectTransformY = self.y * cellSize
                rect = (self.rectTransformX, self.rectTransformY)
                #Draw old position
                if(LEVELS[CURRENT_LEVEL][self.y][self.x] == 2):
                    #self.Draw(RED) (Obsolete)
                    self.display.blit(PORTAL_IMG, rect)
                else:
                    #self.Draw(WHITE) (Obsolete)
                    self.display.blit(FLOOR_IMG, rect)

                #Update position
                if(LEVELS[CURRENT_LEVEL][self.y][self.x] != 2):
                    LEVELS[CURRENT_LEVEL][self.y][self.x] = 0
                if(LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] != 2):
                    LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] = self.tag
                self.x += xValue
                self.y += yValue

                self.Draw(self.color)

        #Detect finish cell
        for i in (0,1):
            if(FINISH_CELLS[i] == (self.x, self.y)):
                FINISH_CELLS_STATE[i] = True




    def MoveBox(self, xValue, yValue):
        global LEVELS, LEVEL1, LEVEL2
        #Update the box position in the level matrix
        LEVELS[CURRENT_LEVEL][self.y + yValue][self.x + xValue] = 0
        LEVELS[CURRENT_LEVEL][self.y + yValue * 2][self.x + xValue * 2] = 5

        #Draw the box in its new position
        boxTransformX = (self.x + xValue) * cellSize
        boxTransformY = (self.y + yValue) * cellSize
        currentRect = (boxTransformX, boxTransformY)
        #DrawRect(self.display, WHITE, currentRect) (obsolete)
        self.display.blit(FLOOR_IMG, currentRect)

        boxNewTransformX = (self.x + xValue * 2) * cellSize
        boxNewTransformY = (self.y + yValue * 2) * cellSize
        newRect = (boxNewTransformX, boxNewTransformY)
        #DrawRect(self.display, BROWN, newRect) (obsolete)
        self.display.blit(BOX_IMG, newRect)
        self.Move(xValue, yValue)
        

    def Draw(self, color):
        self.rectTransformX = self.x * cellSize
        self.rectTransformY = self.y * cellSize

        playerRect = (self.rectTransformX, self.rectTransformY)
        #DrawRect(self.display, color, playerRect)
        self.display.blit(PLAYERiMG[self.tag-1], playerRect)



#The DrawMap function checks the matrix (map) of the level cell by cell and places a floor, wall, portal, box or player depending of the value
def DrawMap(matrix, display, player1, player2):
    global FINISH_CELLS #"global" is used to be able to modify a global variable
    finishCell = 0

    cells = len(matrix)
    for i in range(cells):
        for j in range(cells):
            rect = (i * cellSize, j * cellSize,cellSize, cellSize)
            if(matrix[j][i] == 1): # Wall
                #DrawRect(display, BLUE, rect) (obsolete)
                display.blit(WALL_IMG, (i * cellSize, j * cellSize))
            elif(matrix[j][i] == 2): #Portal
                FINISH_CELLS[finishCell] = (i, j)
                finishCell += 1
                #DrawRect(display, RED, rect) (obsolete)
                display.blit(PORTAL_IMG, (i * cellSize, j * cellSize))
            elif(matrix[j][i] == 5): #Box
                #DrawRect(display, BROWN, rect) (obsolete)
                display.blit(BOX_IMG, (i * cellSize, j * cellSize))
            elif(matrix[j][i] == 6): #Last level text image
                display.blit(THANKS_IMG, (i * cellSize, j * cellSize))

            #Call the SetPos method of both characters
            elif(matrix[j][i] == 3):
                player1.SetPos(i,j)
            elif(matrix[j][i] == 4):
                player2.SetPos(i,j)
                
            elif(matrix[j][i] == 0): #Floor
                #DrawRect(display, WHITE, rect) (obsolete)
                display.blit(FLOOR_IMG, (i * cellSize, j * cellSize))

#Changes the current level value and draws the new level
def NextLevel(display, player1, player2):
    global CURRENT_LEVEL
    CURRENT_LEVEL += 1

    DrawMap(LEVELS[CURRENT_LEVEL], display, player1, player2)

            

def main():
    #Start pygame
    pygame.init()

    #Create a window
    DISPLAY=pygame.display.set_mode(SIZE,0,32)

    #Make the window background white (Not really necessary since we are drawing over that background, but looks better if something fails :p)
    DISPLAY.fill(WHITE)


    #Create two objects of the player class
    player1 = playerClass(0,0, BLACK, DISPLAY, 3)
    player2 = playerClass(0,0, BLACK, DISPLAY, 4)

    #Call the DrawMap function to load the first level
    DrawMap(LEVELS[0], DISPLAY, player1, player2)


    #Update function: Everything inside here is run every frame
    while True:
        global FINISH_CELLS_STATE
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN: #Ckeck keyboard input
                
                #Move with arrows
                if event.key == pygame.K_LEFT: 
                    player1.Move(-1, 0)
                    player2.Move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player1.Move(1, 0)
                    player2.Move(1, 0)
                if event.key == pygame.K_UP:
                    player1.Move(0, -1)
                    player2.Move(0, -1)
                if event.key == pygame.K_DOWN:
                    player1.Move(0, 1)
                    player2.Move(0, 1)
                player1.Draw(player1.color)
                player2.Draw(player2.color)

                #Restart with r
                if event.key == pygame.K_r:
                    DrawMap(LEVELS_TEMPLATE[CURRENT_LEVEL], DISPLAY, player1, player2)
                    LEVELS[CURRENT_LEVEL] =copy.deepcopy(LEVELS_TEMPLATE[CURRENT_LEVEL])

                #Skip level with comma
                if event.key == pygame.K_COMMA:
                    NextLevel(DISPLAY, player1, player2)
                    FINISH_CELLS_STATE = [False, False]


            
                
            #Detect finish cell
            if(FINISH_CELLS_STATE == [True, True]):
                NextLevel(DISPLAY, player1, player2)
            FINISH_CELLS_STATE = [False, False]


            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main()