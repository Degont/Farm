import random

import pygame
import math
import random
from pygame.sprite import Sprite

class Grass(Sprite):
    def __init__(self, game, y, x):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.species = "grass"


        # State
        self.state = "otw"

        self.water = 0
        self.sunlight = 0
        self.awareness = []
        self.interactions = []
        self.energy = self.game.settings.grass_state[self.state]["energy"]
        self.influenced = []


        # traits
        self.color = self.game.settings.grass_state[self.state]["color"]
        self.radius = self.settings.grass_radius

        self.clock = 0
        self.germination_timer = random.randint(0,11)

        # Origin
        self.x = x
        self.y = y

        # Make Rect
        self.rect = self.game.master_grid[self.y][self.x]["rect"]
        self.rect.center = self.game.master_grid[self.y][self.x]["rect"].center


    def update(self, game):
        """This is what determines the path of the bullet"""
        self.game = game

        if self.germination_timer > 0:
            self.germination_timer -= 1
        else:
            if self.clock == 0:
                self.state = "young"
                self.clock += 1
            else:
                # Time Stuff
                self.clock += 1

                if self.clock == self.settings.grass_maturity_time:
                    self.state = "grown"
                elif self.clock == self.settings.grass_seeding_time:
                    self.state = "seed"
                elif self.clock == self.settings.grass_dry_time:
                    self.state = "dry"

                # Update traits
                self.energy = self.game.settings.grass_state[self.state]["energy"]
                self.color = self.game.settings.grass_state[self.state]["color"]

                if self.clock == self.settings.grass_life_span:
                    self.state = "dead"



    def draw_grass(self):
        pygame.draw.rect(self.screen, self.color, self.rect)