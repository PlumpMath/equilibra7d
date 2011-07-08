#!/usr/bin/env ppython
# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, WindowProperties
from panda3d.core import NodePath

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

