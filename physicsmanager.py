from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from panda3d.physics import AngularEulerIntegrator

class PhysicsManager():
    """Handles the physics simulation."""
    
    def __init__(self, world):
        world.enableParticles()
        
        globalForcesNode = ForceNode("global_forces")
        self.forces = world.render.attachNewNode(globalForcesNode)

        integrator = AngularEulerIntegrator()
        world.physicsMgr.attachAngularIntegrator(integrator)
        
        self.world = world
        
    def addLinearForce(self, x, y, z, physicalNode=None):
        """
        Adds a linear vector force to the simulation with the given 
        components.
        If a 'physicalNode' is given, the force will be aplied to it.
        Otherwise the force will be global.
        """
        
        force = LinearVectorForce(x, y, z)
        self.forces.node().addForce(force)
        
        if physicalNode is None:
            self.world.physicsMgr.addLinearForce(force)            
        else:
            physicalNode.addLinearForce(force)
    
    def addActor(self, physicalNode):
        """
        Adds a node to the simulation.
        The parameter 'physicalNode' must be an instance of 
        PhysicalNode.
        """
        
        self.world.physicsMgr.attachPhysicalNode(physicalNode.actor.node())
