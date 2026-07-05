import numpy as np

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        dy = y2 - y1
        dx = x2 - x1

        if(dy == 0):
            m = 0
        elif(dx == 0):
            m = 10000
        else:
            m = dy / dx

        self.m = m
        if (m > 10 or m < -10):
            self.direction = "vertical"
        else:
            self.direction = "horizontal"