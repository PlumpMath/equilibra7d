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
        self.handler.setStaticFrictionCoef(0.25)
        self.handler.setDynamicFrictionCoef(0.15)
        self.handler.addInPattern('into-%in')
        
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
    
    def addCollisionHandling(self, intoNode, *handlers):
        """
        Notifies that a collision event must be handled.
        The given handlers must inherit from the CollisionEventHandler 
        class. Its 'handleCollisionEvent' method will be called whenever
        a collision with the node given by 'intoNode' occurs.
        """
        
        pattern = "into-%s" % intoNode.getName()
        self.world.accept(pattern, self._callHandlers, [handlers])
        
    def _callHandlers(self, handlers, entry):
        for handler in handlers:
            handler.handleCollisionEvent(entry)
