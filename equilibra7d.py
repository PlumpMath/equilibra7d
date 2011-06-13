#!/usr/bin/env ppython
import sys

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, WindowProperties

from objects import Character, Enemy, Landscape, Scenario, Sea
from managers import (AIManager, CollisionManager, HUDManager, KeyboardManager,
                      LightManager, PhysicsManager)
from gamestate import GameState


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.runonce()
        
        # Instantiate objects
        self.scenario = Scenario(self.render, "arena2")
        if len(sys.argv) == 2:
            model = sys.argv[1]
        else:
            model = "character_1_4"
        self.character = Character(self.render, model)
        self.enemy = Enemy(self.render, "enemy")
        self.landscape = Landscape(self.render, "landscape")
        self.sea = Sea(self.render, "sea")
        
        # Instantiate managers
        self.keyboardManager = KeyboardManager()
        self.physicsManager = PhysicsManager()
        self.collisionManager = CollisionManager()
        self.lightManager = LightManager()
        self.hudManager = HUDManager()
        self.aiManager = AIManager()
        
        # Set up state engine
        self.gameState = GameState()
        self.gameState.request("NewGame")
    
    def runonce(self):
        # Set window title
        props = WindowProperties()
        props.setTitle("Equilibra7D")
        self.win.requestProperties(props)
        
        # Set up the camera
        self.camera.setY(-40)
        self.camera.setZ(15)
        self.camera.lookAt(0, 0, 0)
        self.disableMouse()
        
        # Enable per-pixel lighting
        self.render.setShaderAuto()
        
        # Enable FPS meter
        self.setFrameRateMeter(True)
        
        # Fix frame rate
        FPS = 60
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(FPS)
        
    def reset(self):
        self.gameState.reset()


if __name__ == "__main__":
    world = World()
    world.run()

