"""
Helper functions
"""
from utils import *

def spawnEnemies(screen):
    spawns = []
    for i in range(2):
        enemy = Enemy(game_screen=screen)
        spawns.append(enemy)
    return spawns
