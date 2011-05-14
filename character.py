from panda3d.core import Vec3

from physicalnode import PhysicalNode
from keyboardeventhandler import KeyboardEventHandler

class Character(PhysicalNode, KeyboardEventHandler):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "character")
        
        self.addCollisionSphere(0.5)
        
        self._speed = 3

    def handleKeyboardEvent(self, keys, dt):
        velocity = Vec3(0, 0, 0)
        movement = self._speed * dt
        
        if keys["left"] != 0:
            velocity += Vec3(-movement, 0, 0)

        if keys["right"] != 0:
            velocity += Vec3(movement, 0, 0)

        if keys["up"] != 0:
            velocity += Vec3(0, movement, 0)

        if keys["down"] != 0:
            velocity += Vec3(0, -movement, 0)
            
        self.setFluidPos(self.getPos() + velocity)