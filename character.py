from panda3d.core import NodePath
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import BitMask32
from panda3d.physics import ActorNode

class Character(NodePath):
    def __init__(self, parent, model="character"):
        NodePath.__init__(self, "character")
        
        actorNode = ActorNode("characterActorNode")
        self.actor = self.attachNewNode(actorNode)
        
        self.model = loader.loadModel("models/" + model)
        self.model.reparentTo(self.actor)                
        self.model.setCollideMask(BitMask32.allOff())
        
        collisionSphere = CollisionSphere(0, 0, 0, 0.5)
        collisionNode = CollisionNode('characterCollisionNode')
        collisionNode.addSolid(collisionSphere)        
        self.collider = self.actor.attachNewNode(collisionNode)
        
        self.reparentTo(parent)