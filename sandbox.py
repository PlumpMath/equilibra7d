from panda3d.core import Vec4
from panda3d.core import VBase4
from panda3d.core import AmbientLight
from panda3d.core import PointLight

from direct.showbase.ShowBase import ShowBase

from scenario import Scenario
from character import Character

class Sandbox(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scenario = Scenario(self.render, "models/sandbox")
        self.scenario.setH(-90)

        self.character = Character(self.render, "models/ball")
        self.character.setPos(0, -23, 4)
        
        self.initLights()
        
    def initLights(self):
        self.ambientLight = AmbientLight('ambientLight')
        self.ambientLight.setColor(Vec4(0.3, 0.3, 0.3, 1))
        
        ambientLightNP = self.render.attachNewNode(self.ambientLight)
        self.render.setLight(ambientLightNP)

        self.pointLight = PointLight('pointLight')
        self.pointLight.setColor(VBase4(1, 1, 1, 1))
        pointLightNP = self.render.attachNewNode(self.pointLight)
        pointLightNP.setPos(0, -25, 8)
        self.render.setLight(pointLightNP)

        
sandbox = Sandbox()
sandbox.run()
