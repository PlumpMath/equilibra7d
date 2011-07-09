from panda3d.core import Vec3, Point3

from handlers.collision import CollisionEventHandler
from handlers.keyboard import KeyboardEventHandler
from physicalnode import PhysicalNode


class Equismo(PhysicalNode, CollisionEventHandler, KeyboardEventHandler):
    ANIM_WALK = "anim1"
    
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "equismo", [self.ANIM_WALK])
        
        self.mass = 500.0
        
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
        )
        
        task_name = "equismo_movement"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(self.handleKeyboardEvent, task_name)
    
    def setup(self):
        self.setZ(1)
        self.setScale(0.8)
        
        # Little "hack" to fix orientation
        # Seems that the model has its eyes in the back?!
        self.actor.setH(180)
        self.actor.setZ(-1)
        
        self.load_bindings()
    
    def clear(self):
        print "\033[32m unload_bindings from equismo \033[0m"
        self.unload_bindings()
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        
        nodePath = entry.getIntoNodePath()
        enemyManager = base.gameState.currentState.objects['enemy']
        enemy = enemyManager.getNatanFromCollisionNode(nodePath)
        
        otherVelocity = enemy.velocity
        otherMass = enemy.mass
        self.collide(normal, otherVelocity, otherMass, 0.5)
        
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
        
        # If Equismo was not hit by an enemy look at the movement direction.
        # Otherwise look at the enemy until Equismo turns around.
        if not self._hit:
            self.face(self.velocity)
            
        elif ((impulse.length() > 0) and
              (self.velocity.length() > 0.5) and
              (not self.is_braking(impulse))):
                    self._hit = False

        self.doWalkAnimation(impulse)
        
        return task.cont
    
    def setKey(self, key, value):
        self.keys[key] = value
    
    def is_braking(self, coordinate):
        return self.velocity.dot(coordinate) < 0
    
    def doWalkAnimation(self, impulse):
        if impulse.length() > 0:
            if self.model.getCurrentAnim() is None:
                self.model.loop(self.ANIM_WALK)
        else:
            self.model.stop()
            self.model.pose(self.ANIM_WALK, 1)

    @property
    def is_above_limit(self):
        speed = self.velocity.length()
        return speed > self._speedLimit
    
    def face(self, direction):
        """Makes Equismo look at a given the direction.
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

