import pygame
from collections import deque

pygame.init()

w = (255, 255, 255)
r = (255, 0, 0)
g = (0, 255, 0)
blue = (0, 0, 255)
y = (255, 255, 0)
b = (0, 0, 0)

width, height = 800, 800
rows, cols = 20, 20
cell = width // rows

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("BFS")


class Cell:
    def __init__(self, rows, cols):
        self.row = rows
        self.col = cols
        self.color = w
        self.neighbors = []

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.row * cell, self.col * cell, cell, cell))
        pygame.draw.rect(win, b, (self.row * cell, self.col * cell, cell, cell), 1)

    def add_neighbors(self, grid):
        if self.row < cols - 1:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < rows - 1:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, cols):
    grid = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
    for row in grid:
        for cell in row:
            cell.add_neighbors(grid)
    return grid

def draw_grid(win, rows, cols):
    for i in range(rows):
        pygame.draw.line(win, b, (cell * i, 0), (cell * i, height))
        for j in range(cols):
            pygame.draw.line(win, b, (0, cell * j), (width, cell * j))

def draw(win, grid):
    win.fill(w)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid(win, rows, cols)
    pygame.display.update()


def bfs(grid, start, end):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == end:
            temp = current
            while temp in came_from:
                temp.color = y
                temp = came_from[temp]
            end.color = g
            start.color = r
            return True
        for neighbor in current.neighbors:
            if neighbor.color != b and neighbor not in visited:
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.color = blue
                visited.add(neighbor)
                draw(WIN, grid)
                pygame.time.wait(50)  
    return False


def main():
    grid = make_grid(rows, cols)
    start = None
    end = None
    run = True

    while run:
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  
                pos = pygame.mouse.get_pos()
                row, col = pos[0] // cell, pos[1] // cell
                clicked_cell = grid[row][col]  
                if not start:
                    start = clicked_cell
                    start.color = r
                elif not end and clicked_cell != start:
                    end = clicked_cell
                    end.color = g
                elif clicked_cell != start and clicked_cell != end:
                    clicked_cell.color = b
            elif pygame.mouse.get_pressed()[2]:  
                pos = pygame.mouse.get_pos()
                row, col = pos[0] // cell, pos[1] // cell
                clicked_cell = grid[row][col]  
                clicked_cell.color = w
                if clicked_cell == start:
                    start = None
                elif clicked_cell == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    bfs(grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, cols)
    pygame.quit()

if __name__ == "__main__":
    main()
