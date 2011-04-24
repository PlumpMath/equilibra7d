from panda3d.core import NodePath
from panda3d.core import BitMask32

class Scenario(NodePath):
    def __init__(self, parent, model="sandbox"):
        NodePath.__init__(self, "scenario")
        
        self.model = loader.loadModel("models/" + model)
        self.model.reparentTo(self)
        
        ## Explicitly tells Panda to use the Collision Mesh
        #self.model.setCollideMask(BitMask32.allOff())        
        #self.collider = self.model.find("**/sandbox-c")
        #self.collider.node().setIntoCollideMask(BitMask32.bit(0))
        
        self.reparentTo(parent)