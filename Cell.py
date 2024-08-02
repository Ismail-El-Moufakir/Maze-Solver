import numpy as np 

class Cell:
    def __init__(self,width,height,x,y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Walls = {"up":1,"down":1,"left":1,"right":1}   
        self.visited = False
        self.Vis_Path = False
        


        