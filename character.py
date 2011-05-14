from physicalnode import PhysicalNode

class Character(PhysicalNode):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(0.5)
