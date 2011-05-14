from physicalnode import PhysicalNode

class Enemy(PhysicalNode):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "enemy")
        
        self.addCollisionSphere(1.3)
