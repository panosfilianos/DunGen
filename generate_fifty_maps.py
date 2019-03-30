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

from map_gen import *
import os

#This script will create the /lvls folder in your current directory 
#and create inside it a set of fourty, progressively harder levels for the
#multi-agent domain, abiding by the structure and feel of the
#hospital domain (dungeon-like environment). Check the parameters passed and 
#play with them to create maps to your liking.

#Please note that the current script does NOT guarantee the creation of a set of
#solvable maps. Furthermore, the assignment of colors should work but in case you find
#any mistakes feel free to contribute to the code, or open an issue to discuss it

if __name__ == "__main__":
    if not os.path.exists('./lvls'):
        os.mkdir('lvls')
    for map_index in range(1, 41):
        width = 12 + map_index
        height = 10 + map_index
        max_rooms = int(map_index / 5) + 1
        min_room_xy = int(width / 5)
        max_room_xy = int(width / 3)
        random_spurs = 3 + int(map_index / 10)


        #generate easy map for same dimensions
        agent_number_easy = int(map_index / 5) + 1
        box_number_easy = int(map_index / 5) + 2
        color_number_easy = int(map_index / 10) + 1
        gen = Generator(width = width,
                        height = height,
                        max_rooms = max_rooms,
                        min_room_xy = min_room_xy,
                        max_room_xy = max_room_xy,
                        random_spurs=random_spurs,
                        agent_number = agent_number_easy,
                        box_number = box_number_easy,
                        color_number = color_number_easy)
        gen.gen_level()
        gen.gen_start_goal_maps()
        gen.gen_tiles_level()
        lvl_filename = "DunGen"+ str(width) + "_" + str(height) + "_e"
        with open('./lvls/' + lvl_filename, 'w') as f:
            gen.gen_tiles_level(file= f, domain = "hospital", filename = lvl_filename)

        # generate hard map
        agent_number_hard = int(map_index / 3) + 1
        box_number_hard = int(map_index / 3) + 2
        color_number_hard = int(map_index / 7) + 1
        gen = Generator(width = width,
                        height = height,
                        max_rooms = max_rooms,
                        min_room_xy = min_room_xy,
                        max_room_xy = max_room_xy,
                        random_spurs=random_spurs,
                        agent_number = agent_number_hard,
                        box_number = box_number_hard,
                        color_number = color_number_hard)
        gen.gen_level()
        gen.gen_start_goal_maps()
        gen.gen_tiles_level()
        lvl_filename = "DunGen"+ str(width) + "_" + str(height) + "_h"
        with open('./lvls/' + lvl_filename, 'w') as f:
            gen.gen_tiles_level(file= f, domain = "hospital", filename=lvl_filename)



