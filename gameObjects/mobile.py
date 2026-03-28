from . import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)
        self.maxVelocity = 500
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)

        if hasattr(self, 'check_solid') and self.check_solid is not None:
            size = self.getSize()
            

            next_pos_x = self.position.copy()
            next_pos_x[0] += self.velocity[0] * seconds
            corners_x = [
                (next_pos_x[0], self.position[1]),
                (next_pos_x[0] + size[0] - 1, self.position[1]),
                (next_pos_x[0], self.position[1] + size[1] - 1),
                (next_pos_x[0] + size[0] - 1, self.position[1] + size[1] - 1)
            ]
            if any(self.check_solid(x, y) for x, y in corners_x):
                self.velocity[0] = 0
            else:
                self.position[0] = next_pos_x[0]

            # Try moving in y direction
            next_pos_y = self.position.copy()
            next_pos_y[1] += self.velocity[1] * seconds
            corners_y = [
                (self.position[0], next_pos_y[1]),
                (self.position[0] + size[0] - 1, next_pos_y[1]),
                (self.position[0], next_pos_y[1] + size[1] - 1),
                (self.position[0] + size[0] - 1, next_pos_y[1] + size[1] - 1)
            ]
            if any(self.check_solid(x, y) for x, y in corners_y):
                self.velocity[1] = 0
            else:
                self.position[1] = next_pos_y[1]
        else:
            self.position += self.velocity * seconds