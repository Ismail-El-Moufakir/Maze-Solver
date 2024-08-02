import Maze
import pygame
import numpy as np

class Agent:
    def __init__(self, maze: Maze.Maze):
        self.rows = maze.height // maze.CellH
        self.cols = maze.width // maze.CellW
        self.Q_Mtx = np.zeros((self.rows * self.cols, 4))  # Q-Matrix initialized with zeros
        self.epsilon = 0.2
        self.learningRate = 0.5
        self.discountCoef = 0.9

    def choose_action(self):
        if np.random.rand() < self.epsilon:  # epsilon-greedy policy
            return np.random.randint(0, 4)
        else:
            return np.argmax(self.Q_Mtx[self.currentState])

    def get_coordinates(self, state):
        return state // self.cols, state % self.cols

    def train(self, maze: Maze.Maze, screen, iterations=1000):
        for i in range(iterations):
            self.currentState = 0
            ci, cj = 0, 0
            path = []
            while ci != self.rows - 1 or cj != self.cols - 1:
                screen.fill("white")
                maze.Draw_Maze(screen)
                action = self.choose_action()
                reward = 0
                ci, cj = self.get_coordinates(self.currentState)
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                dir = directions[action]
                ni, nj = ci + dir[0], cj + dir[1]

                if ni < 0 or ni >= self.rows or nj < 0 or nj >= self.cols:
                    reward = -100
                    newState = self.currentState
                else:
                    newState = ni * self.cols + nj
                    if maze.Mtx[ni][nj].visited:
                        reward = -10
                    if (maze.Mtx[ci][cj].Walls["up"] == 1 and dir == (-1, 0)) or \
                       (maze.Mtx[ci][cj].Walls["down"] == 1 and dir == (1, 0)) or \
                       (maze.Mtx[ci][cj].Walls["left"] == 1 and dir == (0, -1)) or \
                       (maze.Mtx[ci][cj].Walls["right"] == 1 and dir == (0, 1)):
                        reward = -20

                self.Q_Mtx[self.currentState][action] = (1 - self.learningRate) * self.Q_Mtx[self.currentState][action] + \
                    self.learningRate * (reward + self.discountCoef * np.max(self.Q_Mtx[newState]))

                self.currentState = newState
                ci, cj = self.get_coordinates(self.currentState)
                path.append((ci, cj))
                for cell in path:
                    pygame.draw.circle(screen, "green",
                                       (maze.Mtx[cell[0]][cell[1]].x + maze.CellW // 2,
                                        maze.Mtx[cell[0]][cell[1]].y + maze.CellH // 2), 5)
                pygame.display.flip()

                if ci == self.rows - 1 and cj == self.cols - 1:
                    print(f"Solution found in iteration {i}")
                    break

    def find_path(self, maze: Maze, screen):
        ci, cj = 0, 0
        path = []
        while ci != self.rows - 1 or cj != self.cols - 1:
            screen.fill("white")
            maze.Draw_Maze(screen)
            state = ci * self.cols + cj
            action = np.argmax(self.Q_Mtx[state])
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            dir = directions[action]

            ci, cj = ci + dir[0], cj + dir[1]
            path.append((ci, cj))

            for cell in path:
                pygame.draw.circle(screen, "blue",
                                   (maze.Mtx[cell[0]][cell[1]].x + maze.CellW // 2,
                                    maze.Mtx[cell[0]][cell[1]].y + maze.CellH // 2), 5)
            pygame.display.flip()

            if ci == self.rows - 1 and cj == self.cols - 1:
                print("Reached the goal!")
                print("Path: ", path)
                return path

