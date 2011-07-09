#!/usr/bin/env ppython
# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, WindowProperties

from gamestate import GameState


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.configWorld()
        
        # Set up state engine
        self.gameState = GameState()
        
        # Go to main menu
        self.reset()
    
    def configWorld(self):
        """Set general settings.
        
        Probably run only once."""
        # Set window title
        props = WindowProperties()
        props.setTitle("Equilibra7d")
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
    
    def start(self):
        self.gameState.start()


if __name__ == "__main__":
    world = World()
    world.run()

