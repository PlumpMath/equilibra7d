class CollisionEventHandler():
    """
    This class must be inherited by all classes interested in handling
    collision events.
    After being registered at a CollisionHandler, its handleCollisionEvent 
    method will be called whenever a relevent collision event occurs.
    This is an abstract class and should not be instantiated.
    """
    def handleCollisionEvent(self, entry):
        raise NotImplementedError