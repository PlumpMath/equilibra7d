from panda3d.core import CollisionTraverser
from panda3d.physics import PhysicsCollisionHandler

class CollisionManager():
    """Handles the collision between objects on the scene."""
    
    def __init__(self, world, debug=False):
        world.cTrav = CollisionTraverser()
        world.cTrav.setRespectPrevTransform(True)
        
        if debug:
            world.cTrav.showCollisions(render)
        
        self.handler = PhysicsCollisionHandler()
        
        self.world = world
        self.traverser = world.cTrav
        self.debug = debug
        
    def addCollider(self, node):
        """
        Adds a node to the collision system.
        The node must have a member 'collider', pointing to the 
        collision geometry, and a member 'actor', pointing to the 
        physics simulation's ActorNode.
        """
        
        self.handler.addCollider(node.collider, node.actor)
        self.traverser.addCollider(node.collider, self.handler)

        if self.debug:
            node.collider.show()
