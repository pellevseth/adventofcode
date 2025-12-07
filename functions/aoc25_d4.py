# -*- coding: utf-8 -*-

"""

"""

import logging

import numpy as np
from grid.BaseGrid import read_grid

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day4.txt'
    grid = read_grid(fp)

    # Find coordinates of each paper roll
    row, col = grid.find_coordinates_of_marker('@')

    data = list()
    for r, c in zip(row, col):
        n = grid.get_neighbours(r, c)
        if len(np.where(n.flatten() == '@')[0]) <= 4:
            data.append((r, c))

    logger.info('Finished')


def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = [l.replace('\n', '') for l in ifile.readlines()]
    return lines
