import pygame
import sys

from config import Config
from const import *
from space import *
from entities import *


class Game:
    def __init__(self):
        self.config = Config()
        self.space = Space()
        self.level_manager = Level_Manager()

        self.text_font = pygame.font.SysFont(None, 24)
        self.enemies = [] #store enemies 
        self.bullets = [] #store player bullets
        self.enemy_bullets = [] #store enemy bullets
        self.score_multiplier = 1 #used for double score powerup

        self.hit = 0 #keeps track of hits from enemy to store percent of hits
        self.shot = 0  #store total amount of shots fired
        self.error_margin = 1 #used to calculate how much of a margin enemy should miss by depending on hit/shot ratio

        self.portal = None #store the portal which is active
        self.cimg = pygame.image.load("assets/crossair.png") #cross air image
        self.cimg_rect = self.cimg.get_rect

    def show_bg(self, surface):
        rect = (0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(surface, 'black', rect)
        
        #draw the stars
        for i in self.config.coord:
            rect = (i[0], i[1], 1 , 1)
            pygame.draw.rect(surface, (i[2], i[2], i[2]), rect)

    def show_bullets(self, surface, bullets, dt):
        self.bullets = bullets
        for bullet in bullets:
            surface.blit(bullet.rotatedSurf, bullet.rotatedRect)
        
            bullet.move(dt) #update the bullet based on the time that has passed

            if bullet.time >= BULLET_LIFE_SPAN: #once enough time has passed, remove bullet
                bullets.remove(bullet) 
 
    def show_asteroid(self, surface, asteroids, dt): #load and update asteroids

        self.level_manager.spaceship_coord = self.space.player.coord #store reference coords of spaceship

        for asteroid in asteroids:
            surface.blit(asteroid.rotatedSurf, asteroid.rotatedRect)

            asteroid.move(dt)
            direction, distance, mass = asteroid.Gravity(dt, self.space.player.coord) #gravity function applies force towards player on asteroid and return the direction, distance and mass of asteroid
            self.space.player.Gravity(direction , distance, mass, dt) #apply what was returned in gravity function 

            #CHECK COLLISION WITH PLAYER - have to use rotatedRect in order to get coord of top left point instead of using center
            off_setX = -asteroid.rotatedRect[0] + self.space.player.rotatedRect[0] 
            off_setY = -asteroid.rotatedRect[1] + self.space.player.rotatedRect[1] 
            if asteroid.mask.overlap(self.space.player.mask, (off_setX, off_setY)):
                self.space.player.health -= 20
                try:
                    asteroids.remove(asteroid)
                except: pass
                self.level_manager.asteroid_destroyed(asteroid.name, asteroid.coord)                
                if self.space.player.health <= 0:
                    #DEATH CODE
                    pygame.quit()
                    sys.exit()
                    

            #CHECK COLLISION WITH PW
            for PW in self.proton_wave:
                off_setX = -asteroid.rotatedRect[0] + PW.texture_rect[0] 
                off_setY = -asteroid.rotatedRect[1] + PW.texture_rect[1]             
                if asteroid.mask.overlap(PW.mask, (off_setX, off_setY)):
                    asteroid.Take_Damage(100000)
                    if asteroid.health <= 0:
                        if asteroid:
                            self.level_manager.asteroid_destroyed(asteroid.name, asteroid.coord)
                            self.space.player.score += 10 * self.score_multiplier
                            try:
                                asteroids.remove(asteroid)
                            except:pass
                                

                #COLLISION WITH ENEMY
                for enemy in self.enemies:
                    off_setX = -enemy.rotatedRect[0] + PW.texture_rect[0] 
                    off_setY = -enemy.rotatedRect[1] + PW.texture_rect[1]             
                    if enemy.mask.overlap(PW.mask, (off_setX, off_setY)):
                        enemy.health -= 100000
                        if enemy and enemy.health <= 0:
                            self.level_manager.enemies_destroyed += 1
                            self.enemies.remove(enemy)

            #CHECK COLLISION WITH BULLET
            for bullet in self.bullets:
                off_setX = -asteroid.rotatedRect[0] + bullet.rotatedRect[0] 
                off_setY = -asteroid.rotatedRect[1] + bullet.rotatedRect[1] 
                if asteroid.mask.overlap(bullet.mask, (off_setX, off_setY)):
                    self.bullets.remove(bullet)
                    asteroid.Take_Damage(bullet.speed)
                    if asteroid.health <= 0:
                        try:
                            self.level_manager.asteroid_destroyed(asteroid.name, asteroid.coord)
                            self.space.player.score += 10 * self.score_multiplier
                            asteroids.remove(asteroid)
                        except:
                            pass

    def show_player(self, surface):
        player = self.space.player
        surface.blit(player.rotatedSurf, player.rotatedRect)

    def update_enemy(self, enemies, surface, dt, target = [0,0]):
        self.enemies = enemies
        player = self.space.player
        for enemy in self.enemies:
            

            surface.blit(enemy.rotatedSurf, enemy.rotatedRect)

            enemy.player_info(player.coord, player.direction, player.velocity, player.acceleration) #

            #PREDICT LOCATION
            distance = math.sqrt((player.coord[0]-enemy.coord[0])**2+(player.coord[1]-enemy.coord[1])**2)
            if enemy.speed != 0:
                time = distance / (enemy.speed*self.error_margin + BULLET_SPEED)
            else:
                time = 0
            if time > 5: #only want to be able to predict ships that are at most 5 seconds away
                time = 5
            x = -player.velocity[0] * time + player.coord[0]
            y = -player.velocity[1] * time + player.coord[1]
            target = [x,y]
            
            
            direction = (math.atan((target[1]-enemy.coord[1])/(target[0]-enemy.coord[0]))) * 180/math.pi

            if enemy.coord[0] < target[0]:
                direction += 90 
                direction *= -1
            else:
                direction -= 90
                direction *= -1
            self.cimg_rect = self.cimg.get_rect(center = target)
            surface.blit(self.cimg,self.cimg_rect)

            if self.shot ==0 :
                self.error_margin = 0
            else:
                self.error_margin = self.hit/self.shot
            print(f'{int(self.error_margin*100)}%, SHOT: {self.shot}')
            if self.shot < 20:
                self.error_margin = 1
            
                

            if enemy.fireTime > 2/FIRERATE and distance < 350 and abs(direction - enemy.direction) < 15:
                enemy.fireTime = 0
                position, direction, velocity, player_pos, player_velocity = enemy.bullet_position() , enemy.bullet_direction(), enemy.bullet_velocity(), player.bullet_position(), player.bullet_velocity() #issue in these two functions         
                self.enemy_bullets.append(Bullets(direction, [position[0], position[1]], [velocity[0]*self.error_margin,velocity[1]*self.error_margin], space_ship_coord=[player_pos[0], player_pos[1]], init_pos= [position[0], position[1]], spaceship_velocity_usedByEnemy=[player_velocity[0], player_velocity[1]]))
                self.shot += 1
            enemy.fireTime += dt
            #replace [0,0] with [velocity[0],velocity[1]] for bullet to carry ship velocity -> worse aim

            enemy.turn(direction, dt)
            enemy.apply_force(FORCE/2 , dt)
            for bullet in self.bullets:
                #CHECK COLLISION WITH ENEMY - have to use rotatedRect in order to get coord of top left point instead of using center
                off_setX = -bullet.rotatedRect[0] + enemy.rotatedRect[0] 
                off_setY = -bullet.rotatedRect[1] + enemy.rotatedRect[1] 
                if bullet.mask.overlap(enemy.mask, (off_setX, off_setY)):
                    enemy.health -= 20
                    if enemy and enemy.health <= 0:
                        self.level_manager.enemies_destroyed += 1
                        self.enemies.remove(enemy)
            
            #DRAW BULLETS
        for bullet in self.enemy_bullets:
            surface.blit(bullet.rotatedSurf, bullet.rotatedRect)
                
            bullet.move(dt)

                
            if bullet.time >= BULLET_LIFE_SPAN:
                    
                try:
                    self.enemy_bullets.remove(bullet)
                except:
                    pass
                

            #CHECK COLLISION WITH BULLET AND PLAYER
            off_setX = -player.rotatedRect[0] + bullet.rotatedRect[0] 
            off_setY = -player.rotatedRect[1] + bullet.rotatedRect[1] 
            if player.mask.overlap(bullet.mask, (off_setX, off_setY)):

                try:
                    self.enemy_bullets.remove(bullet)
                    player.health -= 5
                    self.hit +=1
                except:
                    pass
                if self.space.player.health <= 0:
                    #DEATH CODE
                    pygame.quit()
                    sys.exit()

    
    
    def make_portal(self):
        self.portal = portal(coord= self.space.player.coord, direction=self.space.player.direction)
    def show_portal(self, surface):
        surface.blit(self.portal.img1, self.portal.texture_rect1)
        surface.blit(self.portal.img2, self.portal.texture_rect2)


        #PORTAL 1 -> 2
        off_setX = -self.space.player.rotatedRect[0] + self.portal.texture_rect1[0] 
        off_setY = -self.space.player.rotatedRect[1] + self.portal.texture_rect1[1] 
        if self.space.player.mask.overlap(self.portal.mask1, (off_setX, off_setY)) and self.portal.timer >= PORTAL_COOLDOWN:
            self.portal.timer = 0
            self.space.player.coord = [self.portal.coord2[0],self.portal.coord2[1]]
            self.space.player.health += 20
            
            

        #PORTAL 2 -> 1
        off_setX = -self.space.player.rotatedRect[0] + self.portal.texture_rect2[0] 
        off_setY = -self.space.player.rotatedRect[1] + self.portal.texture_rect2[1] 
        if self.space.player.mask.overlap(self.portal.mask2, (off_setX, off_setY)) and self.portal.timer >= PORTAL_COOLDOWN:
            self.portal.timer = 0
            self.space.player.coord = [self.portal.coord1[0],self.portal.coord1[1]]
            self.space.player.health += 20
        
        if self.space.player.health >= HEALTH:
            self.space.player.health = HEALTH
    def show_score(self, screen):
        img = self.text_font.render(f"SCORE: {self.space.player.score}",True, "white")
        screen.blit(img, (30,30))
        img = self.text_font.render(f"Level: {self.level_manager.level}",True, "white")
        screen.blit(img,(30,50))

    def show_healthbar(self, surface):
        health_bar = self.space.health_bar
        surface.blit(health_bar.img, health_bar.texture_rect)
        health_bar.draw(self.space.player.health, surface)
    def show_PWbar(self, surface):
        PWbar = self.space.Proton_Wave_Bar
        surface.blit(PWbar.img, PWbar.texture_rect)
        PWbar.draw(self.space.player.PW_time, surface)
    def show_FTbar(self,surface,time):
        FTbar = self.space.free_time_bar
        surface.blit(FTbar.img, FTbar.texture_rect)
        FTbar.draw(time,surface)
    def show_PW(self, surface, dt, proton_wave):
        self.proton_wave = proton_wave
        for PW in self.proton_wave:
            surface.blit(PW.img2, PW.texture_rect)
            PW.update(dt)
            if PW.alive >= PW_LIFE_TIME:
                proton_wave.remove(PW)
    def show_PSbar(self, surface):
        PSbar = self.space.Phase_shift_bar
        surface.blit(PSbar.img, PSbar.texture_rect)
        PSbar.draw(self.space.player.PS_time, surface)
    def show_blankBars(self,surface):
        surface.blit(self.space.BlankBars.bulletImg, self.space.BlankBars.bulletRect)
        surface.blit(self.space.BlankBars.protonImg, self.space.BlankBars.pwRect)
        surface.blit(self.space.BlankBars.scoreImg, self.space.BlankBars.scoreRect)    
    def show_Bars_bullet(self,surface):
        surface.blit(self.space.Bars.bulletImg, self.space.Bars.bulletRect)   
    def show_Bars_pw(self,surface):
        surface.blit(self.space.Bars.protonImg, self.space.Bars.pwRect)
    def show_Bars_score(self,surface):
        surface.blit(self.space.Bars.scoreImg, self.space.Bars.scoreRect)
    
    
        
        