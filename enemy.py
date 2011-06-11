from physicalnode import PhysicalNode
from handlers.collision import CollisionEventHandler


class Enemy(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "enemy")
        
        self.addCollisionSphere(1.25)
        self._impact = 2
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        self.addImpulse(normal * -self._impact)

