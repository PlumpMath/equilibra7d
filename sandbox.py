import sys

from panda3d.core import Vec4
from panda3d.core import VBase4
from panda3d.core import AmbientLight
from panda3d.core import PointLight
from panda3d.core import CollisionTraverser
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from panda3d.physics import PhysicsCollisionHandler

from direct.showbase.ShowBase import ShowBase

from scenario import Scenario
from character import Character
from cameramanager import CameraManager

class Sandbox(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.initInput()
        
        self.scenario = Scenario(self.render,
                                 "sandbox",
                                 self.taskMgr,
                                 self.keys)
        
        self.scenario.setH(-90)
        self.scenario.setPos(0, 23, -30)

        self.character = Character(self.render, "ball")
        
        self.cameraManager = CameraManager(self.cam,
                                           self.character.actor, 
                                           self.taskMgr)
        
        self.initPhysics()
        self.initCollision()
        self.initLights()
        
        #self.disableMouse()
    
    def initPhysics(self):
        self.enableParticles()
        
        globalForcesNode = ForceNode("global_forces")        
        gravity = LinearVectorForce(0, 0, -1)
        
        globalForcesNode.addForce(gravity)
        self.physicsMgr.addLinearForce(gravity)
        
        self.globalForces = self.render.attachNewNode(globalForcesNode)

        self.physicsMgr.attachPhysicalNode(self.character.actor.node())

    def initCollision(self):
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)
        self.cTrav.showCollisions(render)
        
        self.collisionHandler = PhysicsCollisionHandler()
        
        self.collisionHandler.addCollider(self.character.collider,
                                          self.character.actor)
        
        self.cTrav.addCollider(self.character.collider, self.collisionHandler)

        self.character.collider.show()
        
    def initLights(self):        
        ambientLightNode = AmbientLight('ambient_light')
        ambientLightNode.setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.ambientLight = self.render.attachNewNode(ambientLightNode)
        self.render.setLight(self.ambientLight)

        pointLightNode = PointLight('point_light')
        pointLightNode.setColor(VBase4(1, 1, 1, 1))

        self.pointLight = self.render.attachNewNode(pointLightNode)
        self.pointLight.setPos(0, -25, 8)
        self.render.setLight(self.pointLight)

    def initInput(self):
        self.keys = {"left":0, "right":0, "up":0, "down":0}
        
        self.accept("w", self.setKey, ["up", 1])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("s", self.setKey, ["down", 1])
        self.accept("d", self.setKey, ["right", 1])

        self.accept("w-up", self.setKey, ["up", 0])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("s-up", self.setKey, ["down", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        
        self.accept("escape", sys.exit)

    def setKey(self, key, value):
        self.keys[key] = value


sandbox = Sandbox()
sandbox.run()
