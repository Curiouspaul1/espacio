import pygame
import random
from pygame.locals import (
    K_RIGHT, K_UP, K_LEFT, K_DOWN,
    RLEACCEL
)

explosions = pygame.sprite.Group()


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_screen):
        super().__init__()
        self.game_screen = game_screen
        #self.position = {'left':0, 'right':self.game_screen[0]}
        self.surf = pygame.image.load(f'assets/alien0{random.randint(1,4)}.png').convert()
        self.surf.set_colorkey((0,  0, 0), RLEACCEL)
        #self.xpos = self.position[random.choice(list(self.position.keys()))]  #this line wasn't used, so i commented it out
        #print(self.xpos)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, game_screen[0]), #changed the player default x position
                0   #made it so that the enemies come out the top of the screen
            )
        )
        self.speed_y = 1
        self.speed_x = random.choice([1, -1, 0])#the x-movement can either be forward, backward or stagnant
    
    def update(self, all_missiles):
        #i also changed this function...so that diagonally moving enemies wont just falloff
        #instead hey continue on the other side

        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.x > self.game_screen[0]:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = self.game_screen[0]
        if pygame.sprite.spritecollideany(self, all_missiles):
            self.kill()
            explosion = Explosion(x=self.rect.x,y=self.rect.y)
            explosions.add(explosion)

class Missile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.surf = pygame.image.load('assets/missile1.png')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                player.rect.x+(self.surf.get_width()),
                player.rect.y-(self.surf.get_height())
            )
        )
        self.speed = 4

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()
