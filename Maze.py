import pygame 
import numpy as np
import Cell

class Maze:
    def __init__(self, w, h, CellW, CellH):
        self.Mtx = np.array([[Cell.Cell(CellW, CellH, j * CellW, i * CellH) for j in range(w // CellW)] for i in range(h // CellH)])
        self.width = w
        self.height = h
        self.CellW = CellW
        self.CellH = CellH
        
        self.Walls = []
        for i in range(self.height // self.CellH):
            for j in range(self.width // self.CellW):
                if i > 0:
                    # Vertical wall between cells (i-1, j) and (i, j)
                    self.Walls.append(((i-1, j), (i, j)))
                if j > 0:
                    # Horizontal wall between cells (i, j-1) and (i, j)
                    self.Walls.append(((i, j-1), (i, j)))

    def Draw_Maze(self, Screen):
        if len(self.Mtx) == 0:
            return -1
        
        # Set background color
        Screen.fill((240, 240, 240))  # light grey background
        
        # Initialize font
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        
        # Create the text surface
        text_surface = font.render('Maze Solver', True, (0, 0, 0))
        
        # Get the text rectangle
        text_rect = text_surface.get_rect(center=(self.width + 100, 20))
        
        # Blit the text surface onto the screen
        Screen.blit(text_surface, text_rect)

        # Define the line thickness
        line_thickness = 4
        
        # Draw the maze
        for i in range(len(self.Mtx)):
            for j in range(len(self.Mtx[0])):
                #up
                if self.Mtx[i][j].Walls["up"] == 1:
                    pygame.draw.line(Screen, "black", (self.Mtx[i][j].x, self.Mtx[i][j].y), (self.Mtx[i][j].x + self.Mtx[i][j].width, self.Mtx[i][j].y), line_thickness)
                #down
                if self.Mtx[i][j].Walls["down"] == 1:
                    pygame.draw.line(Screen, "black", (self.Mtx[i][j].x, self.Mtx[i][j].y + self.Mtx[i][j].height), (self.Mtx[i][j].x + self.Mtx[i][j].width, self.Mtx[i][j].y + self.Mtx[i][j].height), line_thickness)
                #left
                if self.Mtx[i][j].Walls["left"] == 1:
                    pygame.draw.line(Screen, "black", (self.Mtx[i][j].x, self.Mtx[i][j].y), (self.Mtx[i][j].x, self.Mtx[i][j].y + self.Mtx[i][j].height), line_thickness)
                #right
                if self.Mtx[i][j].Walls["right"] == 1:
                    pygame.draw.line(Screen, "black", (self.Mtx[i][j].x + self.Mtx[i][j].width, self.Mtx[i][j].y), (self.Mtx[i][j].x + self.Mtx[i][j].width, self.Mtx[i][j].y + self.Mtx[i][j].height), line_thickness)
