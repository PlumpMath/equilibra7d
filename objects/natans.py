from random import random
from math import sin, cos

from panda3d.core import Point3, Vec3

from physicalnode import PhysicalNode
from handlers.collision import CollisionEventHandler


class Natan(PhysicalNode, CollisionEventHandler):
    ANIM_WALK = "anim1"
    JUMP_SOUND = ["water_jumping", 7]
    
    def __init__(self, parent, model, name="enemy"):
        PhysicalNode.__init__(self, parent, model, name, [self.ANIM_WALK])
        
        self.mass = 20.0
        
        self.addCollisionSphere(1.25)
        self._impact = 2
        
        self.model.loop(self.ANIM_WALK)
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        
        equismo = base.gameState.currentState.objects['equismo']
        otherVelocity = equismo.velocity
        otherMass = equismo.mass
        self.collide(-normal, otherVelocity, otherMass, 0.75)


class Natans:
    """Handles the dynamic creation and destruction of Natan objects."""
    
    def __init__(self, parent, model):
        self._parent = parent
        self._model = model
        self.enemies = []
        self.spawnProbability = 0.003
        self.idleTime = 0.5
    
    def setup(self):
        taskMgr.add(self.spawn, "NatanSpawn")
        
    def clear(self):
        self.enemies = []
        taskMgr.remove("NatanSpawn")

    def addNatan(self, position, scale):
        name = "enemy_%d" % len(self.enemies)
        enemy = Natan(self._parent, self._model, name)
        enemy.setPos(position)
        enemy.model.setScale(scale)
        enemy.collider.setScale(scale)
        
        # Collision
        self.addCollision(enemy)
        
        # Physics
        physicsManager = base.gameState.currentState.managers['physics']
        physicsManager.addActor(enemy)
        
        # AI
        aiManager = base.gameState.currentState.managers['ai']
        aiManager.addNatan(enemy, 50, 0.5, 1.5)

        # Audio
        audioManager = base.gameState.currentState.managers['audio']
        audioManager.playRandomEffect(Natan.JUMP_SOUND[0], 
                                      Natan.JUMP_SOUND[1])
        
        self.enemies.append(enemy)
        return enemy
    
    def spawn(self, task):
        if task.time < self.idleTime:
            return task.cont
        
        if random() < self.spawnProbability:
            angle = random() * 360
            x = 16 * cos(angle)
            y = 16 * sin(angle)
            
            position = Point3(x, y, -1)
            
            scale = random() * 0.35 + 0.15
            enemy = self.addNatan(position, scale)
            
            force = (Point3(0, 0, 0) - position) * 0.35
            force += Vec3(0, 0, 6)
            enemy.addImpulse(force)
            
        return task.cont
    
    def addCollision(self, enemy):
        collisionManager = base.gameState.currentState.managers['collision']
        collisionManager.addCollider(enemy)
        equismo = base.gameState.currentState.objects['equismo']
        collisionManager.addMutualCollisionHandling(equismo, enemy)
        
        for otherNatan in self.enemies:
            collisionManager.addMutualCollisionHandling(enemy, otherNatan)
        
    def addAI(self):
        aiManager = base.gameState.currentState.managers['ai']
        for enemy in self.enemies:
            aiManager.addNatan(enemy, 50, 0.5, 1.5)
        
    def addPhysics(self):
        physicsManager = base.gameState.currentState.managers['physics']
        for enemy in self.enemies:
            physicsManager.addActor(enemy)

    def getNatanFromCollisionNode(self, nodePath):
        """Returns the Natan object pointed by the given nodePath."""
        # name format: enemy_2_collision_node
        index = int(nodePath.getName()[len("enemy_")])
        return self.enemies[index]

