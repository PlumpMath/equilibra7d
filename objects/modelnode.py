from panda3d.core import NodePath


class ModelNode(NodePath):
    """A wrapper class to a Panda3D node that has a model.
    
    Structure:
        PandaNode -> ModelNode
    """
    
    def __init__(self, parent, model, name=""):
        NodePath.__init__(self, name)
        
        self.model = loader.loadModel("models/" + model)
        self.model.reparentTo(self)

        self.reparentTo(parent)

        self.name = name

    def setup(self):
        """Reset object to default configuration"""
        raise NotImplementedError

