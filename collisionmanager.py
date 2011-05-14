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
        
    def addCollider(self, physicalNode):
        """
        Adds a node to the collision system.
        The parameter 'physicalNode' must be an instance of 
        PhysicalNode.
        """
        
        self.handler.addCollider(physicalNode.collider, physicalNode.actor)
        self.traverser.addCollider(physicalNode.collider, self.handler)
