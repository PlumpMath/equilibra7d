from panda3d.core import BitMask32
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.physics import ActorNode

from modelnode import ModelNode

class PhysicalNode(ModelNode):
    """
    A wrapper class to a Panda3D node that has a model and will be
    controlled by the physical simulation.
    
    Structure:
        PandaNode -> ActorNode -> ModelNode
                               -> CollisionNode (optional)
    """
    
    def __init__(self, parent, model, name):
        ModelNode.__init__(self, parent, model, name)
        
        actorNode = ActorNode(name + "_actor_node")
        self.actor = self.attachNewNode(actorNode)
                
        self.model.reparentTo(self.actor)

    def addCollisionSphere(self, size):
        """
        Creates a collision sphere and adds it to the node's tree.
        Its radius is given by 'size' and it is centered at the origin.
        """
        collisionSphere = CollisionSphere(0, 0, 0, size)
        collisionNode = CollisionNode(self.name + '_collision_node')
        collisionNode.addSolid(collisionSphere)

        self.collider = self.actor.attachNewNode(collisionNode)
        
        self.model.setCollideMask(BitMask32.allOff())
    
    def addCollisionGeometry(self, modelName):
        """
        Indicates that a geometry must be used in collision tests.
        A collision geometry must be defined along with the model and
        its name must follow the pattern modelNameC (e.g. treeC).
        """
        self.collider = self.model.find("**/%sC" % modelName)
    
    def addImpulse(self, impulse):
        """
        Generates an instantaneous change in the node's velocity.
        This change is given by the vector 'impulse' as a Vec3.
        """
        self.actor.node().getPhysicsObject().addImpulse(impulse)

    def addImpact(self, offsetFromCenterOfMass, impulse):
        """
        Adds an impulse and/or torque to the node based on an offset
        from the center of mass.
        """
        self.actor.node().getPhysicsObject().addImpact(offsetFromCenterOfMass,
                                                       impulse)
    
    def addLinearForce(self, force):
        """
        Adds a linear force to this node.
        The parameter 'force' must be a LinearVectorForce.
        """
        self.actor.node().getPhysical(0).addLinearForce(force)
        
    def getVelocity(self):
        """
        Returns the node's current velocity vector as a Vec3.
        """
        return self.actor.node().getPhysicsObject().getVelocity()
