from panda3d.core import Vec3

from physicalnode import PhysicalNode
from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler

class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(0.5)
        
        self._impulseIncrement = 1.5
        self._speedLimit = 2.0
        self._impact = 10
        
    def handleCollisionEvent(self, entry, type):
        point = entry.getSurfacePoint(self)
        normal = entry.getSurfaceNormal(self)
        self.addImpact(point, normal * self._impact)
    
    def handleKeyboardEvent(self, keys, dt):
        impulse_old = self.handleKeyboardEvent_old(keys, dt)
        impulse_new = self.handleKeyboardEvent_new(keys, dt)
        assert impulse_old == impulse_new, "%s != %s" % (impulse_old, impulse_new)
        self.addImpulse(impulse_new)
    
    # Old implementation
    def handleKeyboardEvent_old(self, keys, dt):
        impulse = Vec3(0, 0, 0)
        increment = self._impulseIncrement * dt
        
        velocity = self.getVelocity()
        speed = velocity.length()
        
        above_limit = (speed > self._speedLimit)
        
        if keys["left"] != 0:
            if not above_limit or self._isBraking(velocity, Vec3.left()):
                impulse += Vec3.left() * increment
        
        if keys["right"] != 0:
            if not above_limit or self._isBraking(velocity, Vec3.right()):
                impulse += Vec3.right() * increment
        
        if keys["up"] != 0:
            if not above_limit or self._isBraking(velocity, Vec3.forward()):
                impulse += Vec3.forward() * increment
        
        if keys["down"] != 0:
            if not above_limit or self._isBraking(velocity, Vec3.back()):
                impulse += Vec3.back() * increment
        
        #self.addImpulse(impulse)
        return impulse
    
    def _isBraking(self, velocity, coordinate):
        return (velocity.dot(coordinate) < 0)

    # New implementation does the same as the old one, but with shorter code
    def handleKeyboardEvent_new(self, keys, dt):
        impulse = Vec3(0, 0, 0)
        increment = self._impulseIncrement * dt
        
        above_limit = self.is_above_limit
        
        for key, vec in (("left", Vec3.left()),
                         ("right", Vec3.right()),
                         ("up", Vec3.forward()),
                         ("down", Vec3.back())):
            if keys[key] and (not above_limit or self.is_braking(vec)):
                impulse += vec * increment
        
        return impulse
    
    def is_braking(self, coordinate):
        velocity = self.getVelocity()
        return velocity.dot(coordinate) < 0
        
    @property
    def is_above_limit(self):
        speed = self.getVelocity().length()
        return speed > self._speedLimit

