from const import *
import random

class Config:
    def __init__(self):
        self.coord = []
        self.create_stars()
    def create_stars(self):
        for x in range(int(WIDTH/15 +1)):
            for y in range(int(HEIGHT/15 +1)):
                self.coord.append((x*15 + random.randint(-8, 8), y*15 + random.randint(-8,8), random.randint(0, 255)))
                
        return self.coord
