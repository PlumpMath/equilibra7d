from panda3d.core import VBase4
from panda3d.core import AmbientLight
from panda3d.core import PointLight

class LightingManager():
    def __init__(self, world):
        self.render = world.render               
        
    def setAmbientLight(self, r, g, b):
        ambientLightNode = AmbientLight('ambient_light')
        ambientLightNode.setColor(VBase4(r, g, b, 1))
        
        self.ambientLight = self.render.attachNewNode(ambientLightNode)
        self.render.setLight(self.ambientLight)

    def setPointLight(self, r, g, b, x, y, z):
        pointLightNode = PointLight('point_light')
        pointLightNode.setColor(VBase4(r, g, b, 1))

        self.pointLight = self.render.attachNewNode(pointLightNode)
        self.pointLight.setPos(x, y, z)
        self.render.setLight(self.pointLight)
