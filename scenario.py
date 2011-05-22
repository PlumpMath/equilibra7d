from panda3d.core import BitMask32

from physicalnode import PhysicalNode
from collisioneventhandler import CollisionEventHandler

class Scenario(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "scenario")
        
        self.addCollisionGeometry(model)        
        
        self._forces = {}
        self._angularVelocity = 0.02
        
    def handleCollisionEvent(self, entry, type):
        fromNode = entry.getFromNodePath().getName()
        
        if type == "into":
            contactPoint = entry.getSurfacePoint(self)
            
            pitch = -contactPoint.getY() * self._angularVelocity
            roll = contactPoint.getX() * self._angularVelocity
            
            torque = self.addTorque(0, pitch, roll)
            self._forces[fromNode] = torque
        
        elif type == "out":
            torque = self._forces[fromNode]            
            self.removeTorque(torque)
            
            del self._forces[fromNode]
