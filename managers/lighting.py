from panda3d.core import AmbientLight, DirectionalLight, PointLight, VBase4


class LightingManager:
    """Handles the lighting of the 3D scene."""
    
    def __init__(self, **lights):
        self.lights = l = render.attachNewNode("equilibra7d_lights")
        self.ambient = l.attachNewNode(AmbientLight('ambient_light'))
        self.point = l.attachNewNode(PointLight('point_light'))
        self.directional = l.attachNewNode(DirectionalLight('directional_light'))
        
        self.setDefaultLights()
        self.setLights(**lights)
    
    def setLights(self, **lights):
        """Set one or more lights at a time."""
        for kind in "ambient point directional".split():
            light = lights.get(kind)
            if light is not None:
                getattr(self, "set%sLight" % kind.capitalize())(*light)
    
    def setDefaultLights(self):
        default = dict(
            ambient = (0.3, 0.3, 0.3),
            point = (0.4, 0.4, 0.4, 0, -8, 5),
            directional = (0.4, 0.4, 0.6, 0, -60, 0),
        )
        self.setLights(**default)
    
    def clear(self):
        render.clearLight(self.ambient)
        render.clearLight(self.point)
        render.clearLight(self.directional)
    
    def setAmbientLight(self, r, g, b):
        """Adds an ambient light with the given RGB values to the scene."""
        self.ambient.node().setColor(VBase4(r, g, b, 1))
        render.setLight(self.ambient)
    
    def setPointLight(self, r, g, b, x, y, z):
        """Adds a point light with the given RGB values and position to 
        the scene.
        """
        self.point.node().setColor(VBase4(r, g, b, 1))
        self.point.setPos(x, y, z)
        render.setLight(self.point)
    
    def setDirectionalLight(self, r, g, b, head, pitch, roll):
        """Adds a directional light source with the given RGB values and
        orientation.
        """
        self.directional.node().setColor(VBase4(r, g, b, 1))
        self.directional.setHpr(head, pitch, roll)
        render.setLight(self.directional)

