from panda3d.core import TransparencyAttrib

from modelnode import ModelNode


class Sea(ModelNode):
    def __init__(self, parent, model):
        ModelNode.__init__(self, parent, model, "sea")
    
    def setup(self):
        self.setTransparency(TransparencyAttrib.MAlpha)
        self.setAlphaScale(0.7)
        self.setScale(20)

