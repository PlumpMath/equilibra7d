from panda3d.core import BitMask32

from physicalnode import PhysicalNode

class Scenario(PhysicalNode):
    def __init__(self, parent, model):
        PhysicalNode.__init__(self, parent, model, "scenario")
