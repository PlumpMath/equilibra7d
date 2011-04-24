from panda3d.core import PandaNode
from panda3d.core import NodePath
from panda3d.physics import ActorNode

class Character(NodePath):
    def __init__(self, parent, model="models/character"):
        NodePath.__init__(self, PandaNode("character"))
        
        actorNode = ActorNode("characterActorNode")
        self.actor = self.attachNewNode(actorNode)
        
        self.model = loader.loadModel(model)
        self.model.reparentTo(self.actor)        
        
        self.reparentTo(parent)