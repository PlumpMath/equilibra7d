from panda3d.core import Vec3

from physicalnode import PhysicalNode
from collisioneventhandler import CollisionEventHandler
from keyboardeventhandler import KeyboardEventHandler

class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(0.5)
        
        self._impulseIncrement = 0.75
        self._speedLimit = 2.0
        self._impact = 10
        
    def handleCollisionEvent(self, entry, type):
        point = entry.getSurfacePoint(self)
        normal = entry.getSurfaceNormal(self)
        self.addImpact(point, normal * self._impact)
    
    def handleKeyboardEvent(self, keys, dt):
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
        
        self.addImpulse(impulse)
    
    def _isBraking(self, velocity, coordinate):
        return (velocity.cross(coordinate) < 0)
