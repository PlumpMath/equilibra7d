from random import random, choice, randint, uniform
from math import sin, cos, floor

from panda3d.ai import AIWorld, AICharacter
from panda3d.core import Point3, Vec3

from handlers.audio import AudioHandler
from physicalnode import PhysicalNode


class Natan(PhysicalNode):
    ANIMATIONS = ["walk"]
    
    def __init__(self, parent, model, name,
                       ai_world, mass, movt_force, max_force):
        PhysicalNode.__init__(self, parent, model, name)
        
        self.mass = mass
        self.addCollisionSphere(1.25)
        
        self.toggleWalkAnimation()
        
        #-----------------------------------------------------------------------
        # Artificial Intelligence
        #-----------------------------------------------------------------------
        self.ai_char = AICharacter("ai_%s" % name, self.actor, mass, movt_force, max_force)
        ai_world.addAiChar(self.ai_char)
        aiBehaviors = self.ai_char.getAiBehaviors()
        equismo = base.gameState.currentState.objects['equismo']
        aiBehaviors.pursue(equismo.actor)
    
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        
        equismo = base.gameState.currentState.objects['equismo']
        otherVelocity = equismo.velocity
        otherMass = equismo.mass
        self.collide(-normal, otherVelocity, otherMass, 0.75)
    
    def toggleWalkAnimation(self):
        if self.model.getCurrentAnim() == "walk":
            self.model.stop()
        else:
            self.model.loop("walk", restart=False)


class Natans(AIWorld, AudioHandler):
    """Handles the dynamic creation and destruction of Natan objects."""
    SFX_FILES = ["water_jumping1.wav", "water_jumping2.wav",
                 "water_jumping3.wav", "water_jumping4.wav",
                 "water_jumping5.wav", "water_jumping6.wav",
                 "water_jumping7.wav"]
    
    def __init__(self, parent, models, amount):
        AIWorld.__init__(self, parent)
        self._parent = parent
        self._models = models
        self.amount = amount
        
        # max number of new natans in a spawn
        self._max_enemies_per_spawn = floor(0.3 * amount)
        # min and max time between spawns in seconds
        self._idle_time_range = (5, 10)
        
        self.enemies = []
    
    @debug(['objects'])
    def setup(self):
        self.addTask(self.update, "AIUpdate")
        self.doMethodLater(self._idle_time_range[0], self.spawn, 'spawn natans')
        
        # Start walk animation
        for enemy in self.enemies:
            enemy.toggleWalkAnimation()
    
    @debug(['objects'])
    def clear(self):
        self.removeAllTasks()
        
        # Stop walk animation
        for enemy in self.enemies:
            enemy.toggleWalkAnimation()
    
    #---------------------------------------------------------------------------
    
    def addEnemy(self, position, scale):
        """Add a new artificially intelligent NPC."""
        name = "enemy_%d" % len(self.enemies)
        enemy = Natan(self._parent, choice(self._models), name,
                      self, 35.0, 0.5, 1.5)
        enemy.setPos(position)
        enemy.model.setScale(scale)
        enemy.collider.setScale(scale)
        
        # Collision
        self.addCollision(enemy)
        
        # Physics
        physicsManager = base.gameState.currentState.managers['physics']
        physicsManager.addActor(enemy)
        
        # Audio
        self.playRandomEffect()
        
        self.enemies.append(enemy)
        return enemy
    
    def update(self, task):
        """Update the AI World.
        
        If the AI is paused, does nothing.
        """
        if hasattr(self, "_paused") and self._paused:
            pass
        else:
            AIWorld.update(self)
            
        return task.cont
    
    def pause_ai(self):
        """Temporarily turn off AI."""
        self._paused = True
    
    def resume_ai(self):
        """Turn AI back on."""
        self._paused = False
    
    #---------------------------------------------------------------------------
    
    def spawn(self, task):
        """Create Natans and throw them to the ice platform."""
        enemies_left = self.amount - len(self.enemies)
        how_many = randint(1, min(enemies_left, self._max_enemies_per_spawn))
        
        for i in xrange(how_many):
            angle = random() * 360
            x = 16 * cos(angle)
            y = 16 * sin(angle)
            
            position = Point3(x, y, -1)
            scale = random() * 0.35 + 0.15
            
            enemy = self.addEnemy(position, scale)
            
            force = (Point3(0, 0, 0) - position) * 0.35
            force += Vec3(0, 0, 6)
            enemy.addImpulse(force)
        
        enemies_left = self.amount - len(self.enemies)
        
        if enemies_left > 0:
            task.delayTime = uniform(*self._idle_time_range)
            return task.again
        else:
            return task.done
    
    def addCollision(self, enemy):
        collisionManager = base.gameState.currentState.managers['collision']
        collisionManager.addCollider(enemy)
        equismo = base.gameState.currentState.objects['equismo']
        collisionManager.addMutualCollisionHandling(equismo, enemy)
        
        for otherNatan in self.enemies:
            collisionManager.addMutualCollisionHandling(enemy, otherNatan)
    
    def addPhysics(self):
        physicsManager = base.gameState.currentState.managers['physics']
        for enemy in self.enemies:
            physicsManager.addActor(enemy)
    
    def getNatanFromCollisionNode(self, nodePath):
        """Returns the Natan object pointed by the given nodePath."""
        # name format: enemy_2_collision_node
        index = int(nodePath.getName()[len("enemy_")])
        return self.enemies[index]

