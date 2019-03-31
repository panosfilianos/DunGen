#! /usr/bin/env python

# coding: utf-8
# map_gen.py, a simple python dungeon generator by
# James Spencer <jamessp [at] gmail.com>.

#Modded to work for the 02285 Artificial Intelligence and Multi-Agent Systems
#MAS Competition 2019 by
#Panagiotis Filianos
#Mirko Biasini
#Vittorio Carmignani

# To the extent possible under law, the person who associated CC0 with
# map_gen.py has waived all copyright and related or neighboring rights
# to map_gen.py.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

#Greatly inspired by http://www.roguebasin.com/index.php?title=A_Simple_Dungeon_Generator_for_Python_2_or_3


from __future__ import print_function

import random
import copy
import string

CHARACTER_TILES = {'stone': ' ',
                   'floor': ' ',
                   'wall': '+',
                   'corridor': ' '}

COLORS = ['blue', 'red', 'cyan', 'purple', 'green', 'orange', 'pink', 'grey', 'lightblue', 'brown']


class Generator():

    def __init__(self, width=5, height=5, max_rooms= 2, min_room_xy=2,
                 max_room_xy=3, rooms_overlap=False, random_connections=1,
                 random_spurs=3, agent_number = 1, box_number = 1, color_number = 1,  tiles=CHARACTER_TILES):
        if (agent_number > 10):
            print("Agents cannot exceed max number of 10. Changing to 10")
            agent_number = 10
        if (color_number > len(COLORS)):
            print("Colors cannot exceed max number of colors: " +str(len(COLORS)))
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = CHARACTER_TILES
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []
        self.agent_number = agent_number
        self.box_number = box_number
        self.color_number = color_number

    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0
        while(True):
            w = random.randint(self.min_room_xy, self.max_room_xy)
            h = random.randint(self.min_room_xy, self.max_room_xy)
            try:
                #fixes cases where max_room_xy is very close to width/height
                x = random.randint(1, (self.width - w -1))
                y = random.randint(1, (self.height - h -1))
                return [x, y, w, h]
            except:
                pass


    def room_overlapping(self, room, room_list):

        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:
            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.

            if (x < (current_room[0] + current_room[2]) and
                    current_room[0] < (x + w) and
                    y < (current_room[1] + current_room[3]) and
                    current_room[1] < (y + h)):
                return True

        return False

    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.

            join = None

            if join_type is 'either' and set([0, 1]).intersection(set([x1, x2, y1, y2])):
                join = 'bottom'
            elif join_type is 'either' and \
                    set([self.width - 1,self.width - 2]).intersection(set([x1, x2])) or \
                    set([self.height - 1, self.height - 2]).intersection(set([y1, y2])):
                join = 'top'
            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type
            if join is 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join is 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])
        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1
        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1
        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])

            else:
                join = join_type

            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_level(self):
        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []
        max_iters = self.max_rooms * 5
        for a in range(max_iters):
            tmp_room = self.gen_room()
            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]
                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)
            if len(self.room_list) >= self.max_rooms:
                break

        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # # do the random joins
        # for a in range(self.random_connections):
        #     room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
        #     room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
        #     self.join_rooms(room_1, room_2)
        #
        # do the spurs - makes those small dents on rooms
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][min(x1, x2) + width] = 'corridor'
            if len(corridor) == 3:
                x3, y3 = corridor[2]
                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][min(x2, x3) + width] = 'corridor'

        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                current_tile_agent = False

                #check if current tile is agent
                try:
                    float(self.level[row][col])
                    current_tile_agent = True
                except:
                    pass
                if self.level[row][col] == 'floor' or \
                    self.level[row][col] == 'corridor' or \
                    current_tile_agent:
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'
                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'
                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'
                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'
                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'
                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'
                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'
                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'

        #solve corridors breaking through wallin the last row
        for col in range(1, self.width - 1):
            if (self.level[self.height - 1][col] == 'floor' or self.level[self.height - 1][col] == 'corridor'):
                self.level[self.height - 1][col] = 'wall'

    def gen_start_goal_maps(self):
        self.goal_level = copy.deepcopy(self.level)
        self.agent_location_list_starting = []
        self.agent_location_list_finishing = []
        for agent_index in range(self.agent_number):
            self.agent_location_list_starting.append(None)
            self.agent_location_list_finishing.append(None)
            agent_x_starting = None
            agent_y_starting = None
            agent_x_finishing = None
            agent_y_finishing = None

            while(self.agent_location_list_starting[agent_index] == None):
                #yes the following are opposite because of the bad way that self.level is defined
                agent_x_starting = random.randint(0, self.height-1)
                agent_y_starting = random.randint(0, self.width-1)
                if(self.level[agent_x_starting][agent_y_starting] == 'floor' or
                        self.level[agent_x_starting][agent_y_starting] == 'corridor'):
                    self.level[agent_x_starting][agent_y_starting] = agent_index
                    self.agent_location_list_starting[agent_index] = (agent_x_starting, agent_y_starting)

        self.box_location_list_starting = []
        self.box_location_list_finishing = []
        self.box_letters_list = []
        for box_index in range(self.box_number):
            self.box_location_list_starting.append(None)
            self.box_location_list_finishing.append(None)
            box_x_starting = None
            box_y_starting = None
            box_x_finishing = None
            box_y_finishing = None

            box_letter = random.choice(string.ascii_uppercase)
            self.box_letters_list.append(box_letter)
            while(self.box_location_list_starting[box_index] == None):
                box_x_starting = random.randint(0, self.height-1)
                box_y_starting = random.randint(0, self.width-1)
                if(self.level[box_x_starting][box_y_starting] == 'floor' or
                        self.level[box_x_starting][box_y_starting] == 'corridor'):
                    self.level[box_x_starting][box_y_starting] = box_letter
                    self.box_location_list_starting[box_index] = (box_x_starting, box_y_starting)

            while(self.box_location_list_finishing[box_index] == None):
                box_x_finishing = random.randint(0, self.height - 1)
                box_y_finishing = random.randint(0, self.width - 1)
                while (box_y_finishing == box_x_finishing and
                       box_x_finishing == box_x_starting):
                    box_x_finishing = random.randint(0, self.height - 1)
                    box_y_finishing = random.randint(0, self.width - 1)
                if(self.goal_level[box_x_finishing][box_y_finishing] == 'floor' or
                        self.goal_level[box_x_finishing][box_y_finishing] == 'corridor'):
                    self.goal_level[box_x_finishing][box_y_finishing] = box_letter
                    self.box_location_list_finishing[box_index] = (box_x_finishing, box_y_finishing)
        return set(self.box_letters_list)


    def return_color_dict(self):
        color_dict = {}
        assigned_agents = []
        assigned_boxes = []
        agent_list = [str(x) for x in list(range(self.agent_number))]
        #assign at least one agent per color
        for color_num in range(self.color_number):
            random_color = random.choice(COLORS)
            while(random_color in color_dict):
                random_color = random.choice(COLORS)
            color_dict[random_color] = []
            random_agent = random.choice(agent_list)
            #make sure that colors are less than agents in every case
            if(not(random_agent in assigned_agents)):
                assigned_agents.append(random_agent)
                color_dict[random_color].append(random_agent)

        #assign the rest agents to the selected colors
        for agent in agent_list:
            if (not(agent in assigned_agents)):
                random_color = random.choice(list(color_dict.keys()))
                assigned_agents.append(agent)
                color_dict[random_color].append(agent)

        #assign boxes to the selected colors
        for box_letter in set(self.box_letters_list):
            random_color = random.choice(list(color_dict.keys()))
            color_dict[random_color].append(box_letter)

        return color_dict

    def print_colors_in_file(self, file):
        color_dict = self.return_color_dict()
        print("#colors", end = '\n', file=file)
        for color,color_list in color_dict.items():
            print(color, end=": ", file=file)
            for index,item in enumerate(color_list):
                if index != len(color_list) -1 :
                    print(item, end=", ", file=file)
                else:
                    print(item, end = '\n', file=file)


    def input_printable_tiles(self, map, map_list):
        for row_num, row in enumerate(map):
            tmp_tiles = []
            for col_num, col in enumerate(row):
                #if col is agent
                try:
                    float(col)
                    tmp_tiles.append(str(col))
                    continue
                except:
                    pass
                if col == 'stone':
                    tmp_tiles.append(self.tiles['stone'])
                elif col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])
                elif col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])
                elif col == 'corridor':
                    tmp_tiles.append(self.tiles['corridor'])
                #box case
                else:
                    tmp_tiles.append(col)
            map_list.append(''.join(tmp_tiles))



    #map something like self.level
    def gen_tiles_level(self, map = None, file = None, domain = "dungeon", filename = None):

        self.start_printable_tiles = []
        self.goal_printable_tiles = []

        self.input_printable_tiles(self.level, self.start_printable_tiles)
        self.input_printable_tiles(self.goal_level, self.goal_printable_tiles)

        print("#domain", end = '\n', file=file)
        print(domain, end = '\n', file=file)
        print("#levelname", end = '\n', file=file)
        print(filename, end = '\n',file=file)
        self.print_colors_in_file(file=file)
        if (file == None):
            [print(row) for row in self.start_printable_tiles]
        else:
            print("#initial", end = '\n', file=file)
            [print(row, end = '\n', file=file) for row in self.start_printable_tiles]
            print("#goal",end = '\n', file=file)
            [print(row, end = '\n',file=file) for row in self.goal_printable_tiles]
            print("#end", end = '\n',file=file)

# if __name__ == '__main__':
#     gen = Generator()
#     gen.gen_level()
#     gen.gen_tiles_level()