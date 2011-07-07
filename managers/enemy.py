from random import random
from math import sin, cos

from panda3d.core import Point3

from objects import Enemy

from base import Manager


class EnemyManager(Manager):
    """Handles the dynamic creation and destruction of Enemy objects."""
    
    def __init__(self):
        self.enemies = []
        self.spawnProbability = 0.002
    
    def setup(self):
        taskMgr.add(self.spawn, "EnemySpawn")
        
    def clear(self):
        self.enemies = []
        taskMgr.remove("EnemySpawn")

    def addEnemy(self, model, position, scale):
        name = "enemy_%d" % (len(self.enemies),)
        enemy = Enemy(base.objectsNode, model, name)
        enemy.setPos(position)
        enemy.setScale(scale)
        
        # Collision
        self.addCollision(enemy)
        
        # Physics
        base.physicsManager.addActor(enemy)
        
        # AI
        base.aiManager.addEnemy(enemy, 50, 0.5, 1.5)
        
        self.enemies.append(enemy)
    
    def spawn(self, task):
        if random() < self.spawnProbability: 
            self.addEnemy("enemyfish", Point3(-4, 0, 1), 0.4)
            
#        self.addEnemy("enemyfish", Point3(-4, 2, 1), 0.4)
#        self.addEnemy("enemyfish", Point3(-4, -2, 1), 0.4)
#        self.addEnemy("enemyfish", Point3(-4, 4, 1), 0.4)
#        self.addEnemy("enemyfish", Point3(-4, -4, 1), 0.4)
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
