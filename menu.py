import pygame, sys
from classes import Player, Enemy
from main import screen, clock

player_speed = 4
enemy_speed = 1
enemy_hp = 100
damage = 5
FPS = 60

def startGame():
    gamePlay()

def gamePlay():
    enemy_max = 5
    player = Player(400, 300, player_speed, damage)
    enemy_group = pygame.sprite.Group()
    
    while True:
        pygame.display.flip()
        screen.fill('black')
        clock.tick(FPS)
        pos = pygame.mouse.get_pos()
        
        #create enemy if enemy < enemy max
        if len(enemy_group) < enemy_max:
            enemy = Enemy(enemy_speed, enemy_hp)
            enemy_group.add(enemy)
        
        # update(move) player, enemy
        player.update(screen, pos, pygame.time.get_ticks(), enemy_group)
        enemy_group.update(player.rect.center, player.bullet_group)
        # draw enemy, player
        player.draw(screen, pos)
        for ene in enemy_group:
            ene.draw(screen)
        
        if player.die:
           gameOver()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
def gameOver():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        pygame.display.flip()
        clock.tick(FPS)
    