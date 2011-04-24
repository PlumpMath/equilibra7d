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

class Sandbox(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scenario = Scenario(self.render, "models/sandbox")
        self.scenario.setH(-90)

        self.character = Character(self.render, "models/ball")
        self.character.setPos(0, -23, 20)
        
        self.initPhysics()
        self.initCollision()
        self.initLights()
        
        self.accept("escape", sys.exit)
       
    def initPhysics(self):
        self.enableParticles()
        
        globalForcesNode = ForceNode("globalForces")        
        gravity = LinearVectorForce(0, 0, -9.81)
        
        globalForcesNode.addForce(gravity)
        self.physicsMgr.addLinearForce(gravity)
        
        self.globalForces = self.render.attachNewNode(globalForcesNode)

        self.physicsMgr.attachPhysicalNode(self.character.actor.node())

    def initCollision(self):
        self.cTrav = CollisionTraverser()
        self.cTrav.showCollisions(render)
        
        self.collisionHandler = PhysicsCollisionHandler()
        
        self.collisionHandler.addCollider(self.character.collider,
                                          self.character.actor)
        
        self.cTrav.addCollider(self.character.collider, self.collisionHandler)

        self.character.collider.show()
        
    def initLights(self):
                                          
        ambientLightNode = AmbientLight('ambientLight')
        ambientLightNode.setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        self.ambientLight = self.render.attachNewNode(ambientLightNode)
        self.render.setLight(self.ambientLight)

        pointLightNode = PointLight('pointLight')
        pointLightNode.setColor(VBase4(1, 1, 1, 1))

        self.pointLight = self.render.attachNewNode(pointLightNode)
        self.pointLight.setPos(0, -25, 8)
        self.render.setLight(self.pointLight)


sandbox = Sandbox()
sandbox.run()
