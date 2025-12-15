

import logging

from grid.BaseGrid import GridPosition

logger = logging.getLogger(__name__)


class MovementObject:
    directions = [(-1,0),
                  (0,1),
                  (1,0),
                  (0,-1)]

    def __init__(self, p, n, grid):
        self.in_bounds = True
        self.position = GridPosition(p, grid=grid)
        self.direction_id = n
        self.dir = self.directions[self.direction_id]

        self.grid = grid

    def __str__(self):
        return f'{self.position}'


    def walk_to_obstacle(self, obstacle):

        p0 = self.position
        keep_walking = True
        steps = 0
        while keep_walking:

            next_step = self.position.step(self.directions[self.direction_id])

            if not next_step.is_within:
                break

            if next_step:
                if self.grid.data[next_step.position] == obstacle:
                    steps = steps + 1
                    self.position = next_step
                    break

            steps = steps + 1
            self.position = next_step

        logger.info(f'Walked {steps} steps from {p0} to {self.position}')
