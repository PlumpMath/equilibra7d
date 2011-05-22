from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import WindowProperties

from scenario import Scenario
from character import Character
from enemy import Enemy
from landscape import Landscape
from sea import Sea
from inputmanager import InputManager
from physicsmanager import PhysicsManager
from collisionmanager import CollisionManager
from lightingmanager import LightingManager
from hudmanager import HUDManager


class World(ShowBase):
    """Class that holds the Panda3D Scene Graph."""
    
    def __init__(self):
        ShowBase.__init__(self)

        props = WindowProperties()
        props.setTitle("Equilibra7D")
        self.win.requestProperties(props)
        
        # Placing the scenario in the world.
        self.scenario = Scenario(self.render, "arena1")
        self.scenario.setZ(0.2)
        
        # Placing the character in the world.
        self.character = Character(self.render, "ball")
        self.character.setZ(5)
        self.character.setScale(1.5)

        # Placing an enemy in the world.
        self.enemy = Enemy(self.render, "enemy")
        self.enemy.setPos(1, 4, 5)
        
        # Placing the landscape (skybox)
        self.landscape = Landscape(self.render, "landscape")
        self.landscape.setScale(20)
        
        # Placing the Sea
        self.sea = Sea(self.render, "sea")
        self.sea.setScale(20)
        
        ## Setting up the Input Manager
        self.inputManager = InputManager(self)
        self.inputManager.addKeyboardEventHandler(self.character)
        
        ## Setting up the Physics Manager
        self.physicsManager = PhysicsManager(self)
        self.physicsManager.addLinearForce(0, 0, -1)
        self.physicsManager.addActor(self.scenario)
        self.physicsManager.addActor(self.character)
        self.physicsManager.addActor(self.enemy)
        
        # Adding buoyancy
        self.physicsManager.addLinearForce(0, 0, 1, self.scenario)
        
        ## Setting up the Collision Manager        
        self.collisionManager = CollisionManager(self)
        self.collisionManager.addCollider(self.character)
        self.collisionManager.addCollider(self.enemy)
        self.collisionManager.addCollisionHandling(self.enemy.collider,
                                                   "into",
                                                   self.character,
                                                   self.enemy)
        self.collisionManager.addCollisionHandling(self.scenario.collider,
                                                   "again",
                                                   self.scenario)
        
        ## Setting up the Lighting Manager
        self.lightingManager = LightingManager(self)
        self.lightingManager.setAmbientLight(0.3, 0.3, 0.3)
        self.lightingManager.setPointLight(1, 1, 1, 0, -8, 5)
        
        ## Setting up the HUD Manager
        self.hudManager = HUDManager()
        
        # Setting up the camera
        self.camera.setY(-40)
        self.camera.setZ(15)
        self.camera.lookAt(0, 0, 0)
        self.disableMouse()
        
        # Enabling per-pixel lighting
        self.render.setShaderAuto()


if __name__ == "__main__":
    world = World()
    world.run()
