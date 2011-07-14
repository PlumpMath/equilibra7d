from modelnode import ModelNode


class DeadEquismo(ModelNode):
    def __init__(self, parent, model):
        ModelNode.__init__(self, parent, model, "dead_equismo")
    
        self.setScale(0.8)
        self.setPos(10, 10, -10)
