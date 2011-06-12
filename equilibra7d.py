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
from managers.gamestate import GameStateManager
from managers.hud import HUDManager
from managers.keyboard import KeyboardManager
from managers.light import LightManager
from managers.physics import PhysicsManager


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)

        # Set window title
        props = WindowProperties()
        props.setTitle("Equilibra7D")
        self.win.requestProperties(props)
        
        # Enable FPS meter (development-only)
        self.setFrameRateMeter(True)
        
        self.initFeatures()
        
        # Set up the Input Manager
        self.keyboardManager = KeyboardManager()
        self.keyboardManager.addKeyboardEventHandler(self.character)
        
        
        # Set up the Physics Manager
        self.physicsManager = PhysicsManager()
        self.physicsManager.addLinearForce(0, 0, -10)
        #self.physicsManager.addActor(self.scenario)
        self.physicsManager.addActor(self.character)
        self.physicsManager.addActor(self.enemy)
        
        # Add buoyancy
        self.physicsManager.addLinearForce(0, 0, 10, self.scenario)
        
        ## Set up the Collision Manager
        self.collisionManager = CollisionManager()
        self.collisionManager.addCollider(self.character)
        self.collisionManager.addCollider(self.enemy)
        self.collisionManager.addCollisionHandling(self.enemy.collider,
                                                   "into",
                                                   self.character,
                                                   self.enemy)
        self.collisionManager.addCollisionHandling(self.scenario.collider,
                                                   "into",
                                                   self.scenario)
        self.collisionManager.addCollisionHandling(self.scenario.collider,
                                                   "again",
                                                   self.scenario)
        self.collisionManager.addCollisionHandling(self.scenario.collider,
                                                   "out",
                                                   self.scenario)
        
        ## Set up the Light Manager
        self.lightManager = LightManager()
        
        ## Set up the HUD Manager
        self.hudManager = HUDManager()
        
        # Set up the camera
        self.camera.setY(-40)
        self.camera.setZ(15)
        self.camera.lookAt(0, 0, 0)
        self.disableMouse()
        
        # Enable per-pixel lighting
        self.render.setShaderAuto()

        # Fix frame rate
        FPS = 60
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(FPS)
        
        # Enable gameover task
        self.gameStateManager = GameStateManager()
        self.gameStateManager.request("NewGame")
        
        # Enable AI
        self.aiManager = AIManager()
        
    def initFeatures(self):
        """Instantiate things in the world"""
        # Place the scenario in the world
        self.scenario = Scenario(self.render, "arena1")
        self.scenario.setZ(0.2)
        
        # Place the character in the world
        if len(sys.argv) == 2:
            model = sys.argv[1]
        else:
            model = "character_1_4"
        self.character = Character(self.render, model)
        self.character.setZ(5)
        self.character.setScale(0.8)

        # Place the enemy in the world
        self.enemy = Enemy(self.render, "enemy")
        self.enemy.setPos(1, 4, 5)
        
        # Place the landscape (skybox)
        self.landscape = Landscape(self.render, "landscape")
        self.landscape.setScale(20)
        
        # Place the sea
        self.sea = Sea(self.render, "sea")
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
        self.gameStateManager.reset()


if __name__ == "__main__":
    world = World()
    world.run()

