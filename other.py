import pygame
from main import SCREEN_HEIGHT, SCREEN_WIDTH

font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 24)

class Button:
    def __init__(self, text, font, color, color_hover, rect):
        self.text = text
        self.font = font
        self.size = pygame.font.Font.size(self.font, text)
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.color = color
        self.color_hover = color_hover
        
    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        color = self.color
        if self.rect.collidepoint(pos[0], pos[1]):
            color = self.color_hover   
        pygame.draw.rect(screen, color, self.rect, 2)
        x = self.rect.centerx - self.size[0]//2
        y = self.rect.centery - self.size[1]//2
        screen.blit(self.font.render(self.text, True, color), (x, y))
    
    def check(self, *keys_pressed):
        key = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        for k in keys_pressed:
            if key[k]:
                return True

        if self.rect.collidepoint(pos[0], pos[1]):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False
        
class NewBoard():
    def __init__(self, text, font, text_color, x, y):
        self.text = text
        self.font = font
        self.size = pygame.font.Font.size(self.font, text)
        self.text_color = text_color
        self.x = x
        self.y = y
        
    def draw(self, screen):
        screen.blit(self.font.render(self.text, True, self.text_color), (self.x, self.y))
        

def draw_panel(player_object, screen, current_time):
    pygame.draw.rect(screen, 'WHITE', (0, SCREEN_HEIGHT, SCREEN_WIDTH, 50))
    
    text = f'Ammo: {player_object.Gun.ammos}/{player_object.Gun.ammos_max}'
    if player_object.Gun.reloading:
        text = f'Ammo: {player_object.Gun.getTimeReload(current_time)}'
    inforAmmo = NewBoard(text, font_big, 'indigo', 0, SCREEN_HEIGHT)
    inforAmmo.draw(screen)
    
    inforGun = NewBoard(f'{player_object.gun_pos+1} : {player_object.Gun.name}', font_big, 'indigo', 400, SCREEN_HEIGHT)
    inforGun.draw(screen)