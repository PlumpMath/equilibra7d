#!/usr/bin/env ppython
# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, WindowProperties
from panda3d.core import NodePath

from objects import Character, Landscape, Scenario, Sea
import managers
from gamestate import GameState


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        # Create parent for all objects
        self.objectsNode = NodePath("objects")
        self.objectsNode.reparentTo(self.render)
        
        self.configWorld()
        
        # Set up state engine
        self.gameState = GameState()
        
        # Start new game
        self.gameState.request("MainMenu")
    
    def createObjects(self):
        """Instantiate objects.
        
        Can be run multiple times to recreate all objects."""
        # Remove nodes if they already exist.
        self.objectsNode.removeChildren()
        self.scenario = Scenario(self.objectsNode, "arena2")
        self.character = Character(self.objectsNode, "teste")
        self.landscape = Landscape(self.objectsNode, "landscape")
        self.sea = Sea(self.objectsNode, "sea")
    
    def createManagers(self):
        """Instantiate managers.
        
        Can be run multiple times to clear all managers."""
        for kind in "Keyboard Enemy Physics Collision Light HUD AI Audio".split():
            manager_attribute_name = "%sManager" % kind.lower()
            if hasattr(self, manager_attribute_name):
                manager = getattr(self, manager_attribute_name)
                # Clear the manager since it already exists
                manager.clear()
            else:
                # Take the *Manager class from the `managers' package
                class_name = "%sManager" % kind
                klass = getattr(managers, class_name)
                
                # Create new Manager. This is similar to
                # self.keyboardManager = managers.KeyboardManager()
                # done for each manager class.
                setattr(self, manager_attribute_name, klass())
    
    def configWorld(self):
        """Set general settings.
        
        Probably run only once."""
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
    
    def pause(self):
        self.gameState.pause()


if __name__ == "__main__":
    world = World()
    world.run()

