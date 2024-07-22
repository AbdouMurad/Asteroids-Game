import pygame
import sys
import time

from const import *
from game import Game
from entities import *




class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroid")
        self.game = Game()

    
    
    def mainloop(self):
        moveUp = False
        rotateLeft = False
        rotateRight = False
        shooting = False
        protonWave = False
        
        bullets = []
        proton_wave = []
        enemies = []
        #enemies.append(Enemy([600,600]))
       


        prev_time = time.time()
        dt = 0
        fireTime = 0
        
        PW_MULTIPLIER = 1
        PW_power_up_timer = 0
        Ammo_multiplier = 1
        Ammo_multiplier_timer = 0
        DS_timer = 0


        screen = self.screen
        game = self.game
        

        while True:
            
            
        
            game.show_bg(screen)
            game.show_blankBars(screen)

            game.show_score(screen)
            game.show_PWbar(screen)
            game.show_healthbar(screen)
            
            game.show_PW(screen, dt, proton_wave)
            game.show_bullets(screen, bullets, dt)            
            game.show_asteroid(screen, game.level_manager.get_asteroids(), dt)

            game.show_player(screen)
            game.update_enemy(enemies, screen, dt)
            
            #delta time
            now = time.time()
            dt = now - prev_time
            prev_time = now

            
            #CHECK POWER UPS
            if game.level_manager.PW:
                PW_power_up_timer += dt
                PW_MULTIPLIER = 2
                game.show_Bars_pw(screen)
                if PW_power_up_timer > PW_power_up_length:
                    game.level_manager.PW = False
                    PW_MULTIPLIER = 1
                    PW_power_up_timer = 0
            if game.level_manager.Health:
                game.space.player.health = HEALTH
                game.level_manager.Health = False
            if game.level_manager.Ammo_Boost:
                Ammo_multiplier = 2
                Ammo_multiplier_timer += dt
                game.show_Bars_bullet(screen)
                if Ammo_multiplier_timer > AMMO_MULTIPLIER_LENGTH:
                    game.level_manager.Ammo_Boost = False
                    Ammo_multiplier = 1
                    Ammo_multiplier_timer = 0
            if game.level_manager.DS:
                game.score_multiplier = 2
                DS_timer+= dt
                game.show_Bars_score(screen)
                if DS_timer >= DS_TIME_LENGTH:
                    DS_timer = 0
                    game.level_manager.DS = False
            





            

            #check if we have destroyed enough asteroids -> new level (level # = # of asteroids spawned)
            if game.level_manager.destroyed >= game.level_manager.level*7:
                game.level_manager.new_level()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        moveUp = True
                    if event.key == pygame.K_a:
                        rotateLeft = True
                    elif event.key == pygame.K_d:
                        rotateRight = True
                    if event.key == pygame.K_SPACE:
                        shooting = True
                    if event.key == pygame.K_s:
                        protonWave = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        moveUp = False
                    if event.key == pygame.K_a:
                        rotateLeft = False
                    if event.key == pygame.K_d:
                        rotateRight = False
                    if event.key == pygame.K_SPACE:
                        shooting = False
                    if event.key == pygame.K_s:
                        protonWave = False

           
            if moveUp:
                game.space.player.apply_force(FORCE, delta_time= dt)
            else:
                game.space.player.apply_force(0, delta_time=dt)
            

            if rotateLeft:
                game.space.player.direction += ROTATE_SPEED * dt
            if rotateRight:
                game.space.player.direction -= ROTATE_SPEED * dt

            fireTime += dt* Ammo_multiplier
            if shooting and fireTime >= 1/FIRERATE:
                position, direction, velocity = game.space.player.bullet_position() , game.space.player.bullet_direction(), game.space.player.bullet_velocity() #issue in these two functions
                fireTime = 0          
                bullets.append(Bullets(direction, [position[0], position[1]], [velocity[0], velocity[1]]))
            self.game.space.player.PW_time += dt * PW_MULTIPLIER
            if protonWave and self.game.space.player.PW_time >= PW_fire_rate:
                self.game.space.player.PW_time = 0
                position = game.space.player.bullet_position()
                proton_wave.append(Proton_Wave([position[0], position[1]] ))
                

                
            

            pygame.display.update()


    

main = Main()
main.mainloop()