from direct.showbase.ShowBase import ShowBase

from scenario import Scenario
from character import Character
from physicsmanager import PhysicsManager

class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scenario = Scenario(self.render, "arena1")
        
        self.character = Character(self.render, "ball")
        self.character.setZ(1)       

        self.physicsManager = PhysicsManager(self)
        self.physicsManager.addLinearForce(0, 0, -1)
        self.physicsManager.addActor(self.character.actor.node())
        
world = World()
world.run()
