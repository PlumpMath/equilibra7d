from panda3d.core import Vec3, Point3

from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler
from physicalnode import PhysicalNode


class Character(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(1.15)
        
        self._impulseIncrement = 4.0
        self._speedLimit = 5.0
        self._impact = 4
        self._turningSpeed = 0.2

        self._hit = False
        self._currentDirection = Vec3.forward()
        self._currentAngle = 0
        
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
        
        task_name = "character_movement"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(self.handleKeyboardEvent, task_name)
    
    def setup(self):
        self.setZ(1)
        self.setScale(0.8)
        
        # Little "hack" to fix orientation
        # Seems that the model has its eyes in the back?!
        self.actor.setH(180)
        
    def handleCollisionEvent(self, entry, type):       
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        self.addImpulse(normal * self._impact)
        
        self.face(-normal)
        self._hit = True
    
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
        
        # If the character was not hit by an enemy look at the movement
        # direction.
        # Otherwise look at the enemy until the character turns around.
        if not self._hit:
            self.face(self.velocity)
            
        elif ((impulse.length() > 0) and
              (self.velocity.length() > 0.5) and
              (not self.is_braking(impulse))):
                    self._hit = False
        
        return task.cont
    
    def setKey(self, key, value):
        self.keys[key] = value
    
    def is_braking(self, coordinate):
        return self.velocity.dot(coordinate) < 0
    
    @property
    def is_above_limit(self):
        speed = self.velocity.length()
        return speed > self._speedLimit
    
    def face(self, direction):
        """Makes the character look at a given the direction.
        This method makes only heading rotations.
        
        `direction': vector
        """
        
        direction = Vec3(direction.x, direction.y, 0)
        
        if direction != Vec3.zero():
            direction.normalize()
            
            currentDirection = self._currentDirection
            
            headingAngle = direction.signedAngleDeg(currentDirection, 
                                                    Vec3.down())
            headingAngle += self._currentAngle
            
            if abs(headingAngle) > 1:
                interval = self.model.hprInterval(self._turningSpeed,
                                                  Point3(headingAngle, 0, 0))
                interval.start()
                
                self._currentDirection = direction
                self._currentAngle = headingAngle

