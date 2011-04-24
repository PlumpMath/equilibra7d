from panda3d.core import NodePath
from panda3d.core import BitMask32

class Scenario(NodePath):
    def __init__(self, parent, model, taskMgr, keys):
        NodePath.__init__(self, "scenario")
        
        self.model = loader.loadModel("models/" + model)
        self.model.reparentTo(self)
        
        ## Explicitly tells Panda to use the Collision Mesh
        #self.model.setCollideMask(BitMask32.allOff())        
        #self.collider = self.model.find("**/sandbox-c")
        #self.collider.node().setIntoCollideMask(BitMask32.bit(0))
        
        self.taskMgr = taskMgr
        self.taskMgr.add(self.rotationTask, "scenario_rotation")
        
        self.keys = keys
        
        self.reparentTo(parent)
    
    def rotationTask(self, task):
        dt = globalClock.getDt()

        if self.keys["left"] != 0:
            self.setP(self.getP() + 10 * dt)

        if self.keys["right"] != 0:
            self.setP(self.getP() - 10 * dt)

        if self.keys["up"] != 0:
            self.setR(self.getR() - 10 * dt)

        if self.keys["down"] != 0:
            self.setR(self.getR() + 10 * dt)
        
        return task.cont
