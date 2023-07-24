import random

import pygame
import math
import random
from pygame.sprite import Sprite

class Wolf(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.color = self.game.settings.wolf_color

        # Origin
        self.x = random.randint(0,self.settings.grid_size - 1)
        self.y = random.randint(0,self.settings.grid_size - 1)
        self.origin = self.game.grid[self.x][self.y]

        # Make bullet Rect
        self.rect = pygame.Rect(0, 0, self.settings.wolf_radius*2, self.settings.wolf_radius*2)
        self.rect.center = self.origin.center


    def update(self):
        """This is what determines the path of the bullet"""

        # movement stuff
        if self.y == 0:
            y_inc = random.choice([1,0])
        elif self.y == self.settings.grid_size - 1:
            y_inc = random.choice([-1,0])
        else:
            y_inc = random.choice([-1,1,0])

        if self.x == 0:
            x_inc = random.choice([1,0])
        elif self.x == self.settings.grid_size - 1:
            x_inc = random.choice([-1,0])
        else:
            x_inc = random.choice([-1,1,0])

        # contingencies
        self.y += y_inc
        self.x += x_inc

        self.rect.center = self.game.grid[self.x][self.y].center

    def draw_wolf(self):
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.settings.wolf_radius)


print(range(60))

val = []


for a in range(60):
    val.append(a)
    print(val[a],f'{a}')