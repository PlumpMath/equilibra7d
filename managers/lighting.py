from panda3d.core import AmbientLight, DirectionalLight, PointLight, VBase4


class LightingManager:
    """Handles the lighting of the 3D scene."""
    
    def __init__(self, **lights):
        self.ambientLight = None
        self.pointLight = None
        self.directionalLight = None
        
        default = dict(
            ambient = (0.3, 0.3, 0.3),
            point = (0.4, 0.4, 0.4, 0, -8, 5),
            directional = (0.4, 0.4, 0.6, 0, -60, 0),
        )
        default.update(lights)
        self.setLights(**default)
    
    def setLights(self, **lights):
        ambient, point, directional = map(lights.get, "ambient point directional".split())
        if ambient is not None:
            self.setAmbientLight(*ambient)
        if point is not None:
            self.setPointLight(*point)
        if directional is not None:
            self.setDirectionalLight(*directional)
    
    def setAmbientLight(self, r, g, b):
        """Adds an ambient light with the given RGB values to the scene."""
        ambientLightNode = AmbientLight('ambient_light')
        ambientLightNode.setColor(VBase4(r, g, b, 1))
        
        self.ambientLight = render.attachNewNode(ambientLightNode)
        render.setLight(self.ambientLight)
    
    def setPointLight(self, r, g, b, x, y, z):
        """Adds a point light with the given RGB values and position to 
        the scene.
        """
        pointLightNode = PointLight('point_light')
        pointLightNode.setColor(VBase4(r, g, b, 1))
        
        self.pointLight = render.attachNewNode(pointLightNode)
        self.pointLight.setPos(x, y, z)
        render.setLight(self.pointLight)
    
    def setDirectionalLight(self, r, g, b, head, pitch, roll):
        """Adds a directional light source with the given RGB values and
        orientation.
        """
        directionalLightNode = DirectionalLight('directional_light')
        directionalLightNode.setColor(VBase4(r, g, b, 1))
        
        self.directionalLight = render.attachNewNode(directionalLightNode)
        self.directionalLight.setHpr(head, pitch, roll)
        render.setLight(self.directionalLight)

