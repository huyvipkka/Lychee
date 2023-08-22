import pygame
from pygame.locals import *
from pygame.math import Vector2
from random import randint
from main import SCREEN_HEIGHT, SCREEN_WIDTH

class Player:
    def __init__(self, x, y, speed, damage):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.bullet_group = pygame.sprite.Group()
        self.bullet_active = False
        self.last_shot_time = 0
        self.shot_cooldown = 50 #ms
        self.damage = damage
        self.hp = 5
        self.hp_max = 5
        self.die = False
        
    def draw(self, surface, pos):
        pygame.draw.rect(surface, 'WHITE', self.rect, 0, 10)
        length = ((pos[0] - self.rect.centerx)**2 + (pos[1] - self.rect.centery)**2)**0.5
        if length != 0:
            self.end_posx = ((pos[0] - self.rect.centerx) * 50)/length + self.rect.centerx
            self.end_posy = ((pos[1] - self.rect.centery) * 50)/length + self.rect.centery
        pygame.draw.line(surface, 'AQUA', self.rect.center,(self.end_posx, self.end_posy), 5)
        
        end_posx_red = (self.rect.right - self.rect.left) * (self.hp/self.hp_max) + self.rect.left
        pygame.draw.line(surface, 'WHITE', (self.rect.left, self.rect.topleft[1] - 10), (self.rect.right, self.rect.topright[1] - 10), 3)
        pygame.draw.line(surface, 'RED', (self.rect.left, self.rect.topleft[1] - 10), (end_posx_red, self.rect.topright[1] - 10), 3)
        
    def update(self, screen, pos, game_timer, enemy_group):
        # player move
        self.move()
        # player shoot
        self.shoot(screen, pos, game_timer)
        # player collide enemy
        self.collide_enemy(enemy_group)
        if self.hp <= 0:
            self.die = True
        
    def move(self):
        key = pygame.key.get_pressed()
        self.move_up = key[K_UP] or key[K_w]
        self.move_down = key[K_DOWN] or key[K_s]
        self.move_left = key[K_LEFT] or key[K_a]
        self.move_right = key[K_RIGHT] or key[K_d]
        direction = Vector2(0, 0)
        if self.move_up:
            direction.y -= 1
        if self.move_down:
            direction.y += 1
        if self.move_left:
            direction.x -= 1
        if self.move_right:
            direction.x += 1
        
        if direction.length_squared() > 0:
            direction.normalize_ip()
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed
        
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.left <= 0:
            self.rect.left = 0
            
    def shoot(self, screen, pos, game_timer):

        if pygame.mouse.get_pressed()[0]:
             if game_timer - self.last_shot_time >= self.shot_cooldown:
                bullet = Bullet(self.rect.centerx, self.rect.centery, pos, self.damage)
                self.bullet_group.add(bullet)
                self.bullet_active = True
                self.last_shot_time = game_timer
                
        self.bullet_group.update()
        self.bullet_group.draw(screen)
        
    def collide_enemy(self, enemy_group):
        collision_list = pygame.sprite.spritecollide(self, enemy_group, True)
        if len(collision_list) > 0:
            self.hp -= 1
                    
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, hp):
        super().__init__()
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.image = pygame.Surface((40, 40))  
        self.image.fill(self.color)  
        self.rect = self.image.get_rect()  
        side = randint(0, 3) # 0: top, 1: right, 2: bottom, 3: left
        if side == 0:
            self.rect.centerx = randint(0, SCREEN_WIDTH)
            self.rect.centery = -100
        elif side == 1:
            self.rect.centerx = SCREEN_WIDTH + 100
            self.rect.centery = randint(0, SCREEN_HEIGHT)
        elif side == 2:
            self.rect.centerx = randint(0, SCREEN_WIDTH)
            self.rect.centery = SCREEN_HEIGHT + 100
        else:
            self.rect.centerx = -100
            self.rect.centery = randint(0, SCREEN_HEIGHT)
        self.speed = speed
        self.hp = hp
        self.hp_max = hp
        
        
    def update(self, player_pos, bullet_group):
        direction = Vector2(player_pos) - Vector2(self.rect.center)
        if direction.length() > 0:
            direction.normalize_ip()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed
        
        for bul in bullet_group:
            if pygame.Rect.colliderect(self.rect, bul.rect):
                bul.kill()
                self.hp -= bul.damage
        
        if self.hp <= 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        end_posx_red = (self.rect.right - self.rect.left) * (self.hp/self.hp_max) + self.rect.left
        pygame.draw.line(screen, 'WHITE', (self.rect.left, self.rect.topleft[1] - 10), (self.rect.right, self.rect.topright[1] - 10), 3)
        pygame.draw.line(screen, 'RED', (self.rect.left, self.rect.topleft[1] - 10), (end_posx_red, self.rect.topright[1] - 10), 3)


        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, pos, damage):
        super().__init__()
        self.image = pygame.Surface((10, 10))  
        self.image.fill('WHITE')  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = y
        self.speed = 8
        self.direction =  Vector2(pos) - Vector2(self.rect.center)
        self.active = True
        self.damage = damage
        
    def update(self):
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.active = False
        if not self.active:
            self.kill()