# -*- coding: utf-8 -*-

"""

"""

import logging
import random

import numpy as np
import pandas as pd
import geopandas as gpd

from grid.BaseGrid import read_grid

logger = logging.getLogger(__name__)

def main(*args, **kwargs):

    fp = 'data/raw/aoc_2024_day10_exmample.txt'

    logger.info('Reading')
    grid = read_grid(fp)

    # Vil en genetisk algoritme ha noe for seg?

    # Finne alle start-punktene, altså de mued 0
    start_points = np.where(grid.data == '0')
    N = len(start_points)

    # Lage N antall tilfeldige spor, hvor N er antallet nuller
    paths = list()
    for sp in np.stack(start_points, axis=1):
        for i in range(10):
            paths.append(grid.make_random_path(p0=sp))
    criterion = np.mean([p.value for p in paths])

    values = list()
    values.append([p.value for p in paths])
    N = 600
    n = 1
    go=True
    data = list()
    while go:
        logger.info('Iteration: {0} ({1})'.format(n, len(paths)))

        # Rangere de på godhet typisk sum(sqrt(p0-p1))
        paths = sorted(paths, key=lambda p: p.value)

        # Drepe de dårligste
        N0 = len(paths)
        paths = [p for p in paths if p.value < criterion]
        N_killed = N0 - len(paths)

        # Dreper kopier
        N0 = len(paths)
        paths = list(set(paths))
        N_unique = N0 - len(paths)

        # Mutere noen - f.eks. splitte på et tilfeldig punkt
        N0 = len(paths)
        N_mutate = min(round(len(paths) * 0.2), 50)
        for p in paths[:N_mutate]:
            split_point = random.randint(1, len(p.points)-1)
            paths.append(p.split_and_mutate())
        N_mutate = len(paths) - N0
        # Parre noen - f.eks. ta to stk med samme utgangspunkt - la koordinatene være median av de to

        # Lage noen helt nye
        N0 = len(paths)
        N_create = np.stack(np.where(grid.data == '0'), axis=1)
        start_points = [tuple(p.points[0].position) for p in paths]
        N_create = [p for p in N_create if tuple(p) not in start_points]
        if len(N_create) == 0:
            N_create = np.stack(np.where(grid.data == '0'), axis=1)
        for i in range(0, random.randint(1, len(N_create))):
            paths.append(grid.make_random_path(p0=N_create[i]))
        N_create = len(paths) - N0

        # For monitoring of progress        
        values.append([p.value for p in paths])

        if n >= N:
            go=False

        dct = {'n': n, 'N_paths': len(paths), 'mean_value': np.mean([p.value for p in paths]),
            'max_value': np.max([p.value for p in paths]),
            'min_value': np.min([p.value for p in paths]),
            'N_killed': N_killed, 'N_mutate': N_mutate, 'N_create': N_create, 'N_unique': N_unique,
            'criterion': criterion}
        data.append(dct)

        # Se om man skal oppdatere kriteriet
        criterion = min(criterion, np.mean([p.value for p in paths]))
        n = n + 1


    # Write out results
    df = pd.DataFrame(data)
    with open('data/results/aoc_2024_day10_overall.csv', 'w') as ofile:
        df.to_csv(ofile, index=False)

    with open('data/intermediate/aoc_2024_day10.txt', 'w') as ofile:
        for v in values:
            ofile.write('{}\n'.format(','.join(['{0}'.format(vv) for vv in v])))
    
    # Collect paths
    df = pd.DataFrame([p.get_linestring().wkt for p in paths], columns=['geometry'])
    df['p0'] = [','.join(map(str, p.points[0].position)) for p in paths]
    df['value'] = [p.value for p in paths]
    df['length'] = [len(p.points) for p in paths]
    with open('data/results/aoc_2024_day10_paths.csv', 'w') as ofile:
        df.to_csv(ofile, index=False)
    
    # Write out geo for visualization
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['geometry'])).drop_duplicates(subset='geometry')
    with open('data/intermediate/aoc_2024_day10.gpkg', 'wb') as ofile:
        gdf.to_file(ofile, driver='GPKG', layer='paths')

    logger.info('Finished')