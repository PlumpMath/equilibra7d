from panda3d.core import PandaNode
from panda3d.core import NodePath

class Scenario(NodePath):
    def __init__(self, parent, model="models/sandbox"):
        NodePath.__init__(self, PandaNode("scenario"))
        
        self.model = loader.loadModel(model)
        self.model.reparentTo(self)
        
        self.reparentTo(parent)