from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce

class PhysicsManager():
    """Handles the physics simulation."""
    
    def __init__(self, world):
        world.enableParticles()
        
        globalForcesNode = ForceNode("global_forces")
        self.globalForces = world.render.attachNewNode(globalForcesNode)
        
        self.world = world
        
    def addLinearForce(self, x, y, z):
        """
        Adds a linear vector force to the simulation with the given 
        components.
        """        
        force = LinearVectorForce(x, y, z)
        
        self.globalForces.node().addForce(force)
        self.world.physicsMgr.addLinearForce(force)
        
    def addActor(self, actor):
        """
        Receives a panda3d.physics.ActorNode and adds it to the 
        simulation.
        """        
        self.world.physicsMgr.attachPhysicalNode(actor)
