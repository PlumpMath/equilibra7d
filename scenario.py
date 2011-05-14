from panda3d.core import BitMask32

from modelnode import ModelNode

class Scenario(ModelNode):
    def __init__(self, parent, model):
        ModelNode.__init__(self, parent, model, "scenario")       
        
        self.setCollideMask(BitMask32.bit(0))
