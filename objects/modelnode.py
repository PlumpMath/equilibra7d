from direct.actor.Actor import Actor
from panda3d.core import NodePath


class ModelNode(NodePath):
    """A base class for nodes that have a 3d model.
    
    Class hierarchy:
        NodePath --> ModelNode
    """
    ANIMATIONS = []
    
    def __init__(self, parent, model, name=""):
        NodePath.__init__(self, name)
        self.name = name
        
        if not self.ANIMATIONS:
            # Load static model
            self.model = loader.loadModel("models/%s.bam" % (model,))
        else:
            # Load animated model
            animations = dict((name, "models/%s-%s.bam" % (model, name))
                              for name in self.ANIMATIONS)
            self.model = Actor("models/%s.bam" % (model,), animations)
        
        self.model.reparentTo(self)
        self.reparentTo(parent)
    
    def setup(self):
        """Reset object to default configuration"""
        raise NotImplementedError

