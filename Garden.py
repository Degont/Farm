import random

import pygame
import sys
from Settings import Settings
from time import sleep
import math

from wolf import Wolf
from grass import Grass
from bunny import Bunny


class Gameboard():
    """The actual game stuff"""

    def __init__(self):
        pygame.init()

        self.screen_info = pygame.display.Info()
        self.settings = Settings(self)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Garden")  # A surface is where game elements can be displayed
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_length))
        self.rect = self.screen.get_rect()

        # Data Structures
        self.grid, self.border, self.top_row, self.tile_length, self.coord = self._create_grid()
        self.color_grid = self._create_color_grid(self.grid,"yuh")
        self.inhabitants_grid = self._reset_inhabitants()
        self.master_grid = self._create_master_grid()

        # Groups
        self.grass = pygame.sprite.Group()
        self.wolf = pygame.sprite.Group()
        self.bunny = pygame.sprite.Group()
        self.circles_checked = []
        self.groups = {"grass":self.grass, "wolf":self.wolf, "bunny":self.bunny}
        self.active_group = pygame.sprite.Group()



        # Initializing Stuff
        self._fill_master_grid()
        self._fill_grass()

        # Counters
        self.rain_counter = 0

        # Flags
        self.show_radius_flag = 1


    def _increment_counters(self):
        self.rain_counter += 1

    # Game loop:

    def run_game(self):
        while True:
            self.clock.tick(self.settings.frame_rate)
            self._increment_counters()
            self._check_events()
            self._weather()
            self._update()




    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_p:
                    self._print_grid(self.master_grid)
                if event.key == pygame.K_o:
                    self.show_radius_flag *= -1
                    self._show_radius()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # this takes the position of the mouse and creates a rect for it
                self._check_mouse(mouse_pos)



    def _update(self):

    # INITIAL
        self.screen.fill(self.settings.screen_bg_color)
        self._color_grid()

    # Interactions
        self._passive_spawn()
        self._draw_creatures()

        self._update_inhabitants(self.groups)
        self._sense()
        self._update_creatures()

        self._color_border()
        pygame.display.flip()



    # Data Structures:

    def _fill_master_grid(self):
        """So this is the actual function used to fill all the things of each dictionary"""
        # So what i want here is a [[{},{},{}...],[{},{},{}...],[{},{},{}...]] for x and y's and inside each thing is a dictionary with all the characteristic
        #first would be rect, color, tile info, list of occupants- that can interact with the tile and each other,
        self._update_master_grid("rect",self.grid)
        self._update_master_grid("color",self.color_grid)
        self._update_master_grid("inhabitants",self.inhabitants_grid)
        self._update_master_grid("coords",self.coord)

    def _create_master_grid(self):

        self.master_grid = []

        for row in range(self.settings.grid_size):
            y_grid = []
            for value in range(self.settings.grid_size):
                empty_dict = {}
                y_grid.append(empty_dict)
            self.master_grid.append(y_grid)

        return self.master_grid

    def _update_master_grid(self, source_text,source_grid):
        """Takes in inputs for what grid and what it would be called in the dict, essentially the key"""

        for row, y in zip(self.master_grid, range(self.settings.grid_size)):
            for tile, x in zip(row, range(self.settings.grid_size)):
                try:
                    tile[f"{source_text}"] = source_grid[y][x]
                except TypeError:
                    print("There was an error Here")

    def _create_grid(self):
        """Creates the grid for the gameas a series of rects inside a list, list in list structure so call the things using index"""

        tile_length = self.screen.get_width() / self.settings.grid_size # dividung the screen by 8 since 8 tiles in chess
        print(f'{tile_length} This is how many units the frame is for the squares')

        grid_map = [] # choose list as data type to store my grid in
        border_map = []
        top_map = []
        coord_map = []

        for repeat_y in range(self.settings.grid_size):
            row = []
            border_row = []
            top_row = []
            coord_row = []
            row_set = 0 + (repeat_y * tile_length) # adding tile lengths to get the spacing for the grids rows
            for repeat in range(self.settings.grid_size):
                tile = pygame.Rect(0 + (repeat * tile_length), row_set, tile_length, tile_length)
                border = pygame.Rect((repeat * tile_length) - (tile_length/10), row_set, tile_length/5, tile_length)
                top_border = pygame.Rect((repeat*tile_length), row_set - (tile_length/10), tile_length, tile_length/5)
                coord = [repeat_y,repeat]

                row.append(tile) # throwing the tile rect into my list
                border_row.append(border)
                top_row.append(top_border)
                coord_row.append(coord)

            grid_map.append(row)
            border_map.append(border_row)
            top_map.append(top_row)
            coord_map.append(coord_row)

        return grid_map, border_map, top_map, tile_length, coord_map


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

    def _create_data_list(self,key = ""):
        """Takes in a key for the data base units and provides you both an ordered list
        with x and y coords and a raw list with just the items"""
        list = []
        raw_list = []

        for y in range(self.settings.grid_size):
            list_y = []
            for x in range(self.settings.grid_size):
                if key:
                    target_value = self.master_grid[y][x][key]
                    list_y.append(target_value)
                    if target_value != []:
                        for value in target_value:
                            raw_list.append(value)

                else:
                   pass
            list.append(list_y)

        return list, raw_list


    # Functions for Data Structures and Style Code

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

                # This first if is to handle the border color on the top
                if counter == 1:
                    if second_counter == 1:
                        second_counter += 1
                        continue
                    else:
                        self.screen.fill((60,74,34), collumn)
                        #self.screen.fill(self.settings.border_color, collumn)
                else:
                    if second_counter == 1:
                        second_counter += 1
                        self.screen.fill(self.settings.border_color, collumn2)
                    else:
                        self.screen.fill(self.settings.border_color,collumn)
                        self.screen.fill(self.settings.border_color,collumn2)
            counter += 1

    def _print_grid(self, grid):
        for y in grid:
            print(y)

    def _draw_circles(self):
        target = random.choice(random.choice(self.grid))
        if target in self.circles_checked:
            color = (0, 255, 255)
        else:
            color = self.settings.circle_color
            self.circles_checked.append(target)
        for circle in self.circles_checked:
            pygame.draw.circle(self.screen, color, circle.center, self.settings.circle_radius)


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


    # Environment Functions

    def _weather(self):

        # Rain
        if random.choice(range(100)) <= self.settings.rain_prob - 1:
            self.rain_counter = 0
            #print("Thank the rain gods its wet")


    # Creatures Functions

    def _draw_creatures(self):
        for grass in self.grass.sprites():
            grass.draw_grass()
        for wolf in self.wolf.sprites():
            wolf.draw_wolf()
        for bunny in self.bunny.sprites():
            bunny.draw_bunny()

    def _update_inhabitants(self,groups):

        # Resetting to keep the master grid fresh and updated
        self.active_group.empty()
        self._reset_inhabitants()
        self._update_master_grid("inhabitants",self.inhabitants_grid)

        # Going through each list and adding to master grid
        for type in groups.values():
            for species in type.sprites():

                # State Checks
                for member in species.influenced:  # -> this is for when creatures kill other creatures
                    type.remove(member)
                if species.state == "dead":        # -> When creatures die of other causes
                    type.remove(species)
                else:
                    self.master_grid[species.y][species.x]["inhabitants"].append(species)


        # Updating inhabitants grid, the temp thing,
        list, list_raw = self._create_data_list("inhabitants")

        # creating active sprite group for collisions
        for group in self.groups.values():
            if group == self.grass:
                continue
            for member in group:
                self.active_group.add(member)

        return list_raw


    def _reset_inhabitants(self):
        self.inhabitants_grid = []

        for row in range(self.settings.grid_size):
            y_grid = []
            for value in range(self.settings.grid_size):
                empty_list = []
                y_grid.append(empty_list)
            self.inhabitants_grid.append(y_grid)

        return self.inhabitants_grid

    def _update_creatures(self):
        self._update_wolf()
        self._update_grass()
        self._update_bunny()

    def _passive_spawn(self):
        if len(self.wolf) < self.settings.wolf_limit:
            self._create_wolf()

        if len(self.bunny) < self.settings.bunny_limit:
            self._create_bunny()

        if self.rain_counter == 2:
            self._fill_grass()

    def _sense(self):
        """Pulls active group of moving creatures, i.e. not grass currently, becuase its too plentiful"""
        for member in self.active_group:

            # for awareness
            awareness = []
            reach = math.ceil((member.radius - (self.tile_length/2))/self.tile_length)


            for y in range((member.y - reach),member.y + reach + 1):
                for x in range(member.x - reach, member.x + reach + 1):
                    try:
                        awareness.append(self.master_grid[y][x])
                    except IndexError:
                        continue

            member.awareness = awareness

    def _show_radius(self):

        for friend in self.groups.values():
            for species in friend:
                if self.show_radius_flag == 1:
                    species.draw_radius = 1
                else:
                    species.draw_radius = -1

    def _check_tiles(self,y,x,key = ""):
        """Returns Dict at position specified"""
        tile = self.master_grid[y][x]

        if key:
            return tile[key]
        else:
            return tile


    """GRASS"""
    def _create_grass(self,y,x):
        occupied = False

        for member in self.grass.sprites():
            if member in self.master_grid[y][x]["inhabitants"]:
                occupied = True

        if occupied == False:
            new_grass = Grass(self,y,x)
            self.grass.add(new_grass)

    def _fill_grass(self):
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                if random.choice(range(100)) <= self.settings.grass_prob - 1:
                    self._create_grass(y = y,x = x)

    def _update_grass(self):

        for grass in self.grass.copy():
            self.master_grid[grass.y][grass.x]["inhabitants"].append(grass)

        self.grass.update(self)


    """Wolves"""
    def _create_wolf(self):
        new_wolf = Wolf(self)
        self.wolf.add(new_wolf)

    def _update_wolf(self):
        self.wolf.update(self)

        for wolf in self.wolf.sprites():
            self.master_grid[wolf.y][wolf.x]["inhabitants"].append(wolf)


    """Bunnies"""
    def _create_bunny(self):
        new_bunny = Bunny(self)
        self.bunny.add(new_bunny)

    def _update_bunny(self):
        self.bunny.update(self)

        for bunny in self.bunny.sprites():
            self.master_grid[bunny.y][bunny.x]["inhabitants"].append(bunny)







if __name__ == "__main__":
    board = Gameboard()
    board.run_game()