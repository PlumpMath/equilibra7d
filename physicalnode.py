from panda3d.core import BitMask32
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.physics import ActorNode

from modelnode import ModelNode

class PhysicalNode(ModelNode):
    """
    A wrapper class to a Panda3D node that has a model and will be
    controlled by the physical simulation.
    
    Structure:
        PandaNode -> ActorNode -> ModelNode
                               -> CollisionNode (optional)
    """
    
    def __init__(self, parent, model, name):
        ModelNode.__init__(self, parent, model, name)
        
        actorNode = ActorNode(name + "_actor_node")
        self.actor = self.attachNewNode(actorNode)
        
        self.model.setCollideMask(BitMask32.allOff())
        self.model.reparentTo(self.actor)

    def addCollisionSphere(self, size):
        collisionSphere = CollisionSphere(0, 0, 0, size)
        collisionNode = CollisionNode(self.name + '_collision_node')
        collisionNode.addSolid(collisionSphere)

        self.collider = self.actor.attachNewNode(collisionNode)
