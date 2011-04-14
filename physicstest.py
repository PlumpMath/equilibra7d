from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.core import BitMask32
from panda3d.core import Plane
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionPlane
from panda3d.core import CollisionTraverser
from panda3d.physics import ActorNode
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from panda3d.physics import PhysicsCollisionHandler

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


        ## Physics

        # Enable the particle system
        self.enableParticles()

        # Create physics node        
        self.physics = NodePath("physics_node")
        self.physics.reparentTo(self.render)

        # Create ball actor
        ballActorNode = ActorNode("ball_physics")
        self.ballActor = self.physics.attachNewNode(ballActorNode)
        self.physicsMgr.attachPhysicalNode(self.ballActor.node())
        self.ballActor.node().getPhysicsObject().setMass(0.5)

        # Set gravity
        gravityNode = ForceNode('world_forces')
        gravityForce = LinearVectorForce(0, 0, -9.81) #gravity acceleration
        gravityForce.setMassDependent(True)
        gravityNode.addForce(gravityForce)

        self.gravity = render.attachNewNode(gravityNode)
        self.physicsMgr.addLinearForce(gravityForce)


        ## Models

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.environ.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Load and transform the ball model.
        self.ballModel = self.loader.loadModel("models/ball")
        self.ballModel.reparentTo(self.ballActor)
        self.ballModel.setScale(10)
        self.ballActor.setPos(0, 0, 10)

        # Set collide mask
        self.ballModel.setCollideMask(BitMask32.allOff())


        ## Colision

        # Create collision traverser
        self.cTrav = CollisionTraverser()
        self.cTrav.showCollisions(render)

        # Create collision handler
        self.collisionHandler = PhysicsCollisionHandler()

        # Create and set collision node for the ball.
        ballCollisionNode = CollisionNode('ball_collision')
        self.ballCollision = self.ballActor.attachNewNode(ballCollisionNode)
        self.ballCollision.node().addSolid(CollisionSphere(0, 0, 0, 4))
        self.ballCollision.show()

        # Set collision mask
        self.ballCollision.node().setFromCollideMask(BitMask32(0x1))
        self.ballCollision.node().setIntoCollideMask(BitMask32.allOff())

        # Create and set collision node for the floor.
        floorCollisionNode = CollisionNode('floor_collision')
        self.floorCollision = self.environ.attachNewNode(floorCollisionNode)
        floor = Plane(Vec3(0, 0, 1), Point3(0, 0, 0))
        self.floorCollision.node().addSolid(CollisionPlane(floor))
        self.floorCollision.show()

        # Set collision mask
        self.floorCollision.node().setFromCollideMask(BitMask32.allOff())
        self.floorCollision.node().setIntoCollideMask(BitMask32(0x1))


        # Add ball to collision traverser
        self.cTrav.addCollider(self.ballCollision, self.collisionHandler)
        self.collisionHandler.addCollider(self.ballCollision, self.ballActor)

        ## Camera
        # Set up camera
        #self.disableMouse()
        self.camera.setPos(0, -50, 10)
        self.camera.lookAt(self.ballActor)

        ## Keyboard events
        # Register "enter" event
        self.accept("a", self.scenarioRoll, ["left"])
        self.accept("d", self.scenarioRoll, ["right"])

    def scenarioRoll(self, direction):
        if direction == "left":
            self.environ.setR(self.environ.getR() + 1)

        else:
            self.environ.setR(self.environ.getR() - 1)

world = World()
world.run()

