# -*- coding: utf-8 -*-

"""

"""

import logging
import json

import pandas as pd
import numpy as np

from grid.BaseGrid import read_grid
from grid.GridMovement import MovementObject


logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day7.txt'

    grid = read_grid(fp)

    answer_part_one, beams = part_one(grid)
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

    all_beams = list()
    # Number of splits
    N_split = 0

    #
    generation = 0
    d = list()

    # Gather the ones crossing
    crossing = list()

    points_covered = list()
    while True:

        new_beams = list()
        for beam in beams:
            impact = beam.walk_to_obstacle('^')

            # Skip if we don't hit anything
            if not impact:
                all_beams.append((generation, beam))
                continue

            # Check if it intersects any other beam
            if len(set(beam.path).intersection(set(points_covered))) > 0:
                continue

            points_covered.extend(beam.path)
            all_beams.append((generation, beam))

            if (beam.position.position[0] == grid.r_high) and (beam.position.position not in [b.position.position for b in crossing]):
                crossing.append(beam)
                continue

            # Beam is obstacle, make a set of new beams
            new_test = list()
            for step in [[0, -1], [0, 1]]:
                n = MovementObject(beam.position.step(step).position, 2, grid=grid)

                if not n.position.is_within:
                    continue

                if n.position.position not in points_covered:
                    new_test.append(n)
                    #points_covered.extend(n.path)

            if len(new_test) > 0:
                new_beams.extend(new_test)
                N_split = N_split + 1

        logger.info('New beams: {0}'.format(','.join(list(map(str, [b.position for b in new_beams])))))

        d.append({'generation': generation, 'new_beams': len(new_beams)})
        beams = new_beams

        if len(beams) == 0:
            break

        generation = generation + 1

    mydict = dict()
    mydict['paths'] = dict()
    for idx, b in enumerate(all_beams):
        mydict['paths'][idx] = {'x': ','.join(map(str, np.array(b[1].path)[:, 0])),
                                'y': ','.join(map(str, np.array(b[1].path)[:, 1])),
                                'generation': b[0]}

    mydict['splitters'] = dict()
    for idx, s in enumerate(zip(splitters[0], splitters[1])):
        mydict['splitters'][idx] = {'x': int(s[0]), 'y': int(s[1])}

    fp = 'data/intermediate/aoc_2025_d7.json'
    with open(fp, 'w') as ofile:
        json.dump(mydict, ofile)

    fp = 'data/intermediate/aoc_2025_d7.csv'
    df = pd.DataFrame(d)
    with open(fp, 'w') as ofile:
        df.to_csv(ofile, index=False)


    return N_split, all_beams

def part_two(data):

    res = list()
    for part in data:
        values = np.array(part[:-1])
        op = part[-1][0]

        v = [int(''.join(values[:,c])) for c in range(values.shape[1])]
        res.append(parse_operator(op)(v))

    return sum(res)


