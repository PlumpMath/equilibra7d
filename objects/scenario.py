from panda3d.core import BitMask32

from handlers.collision import CollisionEventHandler
from physicalnode import PhysicalNode


class Scenario(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "scenario")
        
        self.addCollisionGeometry(model)
        
        self._forces = {}
        self._angularVelocity = 0.01
    
    def setup(self):
        self.setZ(0.2)
    
    def handleCollisionEvent(self, entry, type):
        if type == "into":
            self._addTorque(entry)
        elif type == "again":
            self._removeTorque(entry)
            self._addTorque(entry)
        elif type == "out":
            self._removeTorque(entry)
    
    def _addTorque(self, entry):
        fromNode = entry.getFromNodePath().getName()
        contactPoint = entry.getSurfacePoint(self)
        
        pitch = -contactPoint.getY() * self._angularVelocity
        roll = contactPoint.getX() * self._angularVelocity
        
        torque = self.addTorque(0, pitch, roll)
        self._forces[fromNode] = torque
    
    def _removeTorque(self, entry):
        fromNode = entry.getFromNodePath().getName()
        torque = self._forces.get(fromNode)
        if torque is not None:
            self.removeTorque(torque)
            del self._forces[fromNode]

