import sys

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
        self.keyboardEventHandlers = []
        
        def toggle_lights(state=[False]):
            if state[0]:
                status = "on"
                base.lightManager.setup()
            else:
                status = "off"
                base.lightManager.clear()
            state[0] = not state[0]
            print "<Lights %s>" % status.upper()
        
        def toggle_gravity(state=[False]):
            if state[0]:
                status = "on"
                gravity = 9.8
            else:
                status = "off"
                gravity = 0
            base.physicsManager.setGravity(gravity)
            state[0] = not state[0]
            print "<Gravity %s>" % status.upper()
        
        def toggle_controls(state=[False, ()]):
            if state[0]:
                status = "on"
                for handler in state[1]:
                    self.addKeyboardEventHandler(handler)
            else:
                status = "off"
                state[1] = self.clear()
            state[0] = not state[0]
            print "<Controls %s>" % status.upper()
        
        def toggle_ai(state=[False]):
            if state[0]:
                status = "on"
                base.aiManager.setup()
            else:
                status = "off"
                base.aiManager.clear()
            state[0] = not state[0]
            print "<AI %s>" % status.upper()
        
        self.global_bindings = (
            ("escape", sys.exit),
            ("f1",  lambda: (base.hudManager.clear(),
                             base.hudManager.help())),
            ("f2", base.reset),
            ("f4", toggle_controls),
            ("f5", toggle_ai),
            ("f6", lambda: base.collisionManager.clear()),
            ("f7", lambda: base.physicsManager.clear()),
            ("f8", toggle_gravity),
            ("f9", toggle_lights),
            ("f10", lambda: base.hudManager.clear()),
            ("f11", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.win())),
            ("f12", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.lose())),
#            ("pause", base.pause),
        )
        self.loadKeyBindings(self.global_bindings)
    
    def setup(self):
        self.addKeyboardEventHandler(base.character)
    
    def clear(self):
        """Ignore all events registered by all handlers.
        
        Global bindings are kept.
        """
        old_handlers = self.keyboardEventHandlers[:]
        while self.keyboardEventHandlers:
            handler = self.keyboardEventHandlers.pop()
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
        self.keyboardEventHandlers.append(handler)
        self.loadKeyBindings(handler.bindings)

