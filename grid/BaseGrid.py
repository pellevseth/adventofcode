
import logging

import random


import numpy as np
from shapely.geometry import LineString
from scipy.spatial.distance import pdist


logger = logging.getLogger(__name__)

def read_grid(fp):
    f = open(fp, 'r')
    txt = f.read()

    a = [s for s in txt.split('\n')]
    lst = []
    for s in a:
        n = []
        for ss in s:
            n.append(ss)
        lst.append(n)
    return BaseGrid(np.array(lst))


class BaseGrid:
    directions = [(-1,0), (0,1), (1,0), (0,-1)]

    def __init__(self, data):
        self.char_open = '.'
        self.data = data

        self.r_low = 0
        self.r_high = self.data.shape[0]
        self.c_low = 0
        self.c_high = self.data.shape[1]
    
    def find_unique(self):
        # Return array of unique markers in the grid given a specified 'open space' to be ignored
        u = np.unique(self.data)
        return np.array([a for a in u if a != self.char_open])
    
    def find_coordinates_of_marker(self, marker):
        return np.where(self.data == marker)

    def get_neighbours(self, r, c):
        """
        Get the neighbouts from coordinate r, c
        """
        r_low = np.clip(r-1, a_min=self.r_low, a_max=self.r_high)
        r_high = np.clip(r+1, a_min=self.r_low, a_max=self.r_high)
        c_low = np.clip(c-1, a_min=self.c_low, a_max=self.c_high)
        c_high = np.clip(c+1, a_min=self.c_low, a_max=self.c_high)
        return self.data[r_low:r_high+1,c_low:c_high+1]

    def point_within(self, p):
        within = True

        if (p[0] < 0) or (p[1] < 0):
            within =False
        
        if (p[0] >= self.data.shape[0]) or (p[1] >= self.data.shape[1]):
            within =False
        
        return within
        
    def make_random_path(self, p0, length = 10):

        #if not p0:
        #    p0 = (random.randint(self.r_low, self.r_high), random.randint(self.c_low, self.c_high))
        
        # Make a random list of steps
        steps = [self.directions[random.randint(0, 3)] for i in range(0, length-1)]
        logger.debug(steps)

        pos = GridPosition(p0, grid=self)
        coords = [pos]
        for s in steps:
            p1 = GridPosition(pos.position, grid=self)
            p1.step(s)

            # 
            while not p1.within and not tuple(p1.position) in [tuple(p.position) for p in coords]:
                p1 = GridPosition(pos.position, grid=self)
                p1.step(self.directions[random.randint(0, 3)])

            coords.append(p1)
            pos = p1
        
        return GridPath(coords, grid=self)
    

class GridPath:
    def __init__(self, points, grid=False):
        self.points = points
        self.grid = grid
        self.hash = hash(self.get_linestring().wkt)

        self.set_value()
    
    def __eq__(self, other):
        self.hash == other.hash

    def __hash__(self):
        return self.hash
    
    def set_value(self):
        v = np.array([int(self.grid.data[p.position[0]][p.position[1]]) for p in self.points])
        self.value = sum([(j-i)**2 for i, j in zip(v[:-1], v[1:])])
        self.path_values = v

        # If not ascending increase value
        if not np.all(v[:-1] <= v[1:]):
            self.value = self.value * 100

    def is_ascending(self):
        return np.all(self.path_values[:-1] <= self.path_values[1:])
    
    def split_and_mutate(self, split_point=None):

        if not split_point:
            for i in range(1, len(self.points)):
                v = np.array([int(self.grid.data[p.position[0]][p.position[1]]) for p in self.points[:i+1]])
                if not np.all(v[:-1] <= v[1:]):
                    split_point = i
                    break

                # If we go all the way through we split at random
                split_point = random.randint(1, len(self.points) - 1)
        
        arr = self.points[:split_point]
        arr2 = self.grid.make_random_path(p0=(arr[-1].position[0], arr[-1].position[1]), length=len(self.points) - split_point + 1)
        return GridPath(np.concatenate([arr, [p for p in arr2.points[1:]]]), grid=self.grid)

    
    def get_linestring(self):
        return LineString([p.position for p in self.points])


class GridPosition:
    def __init__(self, p, grid=False):
        self.position = p
        self.grid = grid

        if self.grid:
            self.within = self.grid.point_within(self.position)
    
    def step(self, direction):
        self.position = np.array(list(map(lambda i, j: i + j, self.position, direction)))
        
        # Check if we are within a given grid
        self.within = self.grid.point_within(self.position)
        if self.within:
            ret = 0
        else:
            ret = 1

        return ret


class GuardState:
    directions = [(-1,0),
                  (0,1),
                  (1,0),
                  (0,-1)]

    def __init__(self, p, n, grid):
        self.in_bounds = True
        self.position = p
        self.direction_id = n
        self.dir = self.directions[self.direction_id]

        self.paths = list()
        self.position_list = list()

        self.grid = grid
        self.errors = list()

        self.steps = list()
    
    def walk_to_obstacle(self, grid):

        # Keep the original position
        p0 = self.position

        keep_walking = True
        steps = 0
        while keep_walking:

            if not self.position in self.position_list:
                self.position_list.append(self.position)

            if self.grid[self.position] == '#':
                self.errors.append(self.position)
            self.grid[self.position] = 'X'
            
            next_step = tuple(map(lambda i, j: i + j, self.position, self.dir))
            #print(next_step)

            # Out of bounds?
            if (next_step[0] >= self.grid.shape[0]) or (next_step[1] >= self.grid.shape[1]) or (next_step[0] < 0) or (next_step[1] < 0):
                self.in_bounds = False
                self.steps.append(steps)
                self.paths.append([p0, self.position])
                return 1
            
            # Stop if next is a #
            try:
                if grid[next_step] == '#':
                    break
            except IndexError:
                self.in_bounds = False
                return 1

            steps = steps + 1
            self.position = next_step
        
        self.steps.append(steps)
        self.paths.append([p0, self.position])
        print('Walked {0} steps from {1} to {2}'.format(steps, p0, self.position))

        return 0
    
    def rotate(self):
        self.direction_id = self.direction_id + 1
        if self.direction_id == 4:
            self.direction_id = 0
        self.dir = self.directions[self.direction_id]
    

