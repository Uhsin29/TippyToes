import pygame

from gameObjects import kirby
from .guard import Guard
from . import Drawable, Kirby

from utils import vec, RESOLUTION

class GameEngine(object):
        def load_level(self, level_data):
            """
            Reset all game objects and state for a new level.
            """
            self.current_level = level_data

            # Different guards for each level
            if level_data is self.level1:
                self.kirby = Kirby((50,600), self.check_solid)
                self.kirby.red_key = False
                self.kirby.blue_key = False
                self.kirby.yellow_key = False
                self.background = Drawable((0,0), "background2.jpg")
                self.red_key = Drawable((325,625), "red_key.png", (0,0))
                self.blue_key = Drawable((1100,500), "blue_key.png", (0,0))
                self.yellow_key = Drawable((1000,50), "yellow_key.png", (0,0))
                self.guard = Guard((925,625), self.check_solid, patrol_axis="vertical")
                self.guard1 = Guard((35, 35), self.check_solid, patrol_axis="vertical")
                self.guard2 = Guard((500,100), self.check_solid, patrol_axis="horizontal")
                self.guards = [self.guard, self.guard1, self.guard2]
            elif level_data is self.level2:
                self.kirby = Kirby((50,650), self.check_solid)
                self.kirby.red_key = False
                self.kirby.blue_key = False
                self.kirby.yellow_key = False

                # New key positions
                self.background = Drawable((0,0), "background2.jpg")
                self.red_key = Drawable((725,625), "red_key.png", (0,0))
                self.blue_key = Drawable((1000,50), "blue_key.png", (0,0))
                self.yellow_key = Drawable((100,50), "yellow_key.png", (0,0))

                # New guard positions
                self.guard = Guard((100,220), self.check_solid, patrol_axis="horizontal")
                self.guard1 = Guard((1110,200), self.check_solid, patrol_axis="vertical")
                self.guard2 = Guard((1015,515), self.check_solid, patrol_axis="horizontal")
                self.guard3 = Guard((460,70), self.check_solid, patrol_axis="stationary", turn_timer=3.0, facing="down")
                self.guard4 = Guard((567,650), self.check_solid, patrol_axis="stationary", turn_timer=3.0, facing="up")
                self.guards = [self.guard, self.guard1, self.guard2, self.guard3, self.guard4]

        def __init__(self):
            # Grid of 40 x 25       
            self.level1 = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 4, 4, 1],
                [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            self.level2 = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 1, 1, 4, 4, 4, 1, 1, 1, 4, 4, 4, 1, 1, 1, 0, 0, 0, 1, 1, 1, 4, 4, 4, 1, 1, 1, 4, 4, 4, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
            self.tile_size = 30
            self.size = vec(*RESOLUTION)
            self.current_level = self.level1
            self.load_level(self.current_level)
        
        def draw(self, drawSurface):        
            self.background.draw(drawSurface)
            for y, row in enumerate(self.current_level):
                for x, tile in enumerate(row):
                    if tile == 1:
                        wall = Drawable((x*self.tile_size,y*self.tile_size), "wall.png")
                        wall.draw(drawSurface)

                    if tile == 2 and self.kirby.red_key == True:
                        pygame.draw.rect(drawSurface, (0, 255, 0), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    elif tile == 2:
                        pygame.draw.rect(drawSurface, (255, 0, 0), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

                    if tile == 3 and self.kirby.blue_key == True:
                                        pygame.draw.rect(drawSurface, (0, 255, 0), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    elif tile == 3:
                        pygame.draw.rect(drawSurface, (0, 0, 255), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    
                    if tile == 4 and self.kirby.yellow_key == True:
                        pygame.draw.rect(drawSurface, (0, 255, 0), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    elif tile == 4:
                        pygame.draw.rect(drawSurface, (255, 255, 0), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

                    if tile == 5:
                        pygame.draw.rect(drawSurface, (255, 0, 255), pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    
            for guard in self.guards:
                guard.draw(drawSurface)
                guard.draw_vision_cone(drawSurface)
            self.kirby.draw(drawSurface)
            if self.kirby.red_key == False:
                self.red_key.draw(drawSurface)
            if self.kirby.blue_key == False:
                self.blue_key.draw(drawSurface)
            if self.kirby.yellow_key == False:
                self.yellow_key.draw(drawSurface)

        def check_solid(self, px, py):
            tile_x = int(px // self.tile_size)
            tile_y = int(py // self.tile_size)
            if 0 <= tile_y < len(self.current_level) and 0 <= tile_x < len(self.current_level[0]):
                tile = self.current_level[tile_y][tile_x]
                if tile == 1:
                    return True
                if tile == 2 and not self.kirby.red_key:
                    return True
                if tile == 3 and not self.kirby.blue_key:
                    return True
                if tile == 4 and not self.kirby.yellow_key:
                    return True
                return False
            return False
        
        def handleEvent(self, event):
            self.kirby.handleEvent(event)
        
        def update(self, seconds):
            self.kirby.update(seconds)
            for guard in self.guards:
                guard.kirby_pos = self.kirby.position
                guard.update(seconds)
            kirby_rect = pygame.Rect(self.kirby.position[0], self.kirby.position[1], 16, 16)
            for guard in self.guards:
                guard_rect = pygame.Rect(guard.position[0], guard.position[1], 16, 16)
                if kirby_rect.colliderect(guard_rect):
                    if hasattr(self, 'screenManager') and self.screenManager is not None:
                        self.screenManager.state.die()
                    break
            Drawable.updateOffset(self.kirby, self.size)
            kirby_rect = pygame.Rect(self.kirby.position[0], self.kirby.position[1], 16, 16)
            red_key_rect = pygame.Rect(self.red_key.position[0], self.red_key.position[1], 16, 16)
            blue_key_rect = pygame.Rect(self.blue_key.position[0], self.blue_key.position[1], 16, 16)
            yellow_key_rect = pygame.Rect(self.yellow_key.position[0], self.yellow_key.position[1], 16, 16)
            if kirby_rect.colliderect(red_key_rect):
                self.kirby.red_key = True
            if kirby_rect.colliderect(blue_key_rect):
                self.kirby.blue_key = True
            if kirby_rect.colliderect(yellow_key_rect):
                self.kirby.yellow_key = True

            
            tile_x = int(self.kirby.position[0] // self.tile_size)
            tile_y = int(self.kirby.position[1] // self.tile_size)
            if 0 <= tile_y < len(self.current_level) and 0 <= tile_x < len(self.current_level[0]):
                tile = self.current_level[tile_y][tile_x]
                if tile == 5 and self.current_level is self.level1:
                    self.load_level(self.level2)
                elif tile == 5 and self.current_level is self.level2:
                    self.load_level(self.level1)