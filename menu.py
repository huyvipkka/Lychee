import pygame, sys
from classes import Player, Enemy, Gun
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
    gatling_gun = Gun(30, 8, 100, 3000, 10)
    player = Player(400, 300, player_speed, damage, gatling_gun)
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
        print(player.Gun.ammos, end="\t")
        print(player.Gun.getTimeReload(current_time))
        pygame.draw.line(screen, 'white', (0, 600), (900, 600))
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
        for bul in player.Gun.magazine:
            bul.update()
            bul.draw(screen)
        
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
    