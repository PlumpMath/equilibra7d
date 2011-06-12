from panda3d.core import Vec3

from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler
from physicalnode import PhysicalNode


class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(1.6)
        
        self._impulseIncrement = 1.5
        self._speedLimit = 2.0
        self._impact = 10
        
        self.keys = dict.fromkeys("left right up down".split(), 0)
        self.bindings = (
            ("w", self.handleKeyboardEvent, ["up", 1]),
            ("a", self.handleKeyboardEvent, ["left", 1]),
            ("s", self.handleKeyboardEvent, ["down", 1]),
            ("d", self.handleKeyboardEvent, ["right", 1]),

            ("w-up", self.handleKeyboardEvent, ["up", 0]),
            ("a-up", self.handleKeyboardEvent, ["left", 0]),
            ("s-up", self.handleKeyboardEvent, ["down", 0]),
            ("d-up", self.handleKeyboardEvent, ["right", 0]),
            
            ("arrow_up", self.handleKeyboardEvent, ["up", 1]),
            ("arrow_left", self.handleKeyboardEvent, ["left", 1]),
            ("arrow_down", self.handleKeyboardEvent, ["down", 1]),
            ("arrow_right", self.handleKeyboardEvent, ["right", 1]),

            ("arrow_up-up", self.handleKeyboardEvent, ["up", 0]),
            ("arrow_left-up", self.handleKeyboardEvent, ["left", 0]),
            ("arrow_down-up", self.handleKeyboardEvent, ["down", 0]),
            ("arrow_right-up", self.handleKeyboardEvent, ["right", 0]),
            
            # These are fired when the user keeps pressing a key
            ("w-repeat", self.handleKeyboardEvent, ["up", 1]),
            ("a-repeat", self.handleKeyboardEvent, ["left", 1]),
            ("s-repeat", self.handleKeyboardEvent, ["down", 1]),
            ("d-repeat", self.handleKeyboardEvent, ["right", 1]),
            ("arrow_up-repeat", self.handleKeyboardEvent, ["up", 1]),
            ("arrow_left-repeat", self.handleKeyboardEvent, ["left", 1]),
            ("arrow_down-repeat", self.handleKeyboardEvent, ["down", 1]),
            ("arrow_right-repeat", self.handleKeyboardEvent, ["right", 1]),
        )
    
    def setup(self):
        self.setZ(5)
        self.setScale(0.8)
    
    def handleCollisionEvent(self, entry, type):
        point = entry.getSurfacePoint(self)
        normal = entry.getSurfaceNormal(self)
        self.addImpact(point, normal * self._impact)
    
    def handleKeyboardEvent(self, key, value):
        keys = self.keys
        keys[key] = value
        
        dt = 0.05
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
    
    def is_braking(self, coordinate):
        velocity = self.getVelocity()
        return velocity.dot(coordinate) < 0
    
    @property
    def is_above_limit(self):
        speed = self.getVelocity().length()
        return speed > self._speedLimit

