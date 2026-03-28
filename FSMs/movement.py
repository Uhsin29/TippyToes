from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION

from statemachine import State

class MovementFSM(AbstractGameFSM):
    
    def __init__(self, obj):
        super().__init__(obj)
    
    def update(self, seconds):
        super().update(seconds)

        # Add out of bounds checks here

        if self.obj.position[self.axis] < 0:
            self.stop_decrease()
            self.obj.velocity[self.axis] = 0
            self.obj.position[self.axis] = 0
        elif self.obj.position[self.axis] > RESOLUTION[self.axis] - self.obj.getSize()[self.axis]:
            self.stop_increase()
            self.obj.velocity[self.axis] = 0
            self.obj.position[self.axis] = RESOLUTION[self.axis] - self.obj.getSize()[self.axis]



            
        # if self.obj.position[1] < 0 and self == "negative":
        #     self.stop_decrease()
        #     self.obj.velocity[1] = 0
        # elif self.obj.position[1] > RESOLUTION[1] - self.obj.getSize()[1] and self == "positive":
        #     self.stop_increase()
        #     self.obj.velocity[1] = 0
        


class AccelerationFSM(MovementFSM):
    """Axis-based acceleration with gradual stopping."""
    not_moving = State(initial=True)
    
    negative = State()
    positive = State()
    
    stalemate = State()
    
    decrease  = not_moving.to(negative) | positive.to(stalemate) | negative.to.itself(internal =True) | stalemate.to.itself(internal=True)
    
    increase = not_moving.to(positive) | negative.to(stalemate) | positive.to.itself(internal =True) | stalemate.to.itself(internal=True)
    
    stop_decrease = negative.to(not_moving) | stalemate.to(positive) | positive.to.itself(internal=True) | not_moving.to.itself(internal=True)
    
    stop_increase = positive.to(not_moving) | stalemate.to(negative) | negative.to.itself(internal=True) | not_moving.to.itself(internal=True)
    
    stop_all      = not_moving.to.itself(internal=True) | negative.to(not_moving) | \
                    positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis      = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.accel = 500
        
        super().__init__(obj)

    def update(self, seconds=0):
        if self == "positive":
            self.obj.velocity += self.direction * self.accel * seconds
        elif self == "negative":
            self.obj.velocity -= self.direction * self.accel * seconds
                
        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.accel * seconds:
                self.obj.velocity[self.axis] -= self.accel * seconds
            elif self.obj.velocity[self.axis] < -self.accel * seconds:
                self.obj.velocity[self.axis] += self.accel * seconds
            else:
                self.obj.velocity[self.axis] = 0
        
        
    
        super().update(seconds)