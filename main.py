import pygame
from pygame.locals import (
    K_DOWN, K_UP, K_LEFT,
    K_ESCAPE, K_RIGHT, RLEACCEL, K_1,
    MOUSEBUTTONDOWN
)
from utils import (
    Player, Enemy, Missile, explosions
)

# initialize pygame
pygame.init()

# set game screen
size = WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode(size)
BACKGROUND = pygame.image.load('assets/stars2.jpg')

# sprite groups
all_sprites = pygame.sprite.Group()
all_missiles = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()


# create player instance
player = Player(game_screen=size)

# create custom game events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1200)

#initializing a sound mixer for 16-bit 44100hz steoreo
pygame.mixer.pre_init(44100, 16, 2, 4096)
gunShotSound = pygame.mixer.Sound('assets/Gun+Silencer.wav')

# Game loop
running = True

clock = pygame.time.Clock()

while running:
    screen.blit(BACKGROUND, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_1:
                missile = Missile(player=player)
                all_sprites.add(missile)
                all_missiles.add(missile)
                gunShotSound.play()#play tho sound
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
    all_enemies.update(all_missiles)#using keyword arguments produced errors on pycharm

    # update missiles
    all_missiles.update()

    explosions.draw(screen)
    explosions.update()

    # collision detection
    if pygame.sprite.spritecollideany(player, all_enemies):
        player.kill()
        #running = False
        pass

    pygame.display.flip()

    clock.tick(150)