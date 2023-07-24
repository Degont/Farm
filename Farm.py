import random

import pygame
import sys
from Farm_settings import Settings
from time import sleep

from wolf import Wolf


class Gameboard():
    """The actual game stuff"""

    def __init__(self):
        pygame.init()

        self.screen_info = pygame.display.Info()
        self.settings = Settings(self)
        self.clock = pygame.time.Clock()

        # Set Up
        self.wolf = pygame.sprite.Group()
        self.circles_checked = []


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_length))

        self.rect = self.screen.get_rect()




        self.grid, self.border, self.top_row = self._create_grid()
        self.color_grid = self._create_color_grid(self.grid,"yuh")
        self.master_grid = self._create_master_grid()



    # Game loop:

    def run_game(self):
        while True:
            self.clock.tick(self.settings.frame_rate)
            self._update()
            self._check_events()



    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_p:
                    self._print_grid(self.master_grid['w_1'])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # this takes the position of the mouse and creates a rect for it
                self._check_mouse(mouse_pos)



    def _update(self):

    # INITIAL
        self.screen.fill(self.settings.screen_bg_color)
        self._color_grid()
        self._color_border()

        self._update_creatures()
        for wolf in self.wolf.sprites():
            wolf.draw_wolf()

        pygame.display.flip()


    # Set Up:

    def _create_grid(self):
        """Creates the grid for the gameas a series of rects inside a list, list in list structure so call the things using index"""

        tile_length = self.screen.get_width() / self.settings.grid_size # dividung the screen by 8 since 8 tiles in chess
        print(f'{tile_length} This is how many units the frame is for the squares')

        grid_map = [] # choose list as data type to store my grid in
        border_map = []
        top_map = []

        for repeat in range(self.settings.grid_size):
            row = []
            border_row = []
            top_row = []
            row_set = 0 + (repeat * tile_length) # adding tile lengths to get the spacing for the grids rows
            for repeat in range(self.settings.grid_size):
                tile = pygame.Rect(0 + (repeat * tile_length), row_set, tile_length, tile_length)
                border = pygame.Rect((repeat * tile_length) - (tile_length/10), row_set, tile_length/5, tile_length)
                top_border = pygame.Rect((repeat*tile_length), row_set - (tile_length/10), tile_length, tile_length/5)
                row.append(tile) # throwing the tile rect into my list
                border_row.append(border)
                top_row.append(top_border)
            grid_map.append(row)
            border_map.append(border_row)
            top_map.append(top_row)
        return grid_map, border_map, top_map

    def _print_grid(self,grid):

        for y in grid:
            print(y)





    def _create_master_grid(self):

        self.master_grid = {}

        self.master_grid['w_1'] = []


        for row in range(self.settings.grid_size):
            y_grid = []
            for value in range(self.settings.grid_size):
                empty_dict = {}
                y_grid.append(empty_dict)
            self.master_grid['w_1'].append(y_grid)

        self._fill_master_grid()

        return self.master_grid

    def _into_master_grid(self, source_text,source_grid):
        """Takes in inputs for what grid and what it would be called in the dict, essentially the key"""

        for row, y in zip(self.master_grid["w_1"], range(self.settings.grid_size)):
            for tile, x in zip(row, range(self.settings.grid_size)):
                try:
                    tile[f"{source_text}"] = source_grid[y][x]
                except TypeError:
                    print("There was an error Here")

    def _fill_master_grid(self):
        """So this is the actual function used to fill all the things of each dictionary"""
        # So what i want here is a [list[list[]]] for x and y's and inside each thing is a dictionary with all the characteristic
        #first would be rect, color, tile info, list of occupants- that can interact with the tile and each other,
        self._into_master_grid("rect",self.grid)
        self._into_master_grid("color",self.color_grid)

    def _draw_circles(self):
        target = random.choice(random.choice(self.grid))
        if target in self.circles_checked:
            color = (0,255,255)
        else:
            color = self.settings.circle_color
        self.circles_checked.append(target)
        for circle in self.circles_checked:
            pygame.draw.circle(self.screen, color, circle.center, self.settings.circle_radius)

    def _create_color_grid(self, grid, alt = ""):
        """Gives color to a grid"""
        color_grid = []

        if not alt:
            color_counter = -1

            for row in grid:
                row_colors = []
                repeat = 0
                for collumn in row:
                    if color_counter == -1:
                        tile_color = (0, 0, 0)
                    else:
                        tile_color = (self.settings.screen_bg_color)
                    row_colors.append(tile_color)
                    if repeat != (len(grid) - 1):  # this alternates the color of the thing except at the end
                        color_counter *= -1
                    repeat += 1
                color_grid.append(row_colors)
        else:
            for row in grid:
                row_colors = []
                for collumn in row:
                    tile_color = (self.settings.screen_bg_color)
                    row_colors.append(tile_color)

                color_grid.append(row_colors)

        return color_grid

    def _color_grid(self):
        """USing both grids to color the screen"""

        for row, row_c in zip(self.grid,self.color_grid):
            for tile, tile_c in zip(row,row_c):
                self.screen.fill(tile_c,tile)

    def _color_border(self):
        counter = 1

        for row, row2 in zip(self.border,self.top_row):
            second_counter = 1
            for collumn, collumn2 in zip(row,row2):
                if counter == 1:
                    if second_counter == 1:
                        second_counter += 1
                        continue
                    else:
                        self.screen.fill(self.settings.border_color, collumn)
                else:
                    if second_counter == 1:
                        second_counter += 1
                        self.screen.fill(self.settings.border_color, collumn2)
                    else:
                        self.screen.fill(self.settings.border_color,collumn)
                        self.screen.fill(self.settings.border_color,collumn2)
            counter += 1

    # Interaction Code
    def _check_mouse(self,mouse_pos):
        for row, row_c, x in zip(self.grid, self.color_grid, range(self.settings.grid_size)):
            for tile, tile_c, y in zip(row, row_c, range(self.settings.grid_size)):
                tile_clicked = tile.collidepoint(mouse_pos)
                if tile_clicked:
                    self.color_grid[x][y] = (255,0,0) # by having color grid be a thing we can interact with its easy to change and reference the data
                    print(f"{x}{y}")
                    print(len(self.grid)*len(row))
                else:
                    pass

    # Creatures Functions

    def _check_tiles(self,x,y):
        rect = self.grid[x][y]
        return self.master_grid[rect]

    def _update_creatures(self):
        self._update_wolf()

    def _update_wolf(self):
        if len(self.wolf) < self.settings.wolf_limit:
            self._create_wolf()
        self.wolf.update()

    def _create_wolf(self):
        new_wolf = Wolf(self)
        self.wolf.add(new_wolf)




if __name__ == "__main__":
    board = Gameboard()
    board.run_game()