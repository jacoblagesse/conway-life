import pygame
import numpy as np
import scipy.signal
import math
import time

black = (0, 0, 0)
white = (200, 200, 200)

x_dim = 100
y_dim = 80

cell_size = 10

adj = np.array([[1,1,1], [1,0,1], [1,1,1]])

def update(grid):
    sums = scipy.signal.convolve2d(grid, adj, mode='same')

    for x in range(0, x_dim):
        for y in range(0, y_dim):
            if grid[x][y]:
                if sums[x][y] < 2 or sums[x][y] > 3:
                    grid[x][y] = 0
            else:
                if sums[x][y] == 3:
                    grid[x][y] = 1

    return grid

def draw(grid):
    for x in range(0, x_dim):
        for y in range(0, y_dim):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if grid[x][y]:
                pygame.draw.rect(screen, white, rect, 0)
            else:
                pygame.draw.rect(screen, black, rect, 0)

def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((x_dim*cell_size, y_dim*cell_size))
    clock = pygame.time.Clock()
    screen.fill(black)

    grid = np.zeros((x_dim, y_dim), dtype=int)

    paused = True
    dragging = False

    while True:
        if not paused:
            update(grid)
            time.sleep(0.1)
        draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                pos = pygame.mouse.get_pos()
                grid[math.trunc(pos[0]/10)][math.trunc(pos[1]/10)] = not grid[math.trunc(pos[0]/10)][math.trunc(pos[1]/10)]
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos = pygame.mouse.get_pos()
                    grid[math.trunc(pos[0]/10)][math.trunc(pos[1]/10)] = 1
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        pygame.display.update()

main()