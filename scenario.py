from panda3d.core import BitMask32

from physicalnode import PhysicalNode
from collisioneventhandler import CollisionEventHandler

class Scenario(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "scenario")
        
        self.addCollisionGeometry(model)        
        
    def handleCollisionEvent(self, entry):
        print entry
