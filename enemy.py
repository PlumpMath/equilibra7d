from physicalnode import PhysicalNode
from collisioneventhandler import CollisionEventHandler

class Enemy(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "enemy")
        
        self.addCollisionSphere(1.25)
        
        self._impact = 10
    
    def handleCollisionEvent(self, entry, type):
        point = entry.getSurfacePoint(self)
        normal = entry.getSurfaceNormal(self)
        self.addImpact(point, normal * -self._impact)

