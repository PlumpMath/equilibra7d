from panda3d.physics import AngularEulerIntegrator, ForceNode, LinearVectorForce


class PhysicsManager():
    """Handles the physics simulation."""
    
    def __init__(self):
        base.enableParticles()
        
        globalForcesNode = ForceNode("global_forces")
        self.forces = render.attachNewNode(globalForcesNode)

        integrator = AngularEulerIntegrator()
        base.physicsMgr.attachAngularIntegrator(integrator)
    
    def addLinearForce(self, x, y, z, physicalNode=None):
        """Adds a linear vector force to the simulation with the given 
        components.
        
        If a 'physicalNode' is given, the force will be aplied to it.
        Otherwise the force will be global.
        """
        force = LinearVectorForce(x, y, z)
        self.forces.node().addForce(force)
        
        if physicalNode is None:
            base.physicsMgr.addLinearForce(force)            
        else:
            physicalNode.addLinearForce(force)
    
    def addActor(self, physicalNode):
        """Adds a node to the simulation.
        
        The parameter 'physicalNode' must be an instance of 
        PhysicalNode.
        """
        base.physicsMgr.attachPhysicalNode(physicalNode.actor.node())

