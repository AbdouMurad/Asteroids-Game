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

        self.score_multiplier = 1
    def show_bg(self, surface):
        rect = (0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(surface, 'black', rect)
        
        for i in self.config.coord:
            rect = (i[0], i[1], 1 , 1)
            pygame.draw.rect(surface, (i[2], i[2], i[2]), rect)

    def show_bullets(self, surface, bullets, dt):
        self.bullets = bullets
        for bullet in bullets:
            surface.blit(bullet.rotatedSurf, bullet.rotatedRect)
            #surface.blit(bullet.mask_image, bullet.rotatedRect)
            bullet.move(dt) 

            if bullet.time >= BULLET_LIFE_SPAN:
                bullets.remove(bullet)
        

            
            
    
    def show_asteroid(self, surface, asteroids, dt):

        self.level_manager.spaceship_coord = self.space.player.coord

        for asteroid in asteroids:
            surface.blit(asteroid.rotatedSurf, asteroid.rotatedRect)
            #surface.blit(asteroid.mask_image, asteroid.rotatedRect)
            asteroid.move(dt)
            direction, distance, mass = asteroid.Gravity(dt, self.space.player.coord)
            self.space.player.Gravity(direction , distance, mass, dt)

            #CHECK COLLISION WITH PLAYER - have to use rotatedRect in order to get coord of top left point instead of using center
            off_setX = -asteroid.rotatedRect[0] + self.space.player.rotatedRect[0] 
            off_setY = -asteroid.rotatedRect[1] + self.space.player.rotatedRect[1] 
            if asteroid.mask.overlap(self.space.player.mask, (off_setX, off_setY)):
                self.space.player.health -= 20
                if asteroid:
                    asteroids.remove(asteroid)
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
                            asteroids.remove(asteroid)
                            self.level_manager.asteroid_destroyed(asteroid.name, asteroid.coord)
                            self.space.player.score += 10 * self.score_multiplier

            #CHECK COLLISION WITH BULLET
            for bullet in self.bullets:
                off_setX = -asteroid.rotatedRect[0] + bullet.rotatedRect[0] 
                off_setY = -asteroid.rotatedRect[1] + bullet.rotatedRect[1] 
                if asteroid.mask.overlap(bullet.mask, (off_setX, off_setY)):
                    self.bullets.remove(bullet)
                    asteroid.Take_Damage(bullet.speed)
                    if asteroid.health <= 0:
                        asteroids.remove(asteroid)
                        self.level_manager.asteroid_destroyed(asteroid.name, asteroid.coord)
                        self.space.player.score += 10 * self.score_multiplier
                        
                    

    def show_player(self, surface):
        player = self.space.player
        surface.blit(player.rotatedSurf, player.rotatedRect)
    def update_enemy(self, enemies, surface, dt):
        for enemy in enemies:
            player = self.space.player

            surface.blit(enemy.rotatedSurf, enemy.rotatedRect)

            enemy.player_info(player.coord, player.direction, player.velocity, player.acceleration)
            
            enemy.turn(dt)
            #ENEMY BEHAVIOUR - completly random
            int =  random.randint(0, 100)
            match int:
                case 1:
                    if enemy.turning == False:
                        enemy.turn_amount = random.randint(6,360)
                        enemy.turning = True
                        
                case 2:
                    if enemy.turning == False:
                        enemy.turn_amount = random.randint(-360, -6)
                        enemy.turning = True
                        
                case x if x > 60: #case from 40 and up
                    enemy.apply_force(FORCE , dt)
            if enemy.fireTime > 1/FIRERATE:
                enemy.fireTime = 0
                position, direction, velocity, player_pos, player_velocity = enemy.bullet_position() , enemy.bullet_direction(), enemy.bullet_velocity(), player.bullet_position(), player.bullet_velocity() #issue in these two functions         
                enemy.bullets.append(Bullets(direction, [position[0], position[1]], [velocity[0], velocity[1]], space_ship_coord=[player_pos[0], player_pos[1]], init_pos= [position[0], position[1]], spaceship_velocity_usedByEnemy=[player_velocity[0], player_velocity[1]]))
            enemy.fireTime += dt
            
            #DRAW BULLETS
            for bullet in enemy.bullets:
                surface.blit(bullet.rotatedSurf, bullet.rotatedRect)
                #surface.blit(bullet.mask_image, bullet.rotatedRect)
                bullet.move(dt)
                
                if bullet.time >= BULLET_LIFE_SPAN:
                    enemy.bullets.remove(bullet)

                #CHECK COLLISION WITH BULLET AND PLAYER
                off_setX = -player.rotatedRect[0] + bullet.rotatedRect[0] 
                off_setY = -player.rotatedRect[1] + bullet.rotatedRect[1] 
                if player.mask.overlap(bullet.mask, (off_setX, off_setY)):
                    enemy.bullets.remove(bullet)
                    f = open("assets/Data.txt", "a")
                    dist = sqrt((bullet.space_ship_coord[0]-bullet.init_pos[0])**2 + (bullet.space_ship_coord[1]-bullet.init_pos[1])**2)
                    f.write(f"{bullet.space_ship_coord}, {bullet.init_pos},{dist}, {bullet.spaceship_velocity_usedByEnemy}, {bullet.spaceship_velocity}, {bullet.direction}\n")
                    f.close

                    

            
            


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
    def show_PW(self, surface, dt, proton_wave):
        self.proton_wave = proton_wave
        for PW in self.proton_wave:
            surface.blit(PW.img2, PW.texture_rect)
            PW.update(dt)
            if PW.alive >= PW_LIFE_TIME:
                proton_wave.remove(PW)


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
    
    
        
        