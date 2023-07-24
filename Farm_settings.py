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

        # Wolf
        self.wolf_color = (255,100,100)
        self.wolf_radius = 5
        self.wolf_limit = 10