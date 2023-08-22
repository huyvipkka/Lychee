from menu import *

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

if __name__ == '__main__':
    startGame()

