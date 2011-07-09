from panda3d.physics import AngularEulerIntegrator, ForceNode, LinearVectorForce

from base import Manager


class PhysicsManager(Manager):
    """Handles the physics simulation."""
    
    def __init__(self):
        base.enableParticles()
        base.physicsMgr.attachAngularIntegrator(AngularEulerIntegrator())
        self.forces = render.attachNewNode(ForceNode("global_forces"))
        self.gravity = None
        self._physicalnodes = []
    
    def setGravity(self, value):
        if self.gravity:
            self.removeLinearForce(self.gravity)
        self.gravity = self.addLinearForce(0, 0, -value)
    
    def setup(self):
        base.enableParticles()
        self.setGravity(9.8)
        
        # Equismo
        self.addActor(base.gameState.currentState.objects['equismo'])
        
        # Enemies
        base.gameState.currentState.objects['enemy'].addPhysics()
    
    def clear(self):
        self.forces.removeChildren()
        base.physicsMgr.clearAngularForces()
        base.physicsMgr.clearLinearForces()
        while self._physicalnodes:
            base.physicsMgr.removePhysicalNode(self._physicalnodes.pop())
        base.disableParticles()
    
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
        return force
    
    def removeLinearForce(self, force, physicalNode=None):
        (physicalNode or base.physicsMgr).removeLinearForce(force)
    
    def addActor(self, physicalNode):
        """Adds a node to the simulation.
        
        The parameter 'physicalNode' must be an instance of 
        PhysicalNode.
        """
        node = physicalNode.actor.node()
        base.physicsMgr.attachPhysicalNode(node)
        self._physicalnodes.append(node)

