from direct.showbase.ShowBase import ShowBase

from scenario import Scenario

class Sandbox(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scenario = Scenario(self.render, "models/sandbox")
        
sandbox = Sandbox()
sandbox.run()