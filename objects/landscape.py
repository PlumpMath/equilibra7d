from modelnode import ModelNode


class Landscape(ModelNode):
    def __init__(self, parent, model):
        ModelNode.__init__(self, parent, model, "landscape")
    
    def setup(self):
        self.setScale(20)

