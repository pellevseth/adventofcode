
import numpy as np


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

    def __init__(self, data):
        self.char_open = '.'
        self.data = data
    
    def find_unique(self):
        # Return array of unique markers in the grid given a specified 'open space' to be ignored
        u = np.unique(self.data)
        return np.array([a for a in u if a != self.char_open])
    
    def find_coordinates_of_marker(self, marker):
        return np.where(self.data == marker)
    
    def point_within(self, p):
        within = True

        if (p[0] < 0) or (p[1] < 0):
            within =False
        
        if (p[0] >= self.data.shape[0]) or (p[1] >= self.data.shape[1]):
            within =False
        
        return within


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
    

