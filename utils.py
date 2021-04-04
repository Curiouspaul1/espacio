import pygame
import random
from pygame.locals import (
    K_RIGHT, K_UP, K_LEFT, K_DOWN,
    RLEACCEL
)

enemy_beams = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.surf = pygame.image.load('assets/jet.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                game_screen[0]/2-(self.surf.get_width()/2),
                game_screen[1]-(self.surf.get_height())
            )
        )
        self.life = None

    def update(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if  pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        
        # stop player from moving off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= self.game_screen[0]:
            self.rect.right = self.game_screen[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game_screen[1]:
            self.rect.bottom = self.game_screen[1]


#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"assets/exp{num}.png")
			img = pygame.transform.scale(img, (50, 50))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


class EnemyBeams(pygame.sprite.Sprite):
    def __init__(self, enemy_rect, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.enemy_rect = enemy_rect
        self.surf = pygame.image.load('assets/beams1.png')
        self.rect = self.surf.get_rect(
            center = (
                enemy_rect.x+(self.surf.get_width()*2),
                enemy_rect.y+(self.surf.get_height()*2)
            )
        )
        self.speed = 14
    
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > self.game_screen[1]:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.surf = pygame.image.load(f'assets/alien0{random.randint(1,4)}.png').convert()
        self.surf.set_colorkey((0,  0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, game_screen[0]), #changed the player default x position
                0   #made it so that the enemies come out the top of the screen
            )
        )
        self.beam = None
        self.speed_y = 5
        self.speed_x = random.choice([3.5, -3.5, 0])#the x-movement can either be forward, backward or stagnant
    
    def update(self):
        #i also changed this function...so that diagonally moving enemies wont just falloff
        #instead hey continue on the other side

        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.x > self.game_screen[0]:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = self.game_screen[0]
    
    def generateBeams(self, pos):
        self.beam = EnemyBeams(enemy_rect=pos, game_screen=self.game_screen)
        enemy_beams.add(self.beam)


class EnemyGroup(pygame.sprite.Group):
    def generateBeams(self, *args, **kwargs):
        print("working")
        """
        Generates beams from enemy sprites
        """

class Missile(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load('assets/missile1.png')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                player.rect.x+(self.surf.get_width()),
                player.rect.y-(self.surf.get_height())
            )
        )
        self.speed = 14

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()


class hearts(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("assets/heart01.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = pos
        )
