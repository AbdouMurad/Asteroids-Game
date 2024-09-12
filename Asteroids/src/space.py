from const import *
from entities import *
import random
import math

class Space:
    def __init__(self):
        player = Player([WIDTH/2, HEIGHT/2])
        health_bar = Health_Bar()
        PW_bar = Proton_Wave_Bar()
        PS_bar = Phase_shift_bar()
        self.health_bar = health_bar
        self.player = player
        self.Proton_Wave_Bar = PW_bar
        self.Phase_shift_bar = PS_bar
        self.BlankBars = PowerUpsEmpty()
        self.Bars = PowerUps()
        self.free_time_bar = Time_freeze_bar()

        self.Game_Over = Game_Over()




       
class Level_Manager:

    def __init__(self):
        self.spaceship_coord = [0,0]

        self.enemies = []
        self.asteroids = []
        self.level = 12
        self.destroyed = 0
        self.enemies_destroyed = 0
        self.spawned = 0
        self.enemies

        self.PW = False
        self.DS = False
        self.Ammo_Boost = False
        self.Health = False

    
    def new_level(self):
        self.level += 1
        for _ in range(self.level):
            coord, direction, speed = self.get_attributes()
            self.asteroids.append(Asteroid(coord, direction, speed))
        self.destroyed = 0
        
        for _ in range(int(self.level/3)):
            coord, _, _ = self.get_attributes()
            self.enemies.append(Enemy(coord))
        self.enemies_destroyed = 0
    def asteroid_destroyed(self, name, asteroid_coord):
        self.destroyed += 1
        
        match name:
            case "BIG":
                coord, direction, speed = self.get_attributes(mass = MASS_MEDIUM)
                coord[0] = asteroid_coord[0] - random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                coord[1] = asteroid_coord[1] - random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                self.asteroids.append(Asteroid(coord, direction, speed, size = 60))

                coord, direction, speed = self.get_attributes(mass = MASS_MEDIUM)
                coord[0] = asteroid_coord[0] + random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                coord[1] = asteroid_coord[1] + random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                
                self.asteroids.append(Asteroid(coord, direction, speed, size = 60))
                
                
            case "MEDIUM":
                coord, direction, speed = self.get_attributes(mass = MASS_SMALL)
                coord[0] = asteroid_coord[0] + random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                coord[1] = asteroid_coord[1] + random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                self.asteroids.append(Asteroid(coord, direction, speed, size = 40))
                

                coord, direction, speed = self.get_attributes(mass = MASS_SMALL)
                coord[0] = asteroid_coord[0] - random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                coord[1] = asteroid_coord[1] - random.randint(-ASTEROID_SPAWN_OFFSET, ASTEROID_SPAWN_OFFSET)
                self.asteroids.append(Asteroid(coord, direction, speed, size = 40))
                

            case "SMALL":
                int = random.randint(1,12)
                match int:
                    case 1: self.PW = True
                    case 2: self.DS = True
                    case 3: self.Ammo_Boost = True
                    case 4: self.Health = True    
    def get_asteroids(self):
        return self.asteroids 
    def get_attributes(self, mass = MASS_BIG):
        y = random.randint(0, HEIGHT)
        x = random.randint(0, WIDTH)
        speed = random.randint(1600/mass, 19200/mass)
        direction = random.randint(0, 360)

        while math.dist(self.spaceship_coord , [x,y]) < MIN_SPAWN_DISTANCE:
            y = random.randint(0, HEIGHT)
            x = random.randint(0, WIDTH)

        return [x,y], direction, speed

