# -*- coding: utf-8 -*-

"""

"""

import logging

import numpy as np
import pandas as pd

from grid.BaseGrid import read_grid

logger = logging.getLogger(__name__)

def main(*args, **kwargs):

    fp = 'data/raw/aoc_2024_day8.txt'
    grid = read_grid(fp)

    # 1. Lage df med frekvenser

    markers = grid.find_unique()

    dfs = list()
    for m in markers:
        coords = grid.find_coordinates_of_marker(m)
        d = pd.DataFrame(coords).T
        d.columns = ['row', 'column']
        d['marker'] = m
        dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)


    # 2. For hver frekvens, finne alle de andre
    df = df.merge(df, left_on='marker', right_on='marker')

    # 3. Mål avstand mellom par-vis. Trekk diagonal i motsatt retning
    df['distance'] = df.apply(lambda r: np.sqrt((r['row_x'] - r['row_y']) ** 2 + (r['column_x'] - r['column_y']) ** 2),
                              axis=1)
    df = df.loc[df.distance > 0].copy()
    df['direction'] = df.apply(lambda r: (r['row_x'] - r['row_y'],  (r['column_x'] - r['column_y'])),
                               axis=1)
    df['p2'] = df.apply(lambda r: (r['row_x'] + r['direction'][0], r['column_x'] + r['direction'][1]),
                        axis=1)

    # 4. Hvis den er innafor, så legges den til. Ellers ikke
    df['p2_within'] = df['p2'].apply(grid.point_within)

    N = len(df.loc[df.p2_within].drop_duplicates('p2'))
    logger.info('Finished - Found {0} unique antinodes'.format(N))



