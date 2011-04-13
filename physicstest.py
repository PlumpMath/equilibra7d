from panda3d.core import NodePath
from panda3d.physics import ActorNode
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

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
        # Set gravity
        gravityNode = ForceNode('world_forces')
        gravityForce = LinearVectorForce(0, 0, -0.1) #gravity acceleration
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

        # Load and transform the ball actor.
        self.ball = self.loader.loadModel("models/ball")
        self.ball.reparentTo(self.ballActor)
        self.ball.setScale(10.0)
        self.ball.setPos(0, 0, 10.0)

        ## Camera
        # Set up camera
        self.disableMouse()
        self.camera.setPos(0, -23, 2)



world = World()
world.run()

