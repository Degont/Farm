import random

import pygame
import math
import random
from pygame.sprite import Sprite
import subprocess

class Wolf(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings

        # Set Up
        self.x = random.randint(0, self.settings.grid_size - 1)
        self.y = random.randint(0, self.settings.grid_size - 1)
        self.current_tile = self.game.master_grid[self.x][self.y]
        self.rect = pygame.Rect(0, 0, self.settings.wolf_size * 2, self.settings.wolf_size * 2)
        self.rect.center = self.current_tile["rect"].center

        self.color = self.game.settings.wolf_color
        self.draw_radius = self.game.show_radius_flag

        self.clock = 0

        # State
        self.state = "alive"
        self.influenced = []
        self.interactions = []
        self.awareness = []
        self.entities = {}

        # Traits
        self.species = "wolf"
        self.radius = self.settings.wolf_radius
        self.energy = self.settings.wolf_energy


    def update(self, game):

        self.game = game
        self.clock += 1

        # Metabolism
        self._metabolism()
        if self.energy <= 0:
            self.state = "dead"
            pass

        #
        else:
            self.sense_single_tile()
            self._interactions(self.current_tile, self.awareness)  # Single tile

            # Edge Cases
            if self.y == 0:
                y_inc = random.choice([1, 0])
            elif self.y == self.settings.grid_size - 1:
                y_inc = random.choice([-1, 0])
            else:
                y_inc = random.choice([-1, 1, 0])

            if self.x == 0:
                x_inc = random.choice([1, 0])
            elif self.x == self.settings.grid_size - 1:
                x_inc = random.choice([-1, 0])
            else:
                x_inc = random.choice([-1, 1, 0])

            # Movement
            self.y += y_inc * self.settings.wolf_speed
            self.x += x_inc * self.settings.wolf_speed

            # Reassinging Where to draw the animal
            self.rect.center = self.game.grid[self.y][self.x].center

    def sense_single_tile(self):
        """Single tile interactions"""
        self.current_tile = self.game.master_grid[self.y][self.x]

        friends = self.current_tile["inhabitants"]

        return friends

    def _interactions(self, current_tile=None, awareness=None):
        """Takes in """
        if current_tile:
            for friend in current_tile["inhabitants"]:
                if friend.species == "bunny":
                    self._eat(friend)
        else:
            pass

        wolf = []
        grass = []
        bunny = []

        # count + process
        if awareness:
            for tile in awareness:
                for inhabitant in tile["inhabitants"]:
                    if inhabitant.species == "wolf":
                        wolf.append(inhabitant)
                    elif inhabitant.species == "grass":
                        grass.append(inhabitant)
                    elif inhabitant.species == "bunny":
                        bunny.append(inhabitant)
                    else:
                        pass

    def _metabolism(self):
        if self.clock == self.settings.wolf_metabolic_rate:
            self.energy -= self.settings.wolf_hunger
            self.clock = 0

    def _eat(self, food):
        self.energy += food.energy
        food.state = "dead"
        self.influenced.append(food)


    def draw_wolf(self):

        if self.draw_radius == -1:
            pygame.draw.circle(self.screen, self.settings.radius_color, self.rect.center,self.settings.wolf_radius,1)

        pygame.draw.circle(self.screen, self.color, self.rect.center, self.settings.wolf_size)

subprocess.check_call('C:/Program_Files(x86)/Google/Chrome/Application/chrome')