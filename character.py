from panda3d.core import PandaNode
from panda3d.core import NodePath

class Character(NodePath):
    def __init__(self, parent, model="models/character"):
        NodePath.__init__(self, PandaNode("character"))
        
        self.model = loader.loadModel(model)
        self.model.reparentTo(self)
        
        self.reparentTo(parent)