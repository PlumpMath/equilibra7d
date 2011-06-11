import sys


class KeyboardManager():
    """Manages the input events from Panda3D.
    
    In this class, all the accepted keys are registered and a task is
    defined in order to handle the input events, like a key press.
    
    All classes interested in handling keyboard events must inherit
    from the 'KeyboardEventHandler' class and must be registered
    through the 'addKeyboardEventHandler' method.
    """
    
    def __init__(self, world):
        """All accepted keys are defined here."""
        self.keys = {"left":0, "right":0, "up":0, "down":0}
        
        world.accept("w", self._setKey, ["up", 1])
        world.accept("a", self._setKey, ["left", 1])
        world.accept("s", self._setKey, ["down", 1])
        world.accept("d", self._setKey, ["right", 1])

        world.accept("w-up", self._setKey, ["up", 0])
        world.accept("a-up", self._setKey, ["left", 0])
        world.accept("s-up", self._setKey, ["down", 0])
        world.accept("d-up", self._setKey, ["right", 0])
        
        world.accept("arrow_up", self._setKey, ["up", 1])
        world.accept("arrow_left", self._setKey, ["left", 1])
        world.accept("arrow_down", self._setKey, ["down", 1])
        world.accept("arrow_right", self._setKey, ["right", 1])

        world.accept("arrow_up-up", self._setKey, ["up", 0])
        world.accept("arrow_left-up", self._setKey, ["left", 0])
        world.accept("arrow_down-up", self._setKey, ["down", 0])
        world.accept("arrow_right-up", self._setKey, ["right", 0])
        
        # Handle it differently when the user keeps pressing a key (acceleration)
        #world.accept("d-repeat", self.p, ["repeating D"])
        
        world.accept("n", world.reset)
        world.accept("escape", sys.exit)
        
        world.accept("f12", lambda: world.enemy.actor.setZ(-100))
        
        world.taskMgr.add(self.handleInput, "input_task")

        self.keyboardEventHandlers = []
        self.world = world
        
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

