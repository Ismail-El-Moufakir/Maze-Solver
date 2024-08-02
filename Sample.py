import pygame
import Maze
import Maze_Gen
import Path_Find
import agent
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

maze = Maze.Maze(300,300,30,30)
Maze_Gen.R_First_Depth_Research(maze,screen)
#Maze_Gen.Prim(maze)
#Maze_Gen.Krusal(maze)
agent = agent.Agent(maze)
Path_Find = Path_Find.Agent(0,0)
Rows = maze.height // maze.CellH
Cols = maze.width // maze.CellW
#Path_Find.DFS(maze,Rows -1,Cols -1,screen)
#Path_Find.A_Start(maze,Rows-1,Cols-1,screen)
agent.train(maze,screen)
agent.find_path(maze,screen)
while running:
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     screen.fill("white")
     
     maze.Draw_Maze(screen)
     pygame.display.flip()
pygame.quit()
