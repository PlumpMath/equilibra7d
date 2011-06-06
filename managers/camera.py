class CameraManager:
    def __init__(self, camera, character, taskMgr):
        self.camera = camera
        self.character = character
        self.taskMgr = taskMgr
        
        self.taskMgr.add(self.trackTask, "camera_tracking", priority = 35)
        
    def trackTask(self, task):
        self.camera.setX(self.character.getX())
        self.camera.setY(self.character.getY() - 8)
        self.camera.setZ(self.character.getZ() + 4)
        
        self.camera.lookAt(self.character)
        
        return task.cont

