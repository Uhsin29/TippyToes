from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Kirby(Mobile):
   def __init__(self, position, check_solid=None):
      super().__init__(position, "orb.png")
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
      self.red_key = False
      self.blue_key = False
      self.yellow_key = False

   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.UD.decrease()
             
         elif event.key == K_DOWN:
            self.UD.increase()
            
         elif event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()
            
      elif event.type == KEYUP:
         if event.key == K_UP:
            self.UD.stop_decrease()
             
         elif event.key == K_DOWN:
            self.UD.stop_increase()
             
            
         elif event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.UD.update(seconds)
      
      super().update(seconds)


   def updateMovement(self):
      # For unpausing the game
      pressed = pygame.key.get_pressed()
      
      
      if not pressed[pygame.K_UP] and self.UD == "decrease":
         self.UD.stop_decrease()
      if not pressed[pygame.K_DOWN] and self.UD == "increase":
         self.UD.stop_increase()
         
      if not pressed[pygame.K_LEFT] and self.LR == "decrease":
         self.LR.stop_decrease()
      if not pressed[pygame.K_RIGHT] and self.LR == "increase":
         self.LR.stop_increase()
   
   
  