# -*- coding: utf-8 -*-

"""

"""

import logging

import numpy as np
import pandas as pd

from grid.BaseGrid import read_grid

logger = logging.getLogger(__name__)

def main(*args, **kwargs):

    fp = 'data/raw/aoc_2024_day10_exmample.txt'

    logger.info('Reading')
    grid = read_grid(fp)

    # Vil en genetisk algoritme ha noe for seg?
    # Lage N antall tilfeldige spor, hvor N er antallet nuller
    # Rangere de på godhet typisk sum(sqrt(p0-p1))
    # Drepe de nederste
    # Mutere noen - f.eks. splitte på et tilfeldig punkt
    # Parre noen - f.eks. ta to stk med samme utgangspunkt - la koordinatene være median av de to

    logger.info('Finished')