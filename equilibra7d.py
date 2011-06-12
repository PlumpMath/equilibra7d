#!/usr/bin/env ppython
import sys

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, WindowProperties

from character import Character
from enemy import Enemy
from landscape import Landscape
from scenario import Scenario
from sea import Sea

from managers.ai import AIManager
from managers.collision import CollisionManager
from managers.hud import HUDManager
from managers.keyboard import KeyboardManager
from managers.light import LightManager
from managers.physics import PhysicsManager

from gamestate import GameState


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.runonce()
        
        # Instantiate objects
        self.scenario = Scenario(self.render, "arena1")
        if len(sys.argv) == 2:
            model = sys.argv[1]
        else:
            model = "character_1_4"
        self.character = Character(self.render, model)
        self.enemy = Enemy(self.render, "enemy")
        self.landscape = Landscape(self.render, "landscape")
        self.sea = Sea(self.render, "sea")
        
        self.initFeatures()
        
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
    
    def initFeatures(self):
        """Instantiate things in the world"""
        # Place the scenario in the world
        self.scenario.setZ(0.2)
        
        # Place the character in the world
        self.character.setZ(5)
        self.character.setScale(0.8)

        # Place the enemy in the world
        self.enemy.setPos(1, 4, 5)
        
        # Place the landscape (skybox)
        self.landscape.setScale(20)
        
        # Place the sea
        self.sea.setScale(20)
    
    def _removeFeatures(self):
        """Cleanup the NodePath."""
        to_be_removed = (self.scenario, self.character, self.enemy,
                         self.landscape, self.sea,
                         # self.keyboardManager,
                         # self.physicsManager,
                         # self.collisionManager,
                         # self.lightManager,
                         # self.hudManager
                         )
        for node in to_be_removed:
            node.removeNode()
    
    def reset(self):
        self.gameState.reset()


if __name__ == "__main__":
    world = World()
    world.run()

