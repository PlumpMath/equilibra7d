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
        
    def addActor(self, node):
        """
        Adds a node to the simulation.
        The node must have a member 'actor' poiting to a 
        panda3d.physics.ActorNode.
        """
        
        self.world.physicsMgr.attachPhysicalNode(node.actor.node())
