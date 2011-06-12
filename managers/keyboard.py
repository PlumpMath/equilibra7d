import sys


class KeyboardManager():
    """Manages the input events from Panda3D.
    
    In this class, all the accepted keys are registered and a task is
    defined in order to handle the input events, like a key press.
    
    All classes interested in handling keyboard events must inherit
    from the 'KeyboardEventHandler' class and must be registered
    through the 'addKeyboardEventHandler' method.
    """
    
    def __init__(self):
        """All accepted keys are defined here."""
        self.keys = {"left":0, "right":0, "up":0, "down":0}
        
        base.accept("w", self._setKey, ["up", 1])
        base.accept("a", self._setKey, ["left", 1])
        base.accept("s", self._setKey, ["down", 1])
        base.accept("d", self._setKey, ["right", 1])

        base.accept("w-up", self._setKey, ["up", 0])
        base.accept("a-up", self._setKey, ["left", 0])
        base.accept("s-up", self._setKey, ["down", 0])
        base.accept("d-up", self._setKey, ["right", 0])
        
        base.accept("arrow_up", self._setKey, ["up", 1])
        base.accept("arrow_left", self._setKey, ["left", 1])
        base.accept("arrow_down", self._setKey, ["down", 1])
        base.accept("arrow_right", self._setKey, ["right", 1])

        base.accept("arrow_up-up", self._setKey, ["up", 0])
        base.accept("arrow_left-up", self._setKey, ["left", 0])
        base.accept("arrow_down-up", self._setKey, ["down", 0])
        base.accept("arrow_right-up", self._setKey, ["right", 0])
        
        # Handle it differently when the user keeps pressing a key (acceleration)
        #base.accept("d-repeat", self.p, ["repeating D"])
        
        base.accept("n", base.reset)
        base.accept("escape", sys.exit)
        
        base.accept("f1",  lambda: (base.hudManager.clear(),
                                    base.hudManager.help()))
        base.accept("f10", lambda: base.hudManager.clear())
        base.accept("f11", lambda: (base.hudManager.clear(),
                                    base.hudManager.help(),
                                    base.hudManager.win()))
        base.accept("f12", lambda: (base.hudManager.clear(),
                                    base.hudManager.help(),
                                    base.hudManager.lose()))
        def toogle_lights(m=[0]):
            getattr(base.lightManager, "setDefaultLights" if m[0] % 2 else "clear")()
            m[0] = (m[0] + 1) % 2
        base.accept("f9", toogle_lights)
        
        def toogle_gravity(m=[0]):
            gravity = 9.8 if m[0] % 2 else 0
            base.physicsManager.setGravity(gravity)
            print "gravity = %s" % gravity
            m[0] = (m[0] + 1) % 2
        base.accept("f8", toogle_gravity)
        base.accept("f7", lambda: base.physicsManager.clear())
        base.accept("f6", lambda: base.collisionManager.clear())
        
        taskMgr.add(self.handleInput, "input_task")

        self.keyboardEventHandlers = []
        
    def addKeyboardEventHandler(self, handler):
        """Registers a keyboard event handler.
        
        The given object must inherit from the KeyboardEventHandler 
        class. Its 'handleKeyboardEvent' method will be called at each 
        frame.
        """
        self.keyboardEventHandlers.append(handler)
    
    def handleInput(self, task):
        """Calls the 'handleKeyboardEvent' method from every registered 
        keyboard event handler.
        
        This method is associated with the 'input_task' task and is 
        therefore called on every frame.
        """
        dt = globalClock.getDt()
        
        for handler in self.keyboardEventHandlers:
            handler.handleKeyboardEvent(self.keys, dt)
        
        return task.cont
            
    def _setKey(self, key, value):
        self.keys[key] = value

