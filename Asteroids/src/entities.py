import pygame
import math

from math import *
from const import *

class Health_Bar:
    def __init__(self, health = HEALTH, coord = [120, HEIGHT - 40]):
        self.max_health = health
        self.img = pygame.image.load('assets/healthbar.png')
        self.texture_rect = self.img.get_rect(center = coord)

    def draw(self, health, surface):
        ratio = health/self.max_health

        height = self.texture_rect.height
        width = self.texture_rect.width

        pygame.draw.rect(surface, "green", ((120 - width/2) + 18, (HEIGHT - 38) - height/2, (width-20)*ratio, height - 4))
class Proton_Wave_Bar:
    def __init__(self, reload_time = PW_fire_rate, coord = [120, HEIGHT - 65]):
        self.reload_time = reload_time
        self.img = pygame.image.load('assets/PWbar.png')
        self.texture_rect = self.img.get_rect(center = coord) 
    def draw(self, time, surface):
        if time < self.reload_time:
            ratio = time/self.reload_time
        else:
            ratio = 1

        height = self.texture_rect.height
        width = self.texture_rect.width

        pygame.draw.rect(surface, "blue", ((120 - width/2) + 18, (HEIGHT - 63) - height/2, (width-20)*ratio, height - 4))
class PowerUpsEmpty:
    def __init__(self):
        self.scoreImg = pygame.image.load("assets/DoubleScoreBlank.png")
        self.bulletImg = pygame.image.load("assets/BulletPowerUpBlank.png")
        self.protonImg =  pygame.image.load("assets/ProtonWavePowerUpBlank.png")

        self.scoreRect = self.scoreImg.get_rect(center = [250, HEIGHT - 50])
        self.bulletRect = self.scoreImg.get_rect(center = [290, HEIGHT - 50])
        self.pwRect = self.scoreImg.get_rect(center = [330, HEIGHT - 50])

class PowerUps:
    def __init__(self):
        self.scoreImg = pygame.image.load("assets/DoubleScore.png")
        self.bulletImg = pygame.image.load("assets/BulletPowerUp.png")
        self.protonImg =  pygame.image.load("assets/ProtonWavePowerUp.png")

        self.scoreRect = self.scoreImg.get_rect(center = [250, HEIGHT - 50])
        self.bulletRect = self.scoreImg.get_rect(center = [290, HEIGHT - 50])
        self.pwRect = self.scoreImg.get_rect(center = [330, HEIGHT - 50])
class Player:
    def __init__(self, coord, direction = 0, velocity = [0,0]):
        self.coord = coord
        self.velocity = velocity
        self.acceleration = 0
        self.force = 0
        self.direction = direction
        self.PW_time = 10

        self.score = 0
        self.health = HEALTH
        self.mass = MASS


        self.img = pygame.image.load('assets/spaceship.png')
        self.texture_rect = self.img.get_rect(center = self.coord)

        
        
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

        
    #movement and applying forces
    def apply_force(self, force, delta_time = 0):

        self.acceleration = force/self.mass
        self.velocity[0] += delta_time * self.acceleration * sin(self.direction*pi/180)
        self.velocity[1] += delta_time * self.acceleration * cos(self.direction*pi/180)
        displacementX = self.velocity[0] * delta_time
        displacementY = self.velocity[1] * delta_time
        #print(displacementX, displacementY, "s")
        self.coord[0] -= displacementX
        self.coord[1] -= displacementY

        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        #BORDER
        if self.coord[1] > HEIGHT:
            self.coord[1] = 0
        elif self.coord[1] < 0:
            self.coord[1] = HEIGHT

        if self.coord[0] > WIDTH:
            self.coord[0] = 0
        elif self.coord[0] < 0:
            self.coord[0] = WIDTH


        #CREATING IMAGE TO RENDER
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

    def bullet_position(self):
        return self.coord
    def bullet_direction(self):
        return self.direction
    def bullet_velocity(self):
        return self.velocity
    def Gravity(self, direction, distance, mass, dt):
       
        force = G*self.mass*mass/distance

        acceleration = force/self.mass
        self.velocity[0] -= acceleration * sin(direction) * dt
        self.velocity[1] -= acceleration * cos(direction) * dt    


class Enemy:
    def __init__(self, coord, direction = 0, velocity = [0,0]):
        self.coord = coord
        self.velocity = velocity
        self.acceleration = 0
        self.force = 0
        self.direction = direction 

        self.health = HEALTH
        self.mass = MASS

        self.img = pygame.image.load('assets/enemySpaceship.png')
        self.texture_rect = self.img.get_rect(center = self.coord)

        self.turning = False
        self.turn_amount = 0
        
        self.bullets = []
        self.fireTime = 0

        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

            #movement and applying forces
    def apply_force(self, force, delta_time = 0):
        self.acceleration = force/self.mass
        self.velocity[0] += delta_time * self.acceleration * sin(self.direction*pi/180)
        self.velocity[1] += delta_time * self.acceleration * cos(self.direction*pi/180)
        displacementX = self.velocity[0] * delta_time
        displacementY = self.velocity[1] * delta_time
        
        self.coord[0] -= displacementX
        self.coord[1] -= displacementY

        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        #BORDER
        if self.coord[1] > HEIGHT:
            self.coord[1] = 0
        elif self.coord[1] < 0:
            self.coord[1] = HEIGHT

        if self.coord[0] > WIDTH:
            self.coord[0] = 0
        elif self.coord[0] < 0:
            self.coord[0] = WIDTH


        #CREATING IMAGE TO RENDER
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

    

    def turn(self, delta_time = 0):
        
        #direction : 1 = left -1 = right
        if self.turning and self.turn_amount > 0:
            self.direction += ROTATE_SPEED*delta_time
            self.turn_amount -= ROTATE_SPEED*delta_time
            if self.turn_amount < 5:
                self.turn_amount = 0
                self.turning = False
  

        elif self.turning and self.turn_amount < 0:
            self.direction -= ROTATE_SPEED*delta_time
            self.turn_amount += ROTATE_SPEED*delta_time
            if self.turn_amount > -5:
                self.turn_amount = 0
                self.turning = False


    
        #CREATING IMAGE TO RENDER
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

    def player_info(self, coord, player_direction, velocity, acceleration):
        self.playerInfo = [coord, player_direction, velocity, acceleration]
    
    def bullet_position(self):
        return self.coord
    def bullet_direction(self):
        return self.direction
    def bullet_velocity(self):
        return self.velocity
