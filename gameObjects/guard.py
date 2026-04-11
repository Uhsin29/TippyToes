from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION
import math

from pygame.locals import *

import pygame
import numpy as np

class Guard(Mobile):
    def __init__(self, position, check_solid=None, patrol_axis="horizontal", turn_timer=2.0, facing="right"):
        super().__init__(position, "guard.png")
        self.check_solid = check_solid
        # Animation variables
        self.framesPerSecond = 2 
        self.nFrames = 1
        self.nFramesList = {
            "moving"   : 0,
            "standing" : 0
        }
        self.rowList = {
           "moving"   : 0,
           "standing" : 0
        }
        self.framesPerSecondList = {
           "moving"   : 2,
           "standing" : 2
        }
        self.FSManimated = WalkingFSM(self)
        self.LR = AccelerationFSM(self, axis=0)
        self.UD = AccelerationFSM(self, axis=1)
  
        if patrol_axis == "stationary":
            if facing == "down":
                self.direction = 1
            elif facing == "up":
                self.direction = -1
            else:
                self.direction = 1 
        else:
            self.direction = 1
        self.patrol_speed = 100
        self.vision_angle = math.radians(60)  # 60 degree cone
        self.vision_distance = 200
        self.check_solid = check_solid
        self.kirby_pos = None
        self.chase_timer = 0
        self.patrol_axis = patrol_axis
        self.turn_interval = turn_timer
        self.turn_timer = turn_timer
        self.facing = facing
    def kirby_in_vision(self):
        if self.kirby_pos is None:
            return False
        guard_pos = self.position
        dx, dy = self.kirby_pos[0] - guard_pos[0], self.kirby_pos[1] - guard_pos[1]
        distance = math.hypot(dx, dy)
        if distance > self.vision_distance:
            return False

        if self.patrol_axis == "horizontal":
            facing_angle = 0 if self.direction == 1 else math.pi
        elif self.patrol_axis == "vertical" or self.patrol_axis == "stationary":
            facing_angle = math.pi / 2 if self.direction == 1 else -math.pi / 2
        else:
            facing_angle = 0 if self.direction == 1 else math.pi
        facing_vec = (math.cos(facing_angle), math.sin(facing_angle))
        to_kirby_vec = (dx / distance, dy / distance) if distance != 0 else (0, 0)
        dot = facing_vec[0]*to_kirby_vec[0] + facing_vec[1]*to_kirby_vec[1]
        angle = math.acos(dot) if -1 <= dot <= 1 else 0
        return angle < self.vision_angle / 2
    
    def update(self, seconds):
        if self.chase_timer > 0:
            self.chase_timer -= seconds
            if self.chase_timer < 0:
                self.chase_timer = 0

        if self.kirby_in_vision() and self.has_line_of_sight(self.kirby_pos):
            if self.chase_timer == 0:
                self.chase_timer = 10.0
                self.patrol_speed = 300

        if self.chase_timer > 0:
            dx = self.kirby_pos[0] - self.position[0]
            dy = self.kirby_pos[1] - self.position[1]
            dist = math.hypot(dx, dy)
            if dist != 0:
                speed = self.patrol_speed + 50
                self.velocity[0] = (dx / dist) * speed
                self.velocity[1] = (dy / dist) * speed
            else:
                self.velocity = vec(0, 0)
            self.LR.update(seconds)
            self.UD.update(seconds)
            super().update(seconds)
        else:
            self.patrol_speed = 100
            if self.patrol_axis == "stationary":
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.LR.update(seconds)
                self.UD.update(seconds)
                super().update(seconds)
                # Turn after timer
                self.turn_timer -= seconds
                if self.turn_timer <= 0:
                    self.direction *= -1
                    self.turn_timer = self.turn_interval
            elif self.patrol_axis == "horizontal":
                self.velocity[0] = self.direction * self.patrol_speed
                self.velocity[1] = 0
                self.LR.update(seconds)
                self.UD.update(seconds)
                super().update(seconds)

                if self.velocity[0] > 0:
                    self.direction = 1
                elif self.velocity[0] < 0:
                    self.direction = -1
       
                if self.chase_timer <= 0 and self.velocity[0] == 0:
                    self.direction *= -1
            elif self.patrol_axis == "vertical":
                self.velocity[0] = 0
                self.velocity[1] = self.direction * self.patrol_speed
                self.LR.update(seconds)
                self.UD.update(seconds)
                super().update(seconds)
                if self.velocity[1] > 0:
                    self.direction = 1
                elif self.velocity[1] < 0:
                    self.direction = -1
                if self.chase_timer <= 0 and self.velocity[1] == 0:
                    self.direction *= -1

    def has_line_of_sight(self):
        if self.kirby_pos is None:
            return False
        x0, y0 = self.position[0] + 15, self.position[1] + 15
        x1, y1 = self.kirby_pos[0] + 15, self.kirby_pos[1] + 15
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) // 5)
        for i in range(1, steps):
            x = x0 + (x1 - x0) * i / steps
            y = y0 + (y1 - y0) * i / steps
            if self.check_solid and self.check_solid(x, y):
                return False
        return True
        
    def draw_vision_cone(self, surface):
        cone_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        if self.velocity[0] != 0 or self.velocity[1] != 0:
            start_angle = math.atan2(self.velocity[1], self.velocity[0])
        else:
            if self.patrol_axis == "horizontal":
                start_angle = 0 if self.direction == 1 else math.pi
            elif self.patrol_axis == "vertical" or self.patrol_axis == "stationary":
                start_angle = math.pi / 2 if self.direction == 1 else -math.pi / 2
            else:
                start_angle = 0 if self.direction == 1 else math.pi

        num_rays = 30
        points = [(
            int(self.position[0] + 15),
            int(self.position[1] + 15)
        )]
        for i in range(num_rays + 1):
            offset = -self.vision_angle / 2 + (self.vision_angle * i / num_rays)
            angle = start_angle + offset
            end_x = self.position[0] + math.cos(angle) * 0
            end_y = self.position[1] + math.sin(angle) * 0
            for d in range(0, int(self.vision_distance), 5):
                x = self.position[0] + math.cos(angle) * d
                y = self.position[1] + math.sin(angle) * d
                if self.check_solid is not None and self.check_solid(x, y):
                    break
                end_x, end_y = x, y
            points.append((int(end_x), int(end_y)))
        pygame.draw.polygon(cone_surface, (255, 0, 255, 80), points, 0)
        surface.blit(cone_surface, (0, 0))
        self.cone = cone_surface