import pygame
from pygame.locals import (
    K_DOWN, K_UP, K_LEFT,
    K_ESCAPE, K_RIGHT, RLEACCEL
)
from utils import Player, Enemy

# initialize pygame
pygame.init()

# set game screen
size = WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode(size)
BACKGROUND = pygame.image.load('assets/stars2.jpg')

# sprite groups
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()

# create player instance
player = Player(game_screen=size)

# create custom game events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)

# Game loop
running = True

while running:
    screen.blit(BACKGROUND, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY:
            enemy = Enemy(game_screen=size)
            all_enemies.add(enemy)
            all_sprites.add(enemy)

    # add  player to sprite group
    all_sprites.add(player)

    # block transfer to game screen
    for i in all_sprites:
        screen.blit(i.surf, i.rect)
    
    # check for movement
    keys = pygame.key.get_pressed()
    player.update(pressed_keys=keys)

    #  update new enemy sprites
    all_enemies.update()
    
    pygame.display.flip()

