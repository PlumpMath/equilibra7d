from physicalnode import PhysicalNode
from handlers.collision import CollisionEventHandler


class Enemy(PhysicalNode, CollisionEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "enemy")
        
        self.mass = 20.0
        
        self.addCollisionSphere(1.25)
        self._impact = 2
    
    def setup(self):
        self.setPos(1, 4, 1)
        self.setScale(0.4)
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        self.addImpulse(normal * (-self._impact))

