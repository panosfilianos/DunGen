# DunGen
A 2-D Dungeon Generator in Python 3

## How to run
Clone the repo and just
```
python generate_fifty_maps.py
```

This script will create the `/lvls` folder in your current directory and create inside it a set of fifty, progressively harder levels for the multi-agent domain, abiding by the structure and feel of the hospital domain (dungeon-like environment). 

Check the parameters passed and play with them to create maps to your liking.

## Notes
Please note that the current script does __NOT__ guarantee the creation of a set of solvable maps. Furthermore, the assignment of colors should work but in case you find any mistakes feel free to contribute to the code, or open an issue to discuss it

Furthermore, note that the last 10 maps generated don't comply with the 50x50 limitation of the course.

## Acknowledgements
map_gen.py, is a simple python dungeon generator by
James Spencer <jamessp [at] gmail.com>.

It was modded to work for the 02285 Artificial Intelligence and Multi-Agent Systems MAS Competition 2019 by

Panagiotis Filianos, https://github.com/scoupafi

Mirko Biasini, https://github.com/mirkobiasini

Vittorio Carmignani, https://github.com/carmignanivittorio

To the extent possible under law, the person who associated CC0 with
map_gen.py has waived all copyright and related or neighboring rights
to map_gen.py.

You should have received a copy of the CC0 legalcode along with this
work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

Greatly inspired by http://www.roguebasin.com/index.php?title=A_Simple_Dungeon_Generator_for_Python_2_or_3
