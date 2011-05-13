from direct.showbase.ShowBase import ShowBase

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

world = World()
world.run()
