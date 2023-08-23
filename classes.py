import pygame
from pygame.locals import *
from pygame.math import Vector2
from random import randint
from main import SCREEN_HEIGHT, SCREEN_WIDTH

class Player:
    def __init__(self, x, y, speed, damage, Gun):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.Gun = Gun
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
        
        
    def update(self, screen, mouse_pos, game_timer, enemy_group):
        # player move
        self.move()
        # player shoot
        self.Gun.update(self.rect.center, mouse_pos, game_timer)
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
           
    def collide_enemy(self, enemy_group):
        collision_list = pygame.sprite.spritecollide(self, enemy_group, True)
        if len(collision_list) > 0:
            self.hp -= 1
                    
class Gun():
    def __init__(self, ammos, speed, speedGun, reloadTime, damage):
        self.shoot = pygame.USEREVENT + 1
        pygame.time.set_timer(self.shoot, speedGun)
        self.reloadTime = reloadTime # time to reload ammos
        self.reloading = False # is reload
        self.speed = speed # speed of ammo
        self.ammos = ammos 
        self.ammos_max = ammos
        self.damage = damage
        self.magazine = []
        self.shot_timer = 0  # Initialize the shot timer
        self.shot_interval = speedGun # Set the desired shot interval in milliseconds
        
        for _ in range(self.ammos):
            bullet = Bullet(self.damage)
            self.magazine.append(bullet)
        
    def update(self, player_pos, mouse_pos, current_time):
        if self.ammos > 0:
            self.reloading = False
            self.fire(player_pos, mouse_pos, current_time)
        else:
            self.reloading = True
            self.reloadMag(current_time)
            
    def fire(self, player_pos, mouse_pos, current_time):
        if pygame.mouse.get_pressed()[0]:
            if current_time - self.shot_timer >= self.shot_interval:
                self.shot_timer = current_time  # Update the shot timer
                self.magazine[self.ammos-1].reset(player_pos, mouse_pos)
                self.magazine[self.ammos-1].active = True
                self.ammos -= 1
                
    def reloadMag(self, current_time):
        if current_time - self.shot_timer >= self.reloadTime:
            self.shot_timer = current_time
            self.ammos = self.ammos_max
    
    def getTimeReload(self, current_time):
        time_remaining = round((self.reloadTime - (current_time - self.shot_timer))/1000, 1)
        if self.reloading:
            return time_remaining
        else:
            return 0
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.image = pygame.Surface((10, 10)) 
        self.rect = self.image.get_rect()  
        self.speed = 8
        self.active = False
        self.damage = damage
        
    def update(self):
        if self.active:
            if self.direction.length() > 0:
                self.direction.normalize_ip()
                self.rect.x += self.direction.x * self.speed
                self.rect.y += self.direction.y * self.speed
            
            if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
                self.active = False
                
    def reset(self, player_pos, mouse_pos):
        self.rect.center = player_pos
        self.direction =  Vector2(mouse_pos) - Vector2(self.rect.center)
        
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, 'WHITE', self.rect, 0, 3)
    
    def inflictDmg(self):
        return self.damage if self.active else 0
            
            
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
        
        
    def update(self, player_pos, Gun: Gun):
        direction = Vector2(player_pos) - Vector2(self.rect.center)
        if direction.length() > 0:
            direction.normalize_ip()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed
        if self.hp <= 0:
            self.kill()
        else:
            self.checkShooted(Gun)
    
    def checkShooted(self, Gun):
        for bul in Gun.magazine:
            if self.rect.collidepoint(bul.rect.centerx, bul.rect.centery):
                self.hp -= bul.inflictDmg()
                bul.active = False
                
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        end_posx_red = (self.rect.right - self.rect.left) * (self.hp/self.hp_max) + self.rect.left
        pygame.draw.line(screen, 'WHITE', (self.rect.left, self.rect.topleft[1] - 10), (self.rect.right, self.rect.topright[1] - 10), 3)
        pygame.draw.line(screen, 'RED', (self.rect.left, self.rect.topleft[1] - 10), (end_posx_red, self.rect.topright[1] - 10), 3)
            