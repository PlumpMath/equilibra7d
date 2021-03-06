from random import choice, randint, uniform
from math import sin, cos, floor

from direct.showbase.DirectObject import DirectObject
from panda3d.ai import AIWorld, AICharacter
from panda3d.core import Point3, Vec3

from physicalnode import PhysicalNode


class Natan(PhysicalNode):
    ANIMATIONS = ["walk"]
    JUMP_SOUND = ["water_jumping", 7]
    
    def __init__(self, parent, model, name,
                       ai_world, mass, movt_force, max_force):
        PhysicalNode.__init__(self, parent, model, name)
        
        self.mass = mass
        self.addCollisionSphere(1.25)
        
        self.toggleWalkAnimation()
        
        #-----------------------------------------------------------------------
        # Initialize Artificial Intelligence
        #-----------------------------------------------------------------------
        self.ai_char = AICharacter("ai_%s" % name, self.actor, mass, movt_force, max_force)
        ai_world.addAiChar(self.ai_char)
        aiBehaviors = self.ai_char.getAiBehaviors()
        equismo = base.gameState.currentState.objects['equismo']
        aiBehaviors.pursue(equismo.actor)
    
    #---------------------------------------------------------------------------
    # Animation
    #---------------------------------------------------------------------------
    def toggleWalkAnimation(self):
        if self.model.getCurrentAnim() == "walk":
            self.model.stop()
        else:
            self.model.loop("walk", restart=False)
    
    #---------------------------------------------------------------------------
    # Collision
    #---------------------------------------------------------------------------
    def handleCollisionEvent(self, entry, type):
        normal = entry.getSurfaceNormal(self)
        normal.z = 0
        normal.normalize()
        
        equismo = base.gameState.currentState.objects['equismo']
        otherVelocity = equismo.velocity
        otherMass = equismo.mass
        self.collide(-normal, otherVelocity, otherMass, 0.75)


class Natans(AIWorld, DirectObject):
    """Handles the dynamic creation and destruction of Natan objects."""
    
    def __init__(self, parent, models, amount):
        AIWorld.__init__(self, parent)
        self._parent = parent
        self._models = models
        self.amount = amount
        
        # min and max time between spawns in seconds
        self._idle_time_range = (2, 8)
        
        self.enemies = []
    
    #---------------------------------------------------------------------------
    # State
    #---------------------------------------------------------------------------
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
    
    def pause_ai(self):
        """Temporarily turn off AI."""
        self._paused = True
    
    def resume_ai(self):
        """Turn AI back on."""
        self._paused = False
    
    #---------------------------------------------------------------------------
    # Enemy creation
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
        audioManager = base.gameState.currentState.managers['audio']
        audioManager.playRandomEffect(Natan.JUMP_SOUND[0],
                                      Natan.JUMP_SOUND[1])
        
        self.enemies.append(enemy)
        return enemy
    
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
    
    #---------------------------------------------------------------------------
    # Tasks
    #---------------------------------------------------------------------------
    def update(self, task):
        """Update the AI World.
        
        If the AI is paused, does nothing.
        """
        if hasattr(self, "_paused") and self._paused:
            pass
        else:
            AIWorld.update(self)
        
        return task.cont
    
    def spawn(self, task):
        """Create Natans and throw them to the ice platform."""
        angle = uniform(0, 360)
        x = 16 * cos(angle)
        y = 16 * sin(angle)
        
        position = Point3(x, y, -1)
        scale = uniform(0.15, 0.5)
        
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

