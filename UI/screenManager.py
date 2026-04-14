from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from gameObjects import GameEngine
from utils.vector import vec
from utils.constants import RESOLUTION

from pygame.locals import *

class ScreenManager(object):
      
    def __init__(self):
        self.game = GameEngine()
        self.game.screenManager = self
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),
                                    "Paused")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size // 2
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("main_menu2.jpg", 
                      fontName="default8")
        self.mainMenu.addOption("start", 
                    "Start Game (s)",
                     RESOLUTION // 2 - vec(0,50),
                     lambda x: x.type == KEYDOWN and x.key == K_s,
                     center="both")
        self.mainMenu.addOption("exit", 
                    "Exit Game (e)",
                     RESOLUTION // 2 + vec(0,50),
                     lambda x: x.type == KEYDOWN and x.key == K_e,
                     center="both")

        # Death screen menu
        self.deathMenu = EventMenu("main_menu2.jpg", fontName="default8")
        self.deathMenu.addOption("restart",
                     "Restart (r)",
                     RESOLUTION // 2 - vec(0, 50),
                     lambda x: x.type == KEYDOWN and x.key == K_r,
                     center="both")
        self.deathMenu.addOption("quit",
                     "Quit to Menu (q)",
                     RESOLUTION // 2 + vec(0, 50),
                     lambda x: x.type == KEYDOWN and x.key == K_q,
                     center="both")
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        elif self.state == "deathScreen":
            self.deathMenu.draw(drawSurf)
    
    def handleEvent(self, event):
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.game.handleEvent(event)

        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
        elif self.state == "deathScreen":
            choice = self.deathMenu.handleEvent(event)
            if choice == "restart":
                self.game.load_level(self.game.current_level)
                self.state.restart()
            elif choice == "quit":
                self.game.load_level(self.game.level1)
                self.state.quitToMenu()
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
        elif self.state == "deathScreen":
            self.deathMenu.update(seconds)
    