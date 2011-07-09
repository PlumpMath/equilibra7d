from panda3d.core import CollisionTraverser
from panda3d.physics import PhysicsCollisionHandler

from base import Manager


class CollisionManager(Manager):
    """Handles the collision between objects on the scene."""
    
    def __init__(self, debug=False):
        self.debug = debug
        
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True)
        
        if self.debug:
            base.cTrav.showCollisions(render)
        
        self.handler = PhysicsCollisionHandler()
        self.handler.setStaticFrictionCoef(0.1)
        self.handler.setDynamicFrictionCoef(0.05)
        self.handler.addInPattern('into-%in')
        self.handler.addAgainPattern('again-%in')
        self.handler.addOutPattern('out-%in')
        self.handler.addInPattern('%fn-into-%in')
    
    def setup(self):
        self.addCollider(base.gameState.currentState.objects['character'])
    
    def clear(self):
        base.cTrav.clearColliders()
    
    def addCollider(self, physicalNode):
        """Adds a node to the collision system.
        
        The parameter 'physicalNode' must be an instance of PhysicalNode.
        """
        self.handler.addCollider(physicalNode.collider, physicalNode.actor)
        base.cTrav.addCollider(physicalNode.collider, self.handler)
        
        if self.debug:
            physicalNode.collider.show()
    
    def addCollisionHandling(self, intoNode, type, *handlers):
        """Notifies that a collision event should be handled.
        
        The given 'type' should be "into", "again" or "out".
        The given handlers must inherit from the CollisionEventHandler 
        class. Its 'handleCollisionEvent' method will be called whenever
        a collision with the node given by 'intoNode' occurs.
        """
        pattern = "%s-%s" % (type, intoNode.getName())
        base.accept(pattern, self._callHandlers, [handlers, type])
        
    def addMutualCollisionHandling(self, fromNode, intoNode):
        """Notifies that a 'into' collision event between two specific 
        nodes should be handled by them.

        The given nodes must inherit from the CollisionEventHandler 
        class. Its 'handleCollisionEvent' method will be called whenever
        a collision with the node given by 'intoNode' occurs.
        """
        pattern = "%s-into-%s" % (fromNode.collider.getName(), 
                                  intoNode.collider.getName())
        
        handlers = [fromNode, intoNode]
        base.accept(pattern, self._callHandlers, [handlers, "into"])
        
    def _callHandlers(self, handlers, type, entry):
        for handler in handlers:
            handler.handleCollisionEvent(entry, type)

