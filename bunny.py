import random

import pygame
import math
import random
from pygame.sprite import Sprite

class Bunny(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings

        # Set Up
        self.species = "bunny"
        self.color = self.game.settings.bunny_color
        self.draw_radius = self.game.show_radius_flag
        self.clock = 0


        # State
        self.state = "alive"
        self.x = random.randint(0, self.settings.grid_size - 1)
        self.y = random.randint(0, self.settings.grid_size - 1)
        self.current_tile = self.game.master_grid[self.x][self.y]
        self.interactions = []
        self.awareness = []
        self.entities = {}
        self.energy = 100

        # Traits
        self.radius = self.settings.bunny_radius

        # Enivornment
        self.influenced = []

        # Make bullet Rect
        self.rect = pygame.Rect(0, 0, self.settings.bunny_size*2, self.settings.bunny_size*2)
        self.rect.center = self.current_tile["rect"].center


    def update(self,game):
        """This is what determines the path of the bullet"""

        self.game = game


        # Interactions
        self.clock += 1
        self._metabolism()

        if self.state == "dead":
            pass
        elif self.energy <= 0:
            self.state = "dead"
            pass
        else:
            self.sense_single_tile()
            self._interactions(self.current_tile,self.awareness) # Single tile

            # Edge Cases
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

            # Movement
            self.y += y_inc * self.settings.bunny_speed
            self.x += x_inc * self.settings.bunny_speed

            # Reassinging Where to draw the animal
            self.rect.center = self.game.grid[self.y][self.x].center



    def sense_single_tile(self):
        """Single tile interactions"""
        self.current_tile = self.game.master_grid[self.y][self.x]

        friends = self.current_tile["inhabitants"]

        return friends



    def _interactions(self,current_tile = None, awareness = None):
        """Takes in """
        if current_tile:
            for friend in current_tile["inhabitants"]:
                if friend.species == "grass":
                    self._eat_grass(friend)
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




    # Unique Functions

    def _eat_grass(self,grass):
        self.energy += grass.energy
        grass.state = "dead"
        self.influenced.append(grass)

    def _metabolism(self):

        if self.clock == self.settings.bunny_metabolic_rate:
            self.energy -= self.settings.bunny_hunger
            self.clock = 0


    def draw_bunny(self):

        if self.draw_radius == -1:
            pygame.draw.circle(self.screen, self.settings.radius_color, self.rect.center,self.settings.bunny_radius,1)

        pygame.draw.circle(self.screen, self.color, self.rect.center, self.settings.bunny_size)


    def _process_awareness(self):
        """Takes my expanded Tile list of entities and creates a sorted dictionary using their names"""
        self.entities = {}
        friends = []
        for tile in self.awareness:
            for species in tile["inhabitants"]:
                friends.append(species)

        friends_species = set(friends)

        for species in friends_species:
            self.entities[species] = [indiv for indiv in friends if indiv.species == species]