class Bullets:
    def __init__(self, direction, pos, spaceship_velocity, space_ship_coord = None, init_pos = None, spaceship_velocity_usedByEnemy =  None):
        self.direction = direction
        self.init_pos = init_pos
        self.pos = pos

        self.spaceship_velocity = spaceship_velocity
        self.spaceship_velocity_usedByEnemy = spaceship_velocity_usedByEnemy

        self.space_ship_coord = space_ship_coord
        
        self.speed = BULLET_SPEED
        
        self.img = pygame.image.load('assets/bullet.png')
        self.texture_rect = self.img.get_rect(center = pos)
        
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = pos
        
        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

        self.time = 0

            
    def move(self, delta_time = 0):

        displacementX = (self.speed *  sin(self.direction * pi/180) + self.spaceship_velocity[0]) * delta_time
        displacementY = (self.speed *  cos(self.direction * pi/180) + self.spaceship_velocity[1]) * delta_time
        
        self.pos[0] -= displacementX
        self.pos[1] -= displacementY

        #BORDER
        #if self.pos[1] > HEIGHT:
         #   self.pos[1] = 0
        #elif self.pos[1] < 0:
         #   self.pos[1] = HEIGHT

        #if self.pos[0] > WIDTH:
         #   self.pos[0] = 0
        #elif self.pos[0] < 0:
         #   self.pos[0] = WIDTH
            

        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.pos

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

        self.time += delta_time


class Proton_Wave:
    def __init__(self, coord):
        self.center = coord
        self.speed = GROWTH_SPEED
        self.size = [80,80]
        self.img = pygame.image.load('assets/ProtonWave.png')
        self.img2 = pygame.transform.scale(self.img, self.size)
        self.texture_rect = self.img2.get_rect(center = self.center)
        

        self.mask = pygame.mask.from_surface(self.img2)
        self.mask_image = self.mask.to_surface()

        self.alive = 0
        
        
    def update(self, dt):
        self.size[0] += dt * GROWTH_SPEED
        self.size[1] += dt * GROWTH_SPEED

        self.alive += dt

        
        self.img2 = pygame.transform.scale(self.img, self.size)
        self.texture_rect = self.img2.get_rect(center = self.center)

        self.mask = pygame.mask.from_surface(self.img2)
        self.mask_image = self.mask.to_surface()
        
         
class Asteroid:
    def __init__(self, coord, direction, speed, size = 120):
        self.size = size
        self.coord = coord
        self.direction = direction
        self.speed = speed
        self.velocity = [self.speed * sin(self.direction * pi/180), self.speed * cos(self.direction * pi/180)]


        self.imgDirection = 0

        self.img = pygame.image.load(f'assets/asteroid{size}.png')
        self.texture_rect = self.img.get_rect(center = self.coord)
        
        self.rotatedSurf = pygame.transform.rotate(self.img, self.direction)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

        match size:
            case 120:
                self.name = "BIG"
                self.mass = MASS_BIG
                self.health = HEALTH_BIG
            case 60:
                self.name = "MEDIUM"
                self.mass = MASS_MEDIUM
                self.health = HEALTH_MEDIUM
            case 40:
                self.name = "SMALL"
                self.mass = MASS_SMALL
                self.health = HEALTH_SMALL

    def move(self, delta_time):
        displacementX = self.velocity[0] * delta_time
        displacementY = self.velocity[1] * delta_time 
        
        self.coord[0] -= displacementX
        self.coord[1] -= displacementY

        if self.coord[1] > HEIGHT:
            self.coord[1] = 0
        elif self.coord[1] < 0:
            self.coord[1] = HEIGHT

        if self.coord[0] > WIDTH:
            self.coord[0] = 0
        elif self.coord[0] < 0:
            self.coord[0] = WIDTH
        
        self.imgDirection += ASTEROID_ROTATE_SPEED*delta_time * self.speed


        self.rotatedSurf = pygame.transform.rotate(self.img, self.imgDirection)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = self.coord

        self.mask = pygame.mask.from_surface(self.rotatedSurf)
        self.mask_image = self.mask.to_surface()

        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
    def Gravity(self,  dt, spaceship_coord):
        distance = math.dist(self.coord, spaceship_coord)
        force = G * self.mass * MASS / distance
        if (spaceship_coord[1])-(self.coord[1]) != 0:
            direction = math.atan((spaceship_coord[0]-self.coord[0])/((spaceship_coord[1])-(self.coord[1])))
        if spaceship_coord[1] >= self.coord[1]:
            if spaceship_coord[0] > self.coord[0]:
                direction -= pi
                
            else:
                direction += pi
                
        
        acceleration = force/self.mass
        self.velocity[0] += acceleration * sin(direction) * dt
        self.velocity[1] += acceleration * cos(direction) * dt

        return direction, distance, self.mass

    def Take_Damage(self, bullet_speed):
        damage = bullet_speed/BULLET_SPEED * DAMAGE
        self.health -= damage


        



        
        



        



    





        
        