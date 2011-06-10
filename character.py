from panda3d.core import Vec3

from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler
from physicalnode import PhysicalNode


class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(1.6)
        
        self._impulseIncrement = 2.0
        self._speedLimit = 3.0
        self._impact = 10
        
    def handleCollisionEvent(self, entry, type):
        point = entry.getSurfacePoint(self)
        normal = entry.getSurfaceNormal(self)
        self.addImpact(point, normal * self._impact)
    
    def handleKeyboardEvent(self, keys, dt):
        impulse = Vec3(0, 0, 0)
        increment = self._impulseIncrement * dt
        
        above_limit = self.is_above_limit
        
        for key, vec in (("left", Vec3.left()),
                         ("right", Vec3.right()),
                         ("up", Vec3.forward()),
                         ("down", Vec3.back())):
            if keys[key] and (not above_limit or self.is_braking(vec)):
                impulse += vec * increment
        
        self.addImpulse(impulse)
        self.face(self.getVelocity())
    
    def is_braking(self, coordinate):
        velocity = self.getVelocity()
        return velocity.dot(coordinate) < 0
        
    @property
    def is_above_limit(self):
        speed = self.getVelocity().length()
        return speed > self._speedLimit

    def face(self, direction):
        """
        Makes the character look at the direction given by the given
        'direction' vector.
        """
        velocity = self.getVelocity()
        self.model.lookAt(velocity.x, velocity.y, 0)
