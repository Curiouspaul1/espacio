import pygame
import random
from pygame.locals import (
    K_RIGHT, K_UP, K_LEFT, K_DOWN,
    RLEACCEL
)

class Player(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.surf = pygame.image.load('assets/jet.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                game_screen[0]/2-(self.surf.get_width()/2),
                game_screen[1]-(self.surf.get_height())
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if  pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
        
        # stop player from moving off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= self.game_screen[0]:
            self.rect.right = self.game_screen[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game_screen[1]:
            self.rect.bottom = self.game_screen[1]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        super().__init__()
        self.game_screen = game_screen
        self.surf = pygame.image.load('assets/alien01.png').convert()
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, self.game_screen[0]),
                0
            )
        )
        self.speed = random.randint(5, 15)
    
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()
