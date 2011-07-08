from random import random
from math import sin, cos

from panda3d.core import Point3, Vec3

from objects import Enemy

from base import Manager


class EnemyManager(Manager):
    """Handles the dynamic creation and destruction of Enemy objects."""
    
    def __init__(self):
        self.enemies = []
        self.spawnProbability = 0.003
        self.idleTime = 0.5
    
    def setup(self):
        taskMgr.add(self.spawn, "EnemySpawn")
        
    def clear(self):
        self.enemies = []
        taskMgr.remove("EnemySpawn")

    def addEnemy(self, model, position, scale):
        name = "enemy_%d" % (len(self.enemies),)
        enemy = Enemy(base.objectsNode, model, name)
        enemy.setPos(position)
        enemy.model.setScale(scale)
        enemy.collider.setScale(scale)
        
        # Collision
        self.addCollision(enemy)
        
        # Physics
        base.physicsManager.addActor(enemy)
        
        # AI
        base.aiManager.addEnemy(enemy, 50, 0.5, 1.5)
        
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
            enemy = self.addEnemy("enemyfish_blue", position, scale)
            
            force = (Point3(0, 0, 0) - position) * 0.35
            force += Vec3(0, 0, 6)
            enemy.addImpulse(force)
            
        return task.cont
    
    def addCollision(self, enemy):
        base.collisionManager.addCollider(enemy)
        base.collisionManager.addMutualCollisionHandling(base.character, enemy)
        
        for otherEnemy in self.enemies:
            base.collisionManager.addMutualCollisionHandling(enemy, otherEnemy)
        
    def addAI(self):
        for enemy in self.enemies:
            base.aiManager.addEnemy(enemy, 50, 0.5, 1.5)
        
    def addPhysics(self):
        for enemy in self.enemies:
            base.physicsManager.addActor(enemy)

    def getEnemyFromCollisionNode(self, nodePath):
        """Returns the Enemy object pointed by the given nodePath."""
        
        # name format: enemy_2_collision_node
        index = int(nodePath.getName()[len("enemy_")])
        return self.enemies[index]
