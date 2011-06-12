from panda3d.physics import AngularEulerIntegrator, ForceNode, LinearVectorForce

from manager import Manager


class PhysicsManager(Manager):
    """Handles the physics simulation."""
    
    def __init__(self, gravity=9.8):
        #self._physicals = set()
        base.enableParticles()
        self.forces = render.attachNewNode(ForceNode("global_forces"))
        base.physicsMgr.attachAngularIntegrator(AngularEulerIntegrator())
        
        self.gravity = None
        self.setGravity(gravity)
    
    def setGravity(self, value):
        if self.gravity:
            self.removeLinearForce(self.gravity)
        self.gravity = self.addLinearForce(0, 0, -value)
    
    def clear(self):
        self.forces.removeChildren()
        base.physicsMgr.clearAngularForces()
        base.physicsMgr.clearLinearForces()
        
        # TODO: The current implementation is not perfect.
        #       Only the gravity gets removed by the code above.
        #       To remove movement from nodes such as the main character,
        #       the enemy and the scenario, we could do:
        #
        base.physicsMgr.clearPhysicals()
        #
        #       However, after that, in order to restart the game we still need
        #       to reconnect a lot of "wires". For example, the code below
        #       inserts a new main character, but without collision against
        #       the scenario...
        
#        base.character.removeChildren()
#        import sys
#        from character import Character
#        # Place the character in the world
#        if len(sys.argv) == 2:
#            model = sys.argv[1]
#        else:
#            model = "character_1_4"
#        base.character = Character(render, model)
#        base.character.setZ(5)
#        base.character.setScale(0.8)
#        self.addActor(base.character)
        
        #       Finally, we could store every physicalNode and then clear
        #       their forces:
        
        #for node in self._physicals:
        #for node in (base.enemy, base.character):
        #    node.clearForces()
    
    def addLinearForce(self, x, y, z, physicalNode=None):
        """Adds a linear vector force to the simulation with the given 
        components.
        
        If a 'physicalNode' is given, the force will be aplied to it.
        Otherwise the force will be global.
        """
        force = LinearVectorForce(x, y, z)
        self.forces.node().addForce(force)
        physicalNode = physicalNode or base.physicsMgr
        physicalNode.addLinearForce(force)
        #self._physicals.add(physicalNode)
        return force
    
    def removeLinearForce(self, force, physicalNode=None):
        (physicalNode or base.physicsMgr).removeLinearForce(force)
    
    def addActor(self, physicalNode):
        """Adds a node to the simulation.
        
        The parameter 'physicalNode' must be an instance of 
        PhysicalNode.
        """
        base.physicsMgr.attachPhysicalNode(physicalNode.actor.node())

