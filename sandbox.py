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
    
sandbox = Sandbox()
sandbox.run()