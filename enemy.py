from panda3d.core import NodePath
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import BitMask32
from panda3d.physics import ActorNode

class Enemy(NodePath):
    def __init__(self, parent, model):
        NodePath.__init__(self, "enemy")
        
        actorNode = ActorNode("enemy_actor_node")
        self.actor = self.attachNewNode(actorNode)
        
        self.model = loader.loadModel("models/" + model)
        self.model.reparentTo(self.actor)                
        self.model.setCollideMask(BitMask32.allOff())
        
        collisionSphere = CollisionSphere(0, 0, 0, 1.3)
        collisionNode = CollisionNode('enemy_collision_node')
        collisionNode.addSolid(collisionSphere)

        self.collider = self.actor.attachNewNode(collisionNode)
        
        self.reparentTo(parent)
