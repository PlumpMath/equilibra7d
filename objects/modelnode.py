from panda3d.core import NodePath

from direct.actor.Actor import Actor

class ModelNode(NodePath):
    """A wrapper class to a Panda3D node that has a model.
    
    Structure:
        PandaNode -> ModelNode
    """
    
    def __init__(self, parent, model, name="", animations=[]):
        NodePath.__init__(self, name)
        
        if animations:  # List is not empty
            animationDict = {}
            for name in animations:
                animationDict[name] = "models/%s-%s.egg" % (model, name) 
            
            self.model = Actor("models/%s.egg" % (model,), animationDict)
            
        else:
            self.model = loader.loadModel("models/%s.egg" % (model,))
            
        self.model.reparentTo(self)
        
        self.reparentTo(parent)
        
        self.name = name
    
    def setup(self):
        """Reset object to default configuration"""
        raise NotImplementedError

