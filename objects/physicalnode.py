from panda3d.core import BitMask32, CollisionNode, CollisionSphere
from panda3d.physics import ActorNode, AngularVectorForce

from modelnode import ModelNode


class PhysicalNode(ModelNode):
    """A base class for nodes that have a 3d model, are controlled by
    physical simulation and have physical collision.
    
    Class hierarchy:
        NodePath --> ActorNode --> ModelNode
                               `-> CollisionNode
    
    Use `addCollisionSphere' or `addCollisionGeometry' to setup collision.
    Subclasses must implement `handleCollisionEvent'.
    """
    
    def __init__(self, parent, model, name, animations=None):
        ModelNode.__init__(self, parent, model, name, animations)
        actorNode = ActorNode(name + "_actor_node")
        self.actor = self.attachNewNode(actorNode)
        self.model.reparentTo(self.actor)
    
    #---------------------------------------------------------------------------
    # Methods that must be overwritten by subclasses
    #---------------------------------------------------------------------------
    def handleCollisionEvent(self, entry, type):
        """Handle a single collision event.
        
        This method is called whenever a relevant collision event occurs.
        The 'type' may be "into", "again" or "out".
        """
        raise NotImplementedError
    
    #---------------------------------------------------------------------------
    # PhysicalNode properties
    #---------------------------------------------------------------------------
    @property
    def velocity(self):
        """Return the node's current velocity vector as a Vec3."""
        return self.actor.node().getPhysicsObject().getVelocity()
    
    @velocity.setter
    def velocity(self, value):
        """Set the node's current velocity vector with a Vec3."""
        return self.actor.node().getPhysicsObject().setVelocity(value)
    
    @property
    def mass(self):
        """Return the actor's mass."""
        return self.actor.node().getPhysicsObject().getMass()
    
    @mass.setter
    def mass(self, value):
        """Set the actor's mass."""
        self.actor.node().getPhysicsObject().setMass(value)
    
    #---------------------------------------------------------------------------
    # Collision methods
    #---------------------------------------------------------------------------
    def addCollisionSphere(self, size):
        """Create a collision sphere and adds it to the node's tree.
        
        Its radius is given by 'size' and it is centered at the origin.
        """
        collisionSphere = CollisionSphere(0, 0, 0, size)
        collisionNode = CollisionNode(self.name + '_collision_node')
        collisionNode.addSolid(collisionSphere)

        self.collider = self.actor.attachNewNode(collisionNode)
        
        self.model.setCollideMask(BitMask32.allOff())
    
    def addCollisionGeometry(self, modelName):
        """Indicate that a geometry must be used in collision tests.
        
        A collision geometry must be defined along with the model and
        its name must follow the pattern modelNameC (e.g. treeC).
        """
        self.collider = self.model.find("**/%sC" % modelName)
    
    def collide(self, surfaceNormal, otherVelocity, otherMass, restitution):
        """Update the node's velocity after an inellastic collision."""
        # Initial velocities
        v1_i = self.velocity
        v1_i_norm = v1_i.project(-surfaceNormal)
        v1_i_tang = v1_i - v1_i_norm
        
        v2_i = otherVelocity
        v2_i_norm = v2_i.project(surfaceNormal)
        v2_i_tang = v2_i - v2_i_norm
        
        # Initial masses
        m1 = self.mass
        m2 = otherMass
        
        # Coefficient of Restitution
        cr = restitution
        
        # Final velocity
        v1_f_norm_mod = ((cr * m2 * (v2_i_norm.length() - v1_i_norm.length()) +
                          m1 * v1_i_norm.length() + 
                          m2 * v2_i_norm.length()) / 
                         (m1 + m2))
        v1_f_norm = surfaceNormal * v1_f_norm_mod
        v1_f = v1_f_norm + v1_i_tang
        
        self.velocity = v1_f
    
    #---------------------------------------------------------------------------
    # Helper methods
    #---------------------------------------------------------------------------
    def addImpulse(self, impulse):
        """Generate an instantaneous change in the node's velocity.
        
        This change is given by the vector 'impulse' as a Vec3.
        """
        self.actor.node().getPhysicsObject().addImpulse(impulse)

    def addImpact(self, offsetFromCenterOfMass, impulse):
        """Add an impulse and/or torque to the node based on an offset
        from the center of mass.
        """
        self.actor.node().getPhysicsObject().addImpact(offsetFromCenterOfMass,
                                                       impulse)
    
    def addLinearForce(self, force):
        """Add a linear force to this node.
        
        The parameter 'force' must be a LinearVectorForce.
        """
        self.actor.node().getPhysical(0).addLinearForce(force)
    
#    def clearForces(self):
#        physical = self.actor.node().getPhysical(0)
#        physical.clearAngularForces()
#        physical.clearLinearForces()
#        physical.clearPhysicsObjects()
    
    def addTorque(self, h, p, r):
        """Add a torque to the node.
        
        Return the corresponding 'AngularVectorForce'.
        """
        torque = AngularVectorForce(h, p, r)
        self.actor.node().getPhysical(0).addAngularForce(torque)
        return torque
        
    def removeTorque(self, torque):
        """Remove a torque (AngularForce) from the node."""
        self.actor.node().getPhysical(0).removeAngularForce(torque)

