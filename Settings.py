import pygame

class Settings():

    def __init__(self, game):

        # Screen Settings
        self.screen_info = game.screen_info
        self.screen_width, self.screen_length = 780, 780
        self.screen_bg_color = (255,255,255)
        self.frame_rate = 6

        # Grid
        self.grid_size = 60
        self.border_color = (0,0,0)

        # Circles
        self.circle_color = (255, 0, 0)
        self.circle_radius = 8

        # Common
        self.radius_color = (0,0,200,0.1)

        # Environment
        self.rain_prob = 15

        # Wolf
        self.wolf_color = (255,100,100)
        self.wolf_size = 5
        self.wolf_limit = 3
        self.wolf_radius = 50
        self.wolf_speed = 1
        self.wolf_hunger = 20
        self.wolf_metabolic_rate = 2
        self.wolf_energy = 100

        # Bunny
        self.bunny_color = (10, 60, 255)
        self.bunny_size = 5
        self.bunny_limit = 10
        self.bunny_radius = 25
        self.bunny_speed = 1
        self.bunny_hunger = 5
        self.bunny_metabolic_rate = 3

        # Grass
        self.grass_life_span = 100
        self.grass_dry_time = self.grass_life_span*0.90
        self.grass_seeding_time = self.grass_life_span*0.75
        self.grass_maturity_time = self.grass_life_span*0.25

        self.grass_state = {
                "otw":{"color":(140,40,40),"energy":3},
                "young":{"color":(130,255,105),"energy":10},
                "grown":{"color":(89,222,62),"energy":15},
                "seed":{"color":(62,181,38),"energy":8},
                "dry":{"color":(176,181,38),"energy":2}
        }
        self.grass_prob = 20
        self.grass_radius = 5