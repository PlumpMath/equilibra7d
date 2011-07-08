from base import Manager


class KeyboardManager(Manager):
    """Manages the input events from Panda3D.
    
    In this class, all the accepted keys are registered and a task is
    defined in order to handle the input events, like a key press.
    
    All classes interested in handling keyboard events must inherit
    from the 'KeyboardEventHandler' class and must be registered
    through the 'addKeyboardEventHandler' method.
    """
    
    def __init__(self):
        """All accepted keys are defined here."""
        self._keyboardEventHandlers = []
        self._state = dict()
    
    def setup(self):
        self.addKeyboardEventHandler(base.character)
    
    def clear(self):
        """Ignore all events registered by all handlers.
        
        Global bindings are kept.
        """
        # Clear the state used in toggle functions
        if self._state.has_key("pause"):
            self._state = dict(pause=self._state["pause"])
        else:
            self._state.clear()
        # Remove registered keyboard handlers
        old_handlers = self._keyboardEventHandlers[:]
        while self._keyboardEventHandlers:
            handler = self._keyboardEventHandlers.pop()
            for binding in handler.bindings:
                base.ignore(binding[0])
        return old_handlers
    
    def loadKeyBindings(self, bindings):
        for binding in bindings:
            base.accept(*binding)
    
    def addKeyboardEventHandler(self, handler):
        """Registers a keyboard event handler.
        
        The given object must inherit from the KeyboardEventHandler 
        class. Its 'handleKeyboardEvent' method will be called at each 
        frame.
        """
        self._keyboardEventHandlers.append(handler)
        self.loadKeyBindings(handler.bindings)

