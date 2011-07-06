from objects import Enemy

from base import Manager


class EnemyManager(Manager):
    """Handles the dynamic creation and destruction of Enemy objects."""

    def __init__(self):
        pass
    
    def setup(self):
        self.enemy = Enemy(base.objectsNode, "enemyfish")
        self.enemy.setPos(4, 0, 1)
        self.enemy.setScale(0.4)
        
        # Collision
        self.addCollision()
        
    def clear(self):
        pass

    def addCollision(self):
        base.collisionManager.addCollider(self.enemy)
        base.collisionManager.addCollisionHandling(self.enemy.collider,
                                                   "into",
                                                   base.character,
                                                   self.enemy)
        
    def addAI(self):
        base.aiManager.addEnemy(self.enemy, 50, 0.5, 1.5)
        
    def addPhysics(self):
        base.physicsManager.addActor(self.enemy)

    def getEnemyFromCollisionNode(self, nodePath):
        """Returns the Enemy object pointed by the given nodePath."""
        # There's only one enemy.
        return self.enemy
