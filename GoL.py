################################################################################################
# a simple Game of Life implementation
# (c) JP Darsonville 2019
# GPL v3
################################################################################################

# handle dependencies
from copy import copy, deepcopy
import pygame
import random
import time
import sys

# constants are declared below
MAX_X = 300
MAX_Y = 150
OFFSET_X = 5
OFFSET_Y = 5
MAX_GEN = 10000
SCALE = 4
START_GRID_DENSITY = 30 # grid density between 0 and 100 (-1 for empty grid)
SLEEP_TIME = 0 # wait time between generations

# window parameters
background_colour = (255,255,255)
foreground_color = (0,0,0)
##width = (MAX_X + OFFSET_X * 2) * SCALE
##height = (MAX_Y + OFFSET_Y * 2) * SCALE
width = (MAX_X + 1) * SCALE
height = (MAX_Y + 1) * SCALE

# used for increments
i = 0
j = 0
gen = 0

# create the two grids needed to store in memory the gameboards, G1 = current grid, G2 = old aka previous gen grid
G1 = [ [ 0 for i in range(0, MAX_Y + 1) ] for j in range(0, MAX_X + 1) ]
G2 = [ [ 0 for i in range(0, MAX_Y + 1) ] for j in range(0, MAX_X + 1) ]

################################################################
#  plots output on the screen based on input coordinates
################################################################
def plot (x, y, color):
    if color == 1:
        sel_color = (0,0,0)
    else:
        sel_color = (255,255,255)
    pygame.draw.rect(screen, sel_color, [(x)* SCALE, (y) * SCALE, SCALE, SCALE])

################################################################
# define function that test if life should emerge
################################################################
def cell_test_life(x, y):
    testval = 0
    for i in range (-1, 2):
        for j in range (-1, 2):
            testval = testval + G1[x + i][y + j]
    testval = testval - G1[x][y] # ensure tested cell does not count if alive
    if testval == 2 and G1[x][y] == 1:
        return 1
    elif testval == 3:
        return 1
    else:
        return 0

# generate a random start grid
for i in range (1, MAX_X):
    for j in range (1, MAX_Y):
        if random.randint(0,100) <= START_GRID_DENSITY:
            G1[i][j] = random.randint (0,1)

# open window and populate start grid
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game of Life by JP Darsonville')
screen.fill(background_colour)
for i in range (1, MAX_X):
    for j in range (1, MAX_Y):
        plot (i,j, G1[i][j])
pygame.display.flip()

# phase 1 - configure cell positions through mouse input
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            print (mx, my)
            x = int(mx / SCALE)
            y = int(my / SCALE)
            if e.button == 1:
                G1[x][y] = 1
                plot(x, y, 1)
            if e.button == 3:
                G1[x][y] = 0
                plot (x, y, 0)
            pygame.display.flip()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                running = False

pygame.display.flip()


# phase 2 - begin game and increment from the planned number of generations
for gen in range(1, MAX_GEN):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in range (1, MAX_X):
        for j in range (1, MAX_Y):
            G2[i][j] = cell_test_life(i,j)
            plot (i,j, G2[i][j])
    G1 = deepcopy(G2)
    pygame.display.set_caption('Generation:' + str(gen))
    pygame.display.flip()
    if SLEEP_TIME != 0:
        time.sleep(SLEEP_TIME)

# end simulation / wait for user input to remove grid
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

# end program
