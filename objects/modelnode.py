from direct.actor.Actor import Actor
from panda3d.core import NodePath


class ModelNode(NodePath):
    """A base class for nodes that have a 3d model.
    
    Class hierarchy:
        NodePath --> ModelNode
    """
    
    def __init__(self, parent, model, name="", animations=None):
        NodePath.__init__(self, name)
        self.name = name
        
        if animations is None:
            # Load static model
            self.model = loader.loadModel("models/%s.egg" % (model,))
        else:
            # Load animated model
            animations = dict((name, "models/%s-%s.egg" % (model, name)) for name in animations)
            self.model = Actor("models/%s.egg" % (model,), animations)
        
        self.model.reparentTo(self)
        self.reparentTo(parent)
    
    def setup(self):
        """Reset object to default configuration"""
        raise NotImplementedError

