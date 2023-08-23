import pygame, sys
from classes import Player, Enemy, Gun
from main import screen, clock
from other import *
from main import SCREEN_HEIGHT, SCREEN_WIDTH

player_speed = 4
enemy_speed = 1
enemy_hp = 100
damage = 5
FPS = 60

def startGame():
    gamePlay()

def gamePlay():
    enemy_max = 5
    dict_gun = {
        pygame.K_1 : Gun('gatling_gun', ammos=100, speed=6, speedGun=50, reloadTime=5000, damage=5, color='white'),  
        pygame.K_2 : Gun('pistol', ammos=7, speed=10, speedGun=500, reloadTime=2000, damage=50, color='red')
    }
    player = Player(400, 300, player_speed, damage, dict_gun)
    enemy_group = pygame.sprite.Group()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        screen.fill('black')
        clock.tick(FPS)
        pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        #create enemy if enemy < enemy max
        if len(enemy_group) < enemy_max:
            enemy = Enemy(enemy_speed, enemy_hp)
            enemy_group.add(enemy)
        
        # update(move) player, enemy
        player.update(screen, pos, current_time, enemy_group)
        enemy_group.update(player.rect.center, player.Gun)
        
        # draw enemy, player
        player.draw(screen, pos)
        for ene in enemy_group:
            ene.draw(screen)
        for gun in player.dict_gun.values():
            for bul in gun.magazine:
                bul.update()
                bul.draw(screen)
        # draw panel
        draw_panel(player, screen, current_time)
        if player.die:
           gameOver()
    
def gameOver():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        pygame.display.flip()
        clock.tick(FPS)
    