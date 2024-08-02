import Maze
import Cell
import time
import pygame

import numpy as np
# Randomized First depth research
def R_First_Depth_Research(maze :Maze.Maze,Screen):
    Visited_Count = 1
    current_i = 0
    current_j = 0
    maze.Mtx[current_i][current_j].visited = True
    Memory = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
   
    newi,newj = 0,0
    while Visited_Count != (maze.width // maze.CellW )*(maze.height // maze.CellH):
        
        np.random.shuffle(directions)
        randomDirection = np.random.randint(0,4)
        tried = [0,0,0,0]
        attemp = 0
        #time.sleep(1)
        while attemp < 4:
             newi = current_i + directions[randomDirection][0]
             newj = current_j + directions[randomDirection][1]
             print(f"left attemp {attemp}")
             print(f"newi {newi} newj {newj}")
             print(f"cell visited {Visited_Count}")
             if newi >= 0 and newi< maze.height// maze.CellH and newj >=0 and newj < maze.width// maze.CellW and maze.Mtx[newi][newj].visited == False:
                 RemoveWalls(maze,current_i,current_j,newi,newj)
                 maze.Mtx[newi][newj].visited = True
                 Visited_Count +=1
                 Memory.append((current_i,current_j))
                 current_i = newi
                 current_j = newj
                 print("newi and newj found break attemp")
                 break
             else:
                 print(f"attemp {attemp}")
                 print(f"tried {tried}")
                 randomDirection = np.random.randint(0,4)
                 if tried[randomDirection]==0 :
                     attemp  += 1
                     tried[randomDirection]= 1
                 if attemp == 4:
                    Mem_Cel = Memory.pop()
                    current_i = Mem_Cel[0]
                    current_j = Mem_Cel[1]
             Screen.fill("white")
     
             maze.Draw_Maze(Screen)
             pygame.display.flip()
                        
def Prim(maze:Maze.Maze):
    Wall_List = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)] # UP DOWN RIGHT LEFT
    #the visited attribute of Cell play the role of Maze Part*
    current_i,current_j = 0,0
    maze.Mtx[current_i][current_j].visited = True
    neighbourWalls(maze,0,0,Wall_List)
    while len(Wall_List) !=0:
        np.random.shuffle(Wall_List)
        PickedWall = Wall_List.pop()
        ni, nj, direction = PickedWall
        di, dj = directions[direction]
        ci, cj = ni + di, nj + dj
        if 0 <= ci < maze.height // maze.CellH and 0 <= cj < maze.width // maze.CellW:
            if maze.Mtx[ci][cj].visited and not maze.Mtx[ni][nj].visited:
                neighbourWalls(maze,ni,nj,Wall_List)
                maze.Mtx[ni][nj].visited = True
                RemoveWalls(maze,ci,cj,ni,nj)
            if maze.Mtx[ni][nj].visited and not maze.Mtx[ci][cj].visited:
                neighbourWalls(maze,ci,cj,Wall_List)
                maze.Mtx[ci][cj].visited = True
                RemoveWalls(maze,ci,cj,ni,nj)
            
            print(f"WallList {len(Wall_List)}")
def Krusal(maze:Maze.Maze):
    num_rows = maze.height // maze.CellH
    num_cols = maze.width // maze.CellW
    Cells = set(frozenset({(i,j)}) for i in range(num_rows) for j in range(num_cols))
    while len(maze.Walls)!=0:
        np.random.shuffle(maze.Walls)
        PickedWall = maze.Walls.pop()
        cell1,cell2 = PickedWall
        set1,set2 = find_set(cell1,Cells),find_set(cell2,Cells)
        if set1 != set2 :
            Cells.remove(set1)
            Cells.remove(set2)
            Cells.add(set1.union(set2))
            RemoveWalls(maze,cell1[0],cell1[1],cell2[0],cell2[1])




def find_set(cell,set):
            for s in set:
                if cell in s:
                    return s
            return None

    
        
def count_total_walls(maze):
    total_walls = 0
    for i in range(maze.height // maze.CellH):
        for j in range(maze.width // maze.CellW):
            if maze.Mtx[i][j].Walls["right"]:
                total_walls += 1
            if maze.Mtx[i][j].Walls["down"]:
                total_walls += 1


                 
def RemoveWalls(maze: Maze.Maze,currenti,currentj,newi,newj):
    if currenti - newi == 1:
        maze.Mtx[currenti][currentj].Walls["up"] = 0
        maze.Mtx[newi][newj].Walls["down"] = 0
    elif currenti - newi == -1:
        maze.Mtx[currenti][currentj].Walls["down"] = 0
        maze.Mtx[newi][newj].Walls["up"] = 0
    elif currentj - newj == 1:
        maze.Mtx[currenti][currentj].Walls["left"] = 0
        maze.Mtx[newi][newj].Walls["right"] = 0
    elif currentj - newj == -1:
        maze.Mtx[currenti][currentj].Walls["right"] = 0
        maze.Mtx[newi][newj].Walls["left"] = 0
        

def neighbourWalls(Maze: Maze.Maze,current_i,current_j,WallList):
    directions = [(-1,0),(1,0),(0,-1),(0,1)] # UP DOWN left right
    for k in range(len(directions)):
        newi = current_i + directions[k][0]
        newj = current_j + directions[k][1]
        if newi>=0 and newi< Maze.height//Maze.CellH and newj>=0 and newj< Maze.width//Maze.CellW and Maze.Mtx[newi][newj].visited == False:
            if newi - current_i ==  1:
                WallList.append((newi,newj,0)) #UP WALL
            elif newi - current_i == -1:
                WallList.append((newi,newj,1)) #DOWN WALL
            elif newj - current_j == 1:
                 WallList.append((newi,newj,2)) #RIGHT WALL
            elif newj - current_j == -1:
                 WallList.append((newi,newj,3)) #LEFT WALL
            




        



