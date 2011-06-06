from panda3d.core import AmbientLight, DirectionalLight, PointLight, VBase4


class LightingManager:
    """Handles the lighting of the 3D scene."""
    
    def __init__(self, world):
        self.render = world.render
        
    def setAmbientLight(self, r, g, b):
        """Adds an ambient light with the given RGB values to the scene."""
        ambientLightNode = AmbientLight('ambient_light')
        ambientLightNode.setColor(VBase4(r, g, b, 1))
        
        self.ambientLight = self.render.attachNewNode(ambientLightNode)
        self.render.setLight(self.ambientLight)

    def setPointLight(self, r, g, b, x, y, z):
        """Adds a point light with the given RGB values and position to 
        the scene.
        """
        pointLightNode = PointLight('point_light')
        pointLightNode.setColor(VBase4(r, g, b, 1))

        self.pointLight = self.render.attachNewNode(pointLightNode)
        self.pointLight.setPos(x, y, z)
        self.render.setLight(self.pointLight)
    
    def setDirectionalLight(self, r, g, b, head, pitch, roll):
        """Adds a directional light source with the given RGB values and
        orientation.
        """
        directionalLightNode = DirectionalLight('directional_light')
        directionalLightNode.setColor(VBase4(r, g, b, 1))
        
        self.directionalLight = self.render.attachNewNode(directionalLightNode)
        self.directionalLight.setHpr(head, pitch, roll)
        self.render.setLight(self.directionalLight)

