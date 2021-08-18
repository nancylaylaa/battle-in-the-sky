# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 08:51:18 2021
@author: WiT Kelas E Grup H
"""

# 1 import library ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from sys import exit
from pygame.locals import *
from random import randint


# 2 initialize game ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle in The Sky") #window title

# key mapping
keys = {
        "top": False,
        "bottom": False,
        "left": False,
        "right": False
        }

# 3 load game assets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# images
player = pygame.image.load("assets/plane.png")
sky = pygame.image.load("assets/sky.png")
bullet_p = pygame.image.load("assets/bullet_p.png")
bullet_e = pygame.image.load("assets/bullet_e.png")
the_enemies = pygame.image.load("assets/enemy.png")
healthbar = pygame.image.load("assets/healthbar.png")
health = pygame.image.load("assets/health.png")
gameover = pygame.image.load("assets/game_oversky.png")
exp = pygame.image.load('assets/explosion.png').convert_alpha()
game_font1 = pygame.font.Font('font/aircruiserlaserital.ttf',75)
game_font2 = pygame.font.Font('font/aircruiser3d.ttf',50)
game_font3 = pygame.font.Font('font/Oswald-Heavy.ttf',30)
player_rect = player.get_rect(center = (100,100))

# sounds
bullet_sound = pygame.mixer.Sound('sound/bullet.mp3')
bullet_sound.set_volume(0.3)
enemy_sound = pygame.mixer.Sound('sound/enemy3_down.mp3')
crossing_sound = pygame.mixer.Sound('sound/enemy2_down.mp3')
bomb_sound = pygame.mixer.Sound('sound/bomb.mp3')
win_sound = pygame.mixer.Sound('sound/achievement.mp3')

#functuons
def message_display_gameover(text,pos):
    text_surf = game_font1.render(text, True, (0,0,0))
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

def message_display_win(text,pos):
    text_surf = game_font2.render(text, True, (0,0,0))
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

def message_display_clock(text,pos):
    text_surf = game_font3.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

def message_display_small(text,pos):
    text_surf = game_font3.render(text, True, (255,0,0))
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)
    pygame.display.update()  

def terminate():
    pygame.quit()
    exit()
    
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
        
def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    text_surf = game_font1.render(text, True, (0,0,0))
    text_rect = text_surf.get_rect(center=[width/2,height/2])
    screen.blit(text_surf, text_rect)
    message_display_small("Press any key", (450,375))
    while checkForKeyPress() == None:
        pygame.display.update()

def main():
    screen.blit(sky,(0,0))
    showTextScreen("Battle in The Sky")
    runGame()
    
def runGame():
    running = True
    
    #exit code for game over and win condition
    exitcode =0
    EXIT_CODE_GAME_OVER = 0
    EXIT_CODE_WIN =1

    score=0
    health_point = 194
    countdown_timer = 60000
    player_bullets = []
    projectiles = []
    enemy_timer = 300 # waktu kemunculan
    projectile_timer = 500
    enemies = [[width, 150]] # list yang menampung koordinat musuh

    ## 4 the game loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    while(running):
    
        # 5 clear the screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        screen.fill(0)
    
        # 6 draw the game object ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        screen.blit(sky,(0,0)) 
        screen.blit(player, player_rect)  
    
        # 6.1 draw player bullets
        for bullet in player_bullets:
           bullet_p_index = 0
           bullet[1]+=2
           if bullet[1] > width:
               player_bullets.pop(bullet_p_index)
               bullet_p_index += 1
               # draw the bullet
           for bullet in player_bullets:
               screen.blit(bullet_p, (bullet[1], bullet[2]))
    
        # 6.2 draw enemy projectile
        # waktu peluru musuh akan muncul
        projectile_timer -=1
        if projectile_timer == 0:
            #buat musuh baru
            projectiles.append([width, randint(50, height-50)])
            #reset enemy timer to random time
            projectile_timer = randint(50,500)
        
        #index = 0
        for projectile in projectiles:
            index_b = projectiles.index(projectile)
            projectile[0] -= 1
            screen.blit(bullet_e, projectile)
            proj_rect = bullet_e.get_rect(x = projectile[0], y = projectile[1])
                
            # peluru musuh menabrak player
            if player_rect.colliderect(proj_rect):
                enemy_sound.play()
                crashb_pos = [player_rect.midright[0],player_rect.midright[1]]
                screen.blit(exp, crashb_pos)
                projectiles.pop(index_b)
                health_point -= 15
    
        # 6.3 draw enemy
        # waktu musuh akan muncul
        enemy_timer -=1
        if enemy_timer == 0:
            #buat musuh baru
            enemies.append([width, randint(50, height-50)])
            #reset enemy timer to random time
            enemy_timer = randint(300,700)
        
        #index = 0
        for enemy in enemies:
            index_e = enemies.index(enemy)
            #musuh bergerak dengan kecepatan ... pixel ke kiri
            enemy[0] -= 0.5
            screen.blit(the_enemies, enemy)
            enemy_rect = the_enemies.get_rect(x = enemy[0], y = enemy[1])
                
            # musuh menabrak player
            if player_rect.colliderect(enemy_rect):
                bomb_sound.play()
                crashe_pos = [player_rect.midright[0],player_rect.midright[1]]
                screen.blit(exp, crashe_pos)
                message_display_gameover("Game Over",((width/2),(height/2)))
                running = False
        
            #musuh melewati batas belakang (game over)
            if enemy_rect.left == 0:
                crossing_sound.play()
                enemies.pop(index_e)
                message_display_gameover("Game Over",((width/2),(height/2)))
                running = False
                
            #musuh tertembak
            index_bullet=0
            for bullet in player_bullets:
                bullet_rect = pygame.Rect(bullet_p.get_rect())
                bullet_rect.left = bullet[1]
                bullet_rect.top = bullet[2]
                if enemy_rect.colliderect(bullet_rect):
                    score+=10
                    enemies.pop(index_e)
                    player_bullets.pop(index_bullet)
                index_bullet+=1
            #index +=1
    
        # 6.4 draw health bar
        screen.blit(healthbar, (5,5))
        for hp in range(health_point):
            screen.blit(health, (hp+8, 8))
        
        # 6.5 draw clock
        minutes = int((countdown_timer-pygame.time.get_ticks())/60000)
        seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
        message_display_clock("{:02}:{:02}".format(minutes, seconds),(850,20))  
    
        # 7 update the screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pygame.display.flip()
    
        # 8 event loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for event in pygame.event.get():
            #event saat tombol exit diklik
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            # Fire!!
            if event.type == pygame.KEYDOWN:
                if event.key==K_SPACE:
                    player_bullets.append([0, player_rect[0], player_rect[1]])
                    bullet_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys["top"] = True
                elif event.key == K_a:
                    keys["left"] = True
                elif event.key == K_s:
                    keys["bottom"] = True
                elif event.key == K_d:
                    keys["right"] = True
            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    keys["top"] = False
                elif event.key == K_a:
                    keys["left"] = False
                elif event.key == K_s:
                    keys["bottom"] = False
                elif event.key == K_d:
                    keys["right"] = False
        # end of event loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # 9 move the player ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if keys["top"]:
            if player_rect[1]-50 >0:
                player_rect[1] -= 1.5 # kurangi nilai y
        elif keys["bottom"]:
            if player_rect[1]+50 <600:
                player_rect[1] += 1.5 #tambah nilai y
        if keys["left"]:
           if player_rect[0]-50 >0:
               player_rect[0] -= 1.5 #pesawat tidak bisa mundur?
        elif keys["right"]:
           if player_rect[0] <875:
               player_rect[0] += 1.5 #tambah nilai x
 
        # 10 win/lose check ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if pygame.time.get_ticks() > countdown_timer:
            running = False
            exitcode = EXIT_CODE_WIN
        if health_point <= 0:
            running = False
            exitcode = EXIT_CODE_GAME_OVER
    # - End of game loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 11 Win/lose display~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if exitcode == EXIT_CODE_GAME_OVER:
        message_display_gameover("Game Over",((width/2),(height/2)))
        message_display_small("Score : {}".format(score),(450,350))
    else:
        message_display_win("You Win !",((width/2),(height/2)))
        message_display_small("Score : {}".format(score),(450,350))
        win_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

main()
