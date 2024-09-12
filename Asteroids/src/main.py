import pygame
import sys
import time
import random

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
        #MOVEMENT SWITCHES
        moveUp = False
        rotateLeft = False
        rotateRight = False

        #FIRE/USE SWITCHES
        shooting = False
        protonWave = False
        teleport = False
        freeze = False

        #OBJECTS
        bullets = []
        proton_wave = []
        
        #CALCULATE DT
        prev_time = time.time() 
        dt = 0

        #timer for fire rate
        fireTime = 0 
        
        #TIMERS/MULTIPLIERS
        TIME_MULTIPLIER = 1
        PW_MULTIPLIER = 1
        PW_power_up_timer = 0
        Ammo_multiplier = 1
        Ammo_multiplier_timer = 0
        DS_timer = 0
        Time_slow_timer = 0

        smoke_timer = 0

        screen = self.screen
        game = self.game
        
        while True:
            if len(game.level_manager.asteroids) == 0 and len(game.level_manager.enemies) == 0:  #If true then all objects are destroyed -> start new level
                game.SMOKE_IMG = pygame.image.load(f"Assets/smoke{game.level_manager.level%5}.png")
                game.SMOKE_IMG_ENEMY = pygame.image.load(f"Assets/smoke{(game.level_manager.level+1)%5}.png")
                game.level_manager.new_level()
                

            #SHOW IMAGES IN ORDER
            game.show_bg(screen)
            game.show_blankBars(screen)
            
            #portal specific images
            if game.portal:
                game.show_portal(screen)
                game.portal.timer += dt

            game.show_score(screen)
            game.show_PWbar(screen)
            game.show_healthbar(screen)
            game.show_PSbar(screen)
            game.show_FTbar(screen,Time_slow_timer, freeze)
             
            game.show_smoke(screen,dt)

            game.show_PW(screen, dt, proton_wave)
            game.show_bullets(screen, bullets, dt)            
            game.show_asteroid(screen, game.level_manager.get_asteroids(), dt)

            game.show_pop_ups(screen,dt)

            game.show_player(screen)
            game.update_enemy(game.level_manager.enemies, screen, dt, self.game.space.player.coord)
            
            if game.Alive == False:
                game.show_game_over(screen,dt)
            #delta time
            now = time.time()
            
            dt = (now - prev_time) * TIME_MULTIPLIER
            prev_time = now
            
            #check if powerup is active -> calculate time passed in order to turn powerup off -> adjust multipliers depending on powerup -> show updated image to indicate powerup is active

            #PROTON WAVE POWER UP -> timer goes 2 times faster
            if game.level_manager.PW:
                PW_power_up_timer += dt
                PW_MULTIPLIER = 2
                game.show_Bars_pw(screen)
                if PW_power_up_timer > PW_power_up_length:
                    game.level_manager.PW = False
                    PW_MULTIPLIER = 1
                    PW_power_up_timer = 0
            #HEALTH POWER UP -> fill health bar
            if game.level_manager.Health:
                game.space.player.health  += dt*10
                if game.space.player.health >= HEALTH:
                    game.space.player.health = HEALTH
                    game.level_manager.Health = False
            #DOUBLE FIRE RATE
            if game.level_manager.Ammo_Boost:
                Ammo_multiplier = 2
                Ammo_multiplier_timer += dt
                game.show_Bars_bullet(screen)
                if Ammo_multiplier_timer > AMMO_MULTIPLIER_LENGTH:
                    game.level_manager.Ammo_Boost = False
                    Ammo_multiplier = 1
                    Ammo_multiplier_timer = 0
            #DOUBLE SCORE POWER UP 
            if game.level_manager.DS:
                game.score_multiplier = 2
                DS_timer+= dt
                game.show_Bars_score(screen)
                if DS_timer >= DS_TIME_LENGTH:
                    DS_timer = 0
                    game.level_manager.DS = False
            else:
                game.score_multiplier = 1


            #TAKE INPUT VALUES
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #TAKE INPUT KEYS
                #press
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
                    if event.key == pygame.K_LSHIFT:
                        teleport = True
                    if event.key ==  pygame.K_LCTRL and Time_slow_timer > 2: #only able to activate once atleast 2 seconds are in the timerAA
                        freeze = True
                #release
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
                    if event.key == pygame.K_LSHIFT:
                        teleport = False
                    if event.key == pygame.K_LCTRL:
                        freeze = False

            #apply force when moving forward -> else apply 0 force but calll function to update position using dt
            if moveUp:

                game.space.player.apply_force(FORCE, game.Alive,delta_time= dt)
                game.space.player.img = game.space.player.img2
                if smoke_timer > 0.02 and game.Alive:
                    x = random.randint(-10,10)
                    y = random.randint(-10,10)
                    game.smokes.append(smoke(game.space.player.direction,[game.space.player.coord[0]+x,game.space.player.coord[1]+y],game.SMOKE_IMG))
                    smoke_timer = 0
            else:
                game.space.player.apply_force(0, game.Alive,delta_time=dt)
                #toggle image 
                game.space.player.img = game.space.player.img1
            smoke_timer += dt

            #PLAYER ROTATION
            if rotateLeft:
                game.space.player.direction += ROTATE_SPEED * dt
            if rotateRight:
                game.space.player.direction -= ROTATE_SPEED * dt


            #check if enough times has passed to fire and if player if firing
            if shooting and fireTime >= 1/FIRERATE and game.Alive:
                position, direction, velocity = game.space.player.bullet_position() , game.space.player.bullet_direction(), game.space.player.bullet_velocity() #functions simply return player values
                fireTime = 0          
                bullets.append(Bullets(direction, [position[0], position[1]], [velocity[0], velocity[1]])) #by appending bullet we are creating a new object
            self.game.space.player.PW_time += dt * PW_MULTIPLIER
            self.game.space.player.PS_time += dt
            fireTime += dt* Ammo_multiplier

            if freeze and Time_slow_timer > 0 and game.Alive:
                TIME_MULTIPLIER = 1/3          
                Time_slow_timer -= dt*1/TIME_MULTIPLIER
            else:
                freeze = False
                TIME_MULTIPLIER = 1
                if Time_slow_timer <TIME_FREEZE_TIME:
                    Time_slow_timer += dt
                else:
                    Time_slow_timer = TIME_FREEZE_TIME
            #same provess as above
            if protonWave and self.game.space.player.PW_time >= PW_fire_rate and game.Alive:
                self.game.space.player.PW_time = 0
                position = game.space.player.bullet_position()
                proton_wave.append(Proton_Wave([position[0], position[1]] ))
            if teleport and game.space.player.PS_time >= PS_fire_rate and game.Alive:
                game.make_portal()
                game.space.player.PS_time = 0

                
            

            pygame.display.update()
            #print("UPS:", 1/dt)


    

main = Main()
main.mainloop()