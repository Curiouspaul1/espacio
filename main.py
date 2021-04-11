import pygame
from pygame.locals import (
    K_DOWN, K_UP, K_LEFT,
    K_ESCAPE, K_RIGHT, RLEACCEL, K_1,
    MOUSEBUTTONDOWN
)
from utils import (
    Player, Enemy, Missile, Explosion, hearts, EnemyGroup,
    enemy_beams
)
from helpers import spawnEnemies
import random

# initialize pygame
pygame.init()

# set game screen
size = WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode(size)
BACKGROUND = pygame.image.load('assets/stars2.jpg')

# sprite groups
all_sprites = pygame.sprite.Group()
all_missiles = pygame.sprite.Group()
all_enemies =  EnemyGroup()
explosions = pygame.sprite.Group()

# create player instance
player = Player(game_screen=size)
lives = [hearts(pos=(i, 20)) for i in range(10, 70, 20)]
no_of_lives = 3

# create custom game events
ADDENEMY = pygame.USEREVENT + 1
SHOOTENEMYBEAMS = pygame.USEREVENT + 2
pygame.time.set_timer(SHOOTENEMYBEAMS, random.randint(200, 400))
pygame.time.set_timer(ADDENEMY, 3000)

#initializing a sound mixer for 16-bit 44100hz steoreo
pygame.mixer.pre_init(44100, 16, 2, 4096)
gunShotSound = pygame.mixer.Sound('assets/Gun+Silencer.wav')

isPlayerkilled = False

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
            global enemies
            enemies = spawnEnemies(size)
            all_enemies.add(enemies)
            all_sprites.add(enemies)
        elif event.type == SHOOTENEMYBEAMS:
            for enemy in all_enemies:
                enemy.generateBeams(enemy.rect)

    # add  player to sprite group
    if isPlayerkilled is False:
        all_sprites.add(player)
    all_sprites.add(lives[:no_of_lives])

    # block transfer to game screen
    for i in all_sprites:
        screen.blit(i.surf, i.rect)
    
    # draw beams
    for i in enemy_beams:
        screen.blit(i.surf, i.rect)

    # #update beams
    enemy_beams.update()

    # check for movement
    keys = pygame.key.get_pressed()
    player.update(pressed_keys=keys)

    #  update new enemy sprites
    all_enemies.update()#using keyword arguments produced errors on pycharm

    # update missiles
    all_missiles.update()

    # enemy colliding with other enemies
    for enemy in all_enemies:
        if pygame.sprite.spritecollide(enemy, all_enemies, False):
            _collided = pygame.sprite.spritecollide(enemy, all_enemies, False)
            if _collided[0].rect.x > enemy.rect.x:
                _collided[0].rect.move_ip(_collided[0].rect.x + 3, 0)
                enemy.rect.move_ip(-enemy.rect.x + random.randint(0, 2), 0)
            if _collided[0].rect.x < enemy.rect.x:
                _collided[0].rect.move_ip(-_collided[0].rect.x + random.randint(0, 2), 0)
                enemy.rect.move_ip(enemy.rect.x + 3, 0)

    # check to see if enemy collides with player missiles and explosion
    enemy_collide = pygame.sprite.groupcollide(
        all_enemies, all_missiles,
        True, False
    )
    if enemy_collide:
        enemy_ = list(enemy_collide.keys())[0]
        explosion = Explosion(x=enemy_.rect.x,y=enemy_.rect.y)
        explosions.add(explosion)

    explosions.draw(screen)
    explosions.update()

    # player collision with beam
    beam = pygame.sprite.spritecollideany(player, enemy_beams)
    if beam:
        beam.kill()
        print(no_of_lives)
        print(lives[:no_of_lives])
        if no_of_lives > 0:
            no_of_lives -= 1
            for life in lives:
                life.kill()

    # check to see if player still has lives
    if no_of_lives == 0:
        isPlayerkilled = True
        player.kill()
        #running = False

    pygame.display.flip()

    clock.tick(30)