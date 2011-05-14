from direct.showbase.ShowBase import ShowBase

from scenario import Scenario
from character import Character
from enemy import Enemy
from physicsmanager import PhysicsManager
from collisionmanager import CollisionManager
from lightingmanager import LightingManager

class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scenario = Scenario(self.render, "arena1")
        
        self.character = Character(self.render, "ball")
        self.character.setZ(5)

        self.enemy = Enemy(self.render, "enemy")
        self.enemy.setPos(4, 4, 5)
        
        self.physicsManager = PhysicsManager(self)
        self.physicsManager.addLinearForce(0, 0, -1)
        self.physicsManager.addActor(self.character)
        self.physicsManager.addActor(self.enemy)
        
        self.collisionManager = CollisionManager(self, True)
        self.collisionManager.addCollider(self.character)
        self.collisionManager.addCollider(self.enemy)
        
        self.lightingManager = LightingManager(self)
        self.lightingManager.setAmbientLight(0.2, 0.2, 0.2)
        self.lightingManager.setPointLight(1, 1, 1, 0, -8, 5)
        
        self.camera.setY(-20)
        self.camera.setZ(4)
        self.camera.lookAt(0, 0, 0)
        self.disableMouse()

world = World()
world.run()
