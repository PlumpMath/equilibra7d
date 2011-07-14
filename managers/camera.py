from base import Manager


class CameraManager(Manager):
    """Handles game's camera."""
    
    def __init__(self):        
        base.disableMouse()
        self.camera = base.camera
            
    @debug(['managers'])
    def setup(self):
        self.camera.reparentTo(base.render)
        self.camera.setPos(0, -40, 15)
        self.camera.lookAt(0, 0, 0)
    
    @debug(['managers'])
    def clear(self):
        pass
    
    def follow(self, nodePath):
        """Allow the camera follow a given nodePath"""
        self.camera.reparentTo(nodePath)
        self.camera.setPos(2, -10, -0.2)
        self.camera.lookAt(0, 0, 0)

