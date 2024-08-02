import pygame
import Maze
import time
from heapq import heappop, heappush
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Maze Solver using DFS algorithm
    def DFS(self, maze: Maze.Maze, target_i, target_j, screen):
        path = [(0, 0)]
        rows_count = maze.height // maze.CellH
        cols_count = maze.width // maze.CellW
        current_i, current_j = 0, 0
        maze.Mtx[current_i][current_j].Vis_Path = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill("white")
            maze.Draw_Maze(screen)

            if current_i == target_i and current_j == target_j:
                print("Solution found")
                # Draw the path
                for cell in path:
                    pygame.draw.circle(screen, "green", 
                                       (maze.Mtx[cell[0]][cell[1]].x + maze.CellW // 2, 
                                        maze.Mtx[cell[0]][cell[1]].y + maze.CellH // 2), 5)
                pygame.display.flip()
                break

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT
            found_next = False

            for dir in directions:
                new_i, new_j = current_i + dir[0], current_j + dir[1]

                if 0 <= new_i < rows_count and 0 <= new_j < cols_count and not maze.Mtx[new_i][new_j].Vis_Path:
                    if (dir == (-1, 0) and maze.Mtx[current_i][current_j].Walls["up"]) or \
                       (dir == (1, 0) and maze.Mtx[current_i][current_j].Walls["down"]) or \
                       (dir == (0, -1) and maze.Mtx[current_i][current_j].Walls["left"]) or \
                       (dir == (0, 1) and maze.Mtx[current_i][current_j].Walls["right"]):
                        continue

                    path.append((new_i, new_j))
                    current_i, current_j = new_i, new_j
                    maze.Mtx[new_i][new_j].Vis_Path = True
                    pygame.draw.circle(screen, "green", 
                                       (maze.Mtx[new_i][new_j].x + maze.CellW // 2, 
                                        maze.Mtx[new_i][new_j].y + maze.CellH // 2), 5)
                    found_next = True
                    break

            if not found_next:
                # If no direction is found, backtrack
                current_i, current_j = path.pop()
                if len(path) == 0:
                    print("No solution found")
                    break

            # Draw the current path
            for cell in path:
                pygame.draw.circle(screen, "green", 
                                   (maze.Mtx[cell[0]][cell[1]].x + maze.CellW // 2, 
                                    maze.Mtx[cell[0]][cell[1]].y + maze.CellH // 2), 5)

            pygame.display.flip()
            time.sleep(0.05)  
    #Maze Solving Algorithm using A Start function:
    def heuristic(self,current_i,current_j,target_i,target_j):
        return  abs(target_i -current_i) +abs(target_j - current_j)


    def A_Start(self, maze, target_i, target_j, screen):
        def heuristic(current_i, current_j):
            return abs(target_i - current_i) + abs(target_j - current_j)

        Queue = []  # Queue to retrieve the Cell with the smallest F score
        Parent = {}  # Parent dictionary to track the path at the end
        g_score = {}  # g score of Cells
        f_score = {}  # f score of Cells f(n) = g(n) + h(n)

        # Starting with the start Cell
        start = (0, 0)
        g_score[start] = 0
        f_score[start] = g_score[start] + heuristic(0, 0)

        heappush(Queue, (f_score[start], start))
        current_i, current_j = start

        print("-------------------------------------------------")
        print("A Star Algo Starting ......")

        # While we don't find the solution
        while Queue:
            print(f"len of Queue {len(Queue)}")
            current_f_score, (current_i, current_j) = heappop(Queue)

            if (current_i, current_j) == (target_i, target_j):
                print("Solution found")
                self.draw_path(screen, maze, Parent, start, (target_i, target_j))
                return Parent

            maze.Mtx[current_i][current_j].Vis_Path = True

            # Draw the current cell as visited
            self.draw_cell(screen, maze, current_i, current_j, (255, 0, 0))  # Red color for visited
            pygame.display.update()
            pygame.time.delay(50)  # Add a delay for animation effect

            # Adding not visited neighbours to Queue heap
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP DOWN LEFT RIGHT
            for dir in directions:
                newi = current_i + dir[0]
                newj = current_j + dir[1]
                print(f"dir {dir} new_i {newi} newj {newj}")

                if 0 <= newi < maze.height // maze.CellH and 0 <= newj < maze.width // maze.CellW and not maze.Mtx[newi][newj].Vis_Path:
                    if dir == (-1, 0) and maze.Mtx[current_i][current_j].Walls["up"] == 1:
                        continue
                    if dir == (1, 0) and maze.Mtx[current_i][current_j].Walls["down"] == 1:
                        continue
                    if dir == (0, -1) and maze.Mtx[current_i][current_j].Walls["left"] == 1:
                        continue
                    if dir == (0, 1) and maze.Mtx[current_i][current_j].Walls["right"] == 1:
                        continue

                    # Add found Cell to Lists
                    print(f"found new cell: new_i {newi} newj {newj}")
                    tentative_g_score = g_score[(current_i, current_j)] + 1
                    if (newi, newj) not in g_score or tentative_g_score < g_score[(newi, newj)]:
                        g_score[(newi, newj)] = tentative_g_score
                        f_score[(newi, newj)] = tentative_g_score + heuristic(newi, newj)
                        Parent[(newi, newj)] = (current_i, current_j)
                        heappush(Queue, (f_score[(newi, newj)], (newi, newj)))

        print("No solution found")
        return None

    def draw_cell(self, screen, maze, i, j, color):
        cell = maze.Mtx[i][j]
        center_x = cell.x + cell.width // 2
        center_y = cell.y + cell.height // 2
        radius = min(cell.width, cell.height) // 4  # Adjust the radius as needed
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.rect(screen, (0, 0, 0), (cell.x, cell.y, cell.width, cell.height), 1)  # Cell border

    def draw_path(self, screen, maze, Parent, start, target):
        current = target
        while current != start:
            i, j = current
            self.draw_cell(screen, maze, i, j, (0, 255, 0))  # Green color for path
            pygame.display.update()
            pygame.time.delay(50)  # Add a delay for animation effect
            current = Parent[current]
        self.draw_cell(screen, maze, start[0], start[1], (0, 255, 0))  # Mark the start cell
        pygame.display.update()