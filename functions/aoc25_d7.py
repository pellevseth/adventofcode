# -*- coding: utf-8 -*-

"""

"""

import logging
from math import prod

import numpy as np

from grid.BaseGrid import read_grid
from grid.GridMovement import MovementObject


logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day7_example.txt'

    grid = read_grid(fp)

    answer_part_one = part_one(grid)
    logger.info('Part one, answer is {}'.format(answer_part_one))

    # Part two
    answer_part_two = part_two(data)

    logger.info('Part two answer is {}'.format(answer_part_two))
    logger.info('Finished')


def part_one(grid):

    start_position = grid.find_coordinates_of_marker('S')
    start_position = (start_position[0][0], start_position[1][0])
    splitters = grid.find_coordinates_of_marker('^')
    beams = [MovementObject(start_position, 2, grid)]

    # Number of splits
    N_split = 0

    #
    generation = 0
    d = list()

    # Gather the ones crossing
    crossing = list()
    while True:

        new_beams = list()
        for beam in beams:
            beam.walk_to_obstacle('^')

            if (beam.position.position[0] == grid.r_high) and (beam.position.position not in [b.position.position for b in crossing]):
                crossing.append(beam)
                continue

            # Beam is obstacle, make a set of new beams
            for step in [[0, -1], [0, 1]]:
                n = MovementObject(beam.position.step(step).position, 2, grid=grid)

                if not n.position.is_within:
                    continue

                if (n.position.position[0] < grid.r_high) and (n.position.position not in [b.position.position for b in new_beams]):
                    new_beams.append(n)
                    N_split = N_split + 1

        logger.info('New beams: {0}'.format(','.join(list(map(str, [b.position for b in new_beams])))))

        d.append({'generation': generation, 'new_beams': len(new_beams)})
        beams = new_beams

        if len(beams) == 0:
            break

        generation = generation + 1

    return N_split

def part_two(data):

    res = list()
    for part in data:
        values = np.array(part[:-1])
        op = part[-1][0]

        v = [int(''.join(values[:,c])) for c in range(values.shape[1])]
        res.append(parse_operator(op)(v))

    return sum(res)


