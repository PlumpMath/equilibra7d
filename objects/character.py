from panda3d.core import Vec3

from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler
from physicalnode import PhysicalNode


class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(1.15)
        
        self._impulseIncrement = 2.0
        self._speedLimit = 3.0
        self._impact = 3
        
        self.keys = dict.fromkeys("left right up down".split(), 0)
        self.bindings = (
            ("w", self.setKey, ["up", 1]),
            ("a", self.setKey, ["left", 1]),
            ("s", self.setKey, ["down", 1]),
            ("d", self.setKey, ["right", 1]),
            
            ("w-up", self.setKey, ["up", 0]),
            ("a-up", self.setKey, ["left", 0]),
            ("s-up", self.setKey, ["down", 0]),
            ("d-up", self.setKey, ["right", 0]),
            
            ("arrow_up", self.setKey, ["up", 1]),
            ("arrow_left", self.setKey, ["left", 1]),
            ("arrow_down", self.setKey, ["down", 1]),
            ("arrow_right", self.setKey, ["right", 1]),
            
            ("arrow_up-up", self.setKey, ["up", 0]),
            ("arrow_left-up", self.setKey, ["left", 0]),
            ("arrow_down-up", self.setKey, ["down", 0]),
            ("arrow_right-up", self.setKey, ["right", 0]),
            
            # These are fired when the user keeps pressing a key
            #("w-repeat", self.handleKeyboardEvent, ["up", 1]),
            #("a-repeat", self.handleKeyboardEvent, ["left", 1]),
            #("s-repeat", self.handleKeyboardEvent, ["down", 1]),
            #("d-repeat", self.handleKeyboardEvent, ["right", 1]),
            #("arrow_up-repeat", self.handleKeyboardEvent, ["up", 1]),
            #("arrow_left-repeat", self.handleKeyboardEvent, ["left", 1]),
            #("arrow_down-repeat", self.handleKeyboardEvent, ["down", 1]),
            #("arrow_right-repeat", self.handleKeyboardEvent, ["right", 1]),
        )
        
        taskMgr.add(self.handleKeyboardEvent, "character_move_task")
    
    def setup(self):
        self.setZ(5)
        self.setScale(0.8)
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        self.addImpulse(normal * self._impact)
    
    def handleKeyboardEvent(self, task):
        keys = self.keys
        
        dt = globalClock.getDt()
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
        
        # Looks like a hack...
        # Face the symmetric of the velocity works but.. is the model with
        # its eyes in the back?!
        self.face(-self.getVelocity())
        
        return task.cont
    
    def setKey(self, key, value):
        self.keys[key] = value
    
    def is_braking(self, coordinate):
        velocity = self.getVelocity()
        return velocity.dot(coordinate) < 0
    
    @property
    def is_above_limit(self):
        speed = self.getVelocity().length()
        return speed > self._speedLimit
    
    def face(self, direction):
        """Makes the character look at a given the direction.
        
        `direction': vector
        """
        # It seems that headsUp works better than lookAt.
        self.model.headsUp(direction.x, direction.y, direction.z)
        #self.model.lookAt(direction.x, direction.y, direction.z)

