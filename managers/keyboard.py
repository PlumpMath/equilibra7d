import sys

from manager import Manager


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
        
        def toggle_lights(m=[0]):
            getattr(base.lightManager, "setDefaultLights" if m[0] % 2 else "clear")()
            m[0] = (m[0] + 1) % 2
        
        def toggle_gravity(m=[0]):
            gravity = 9.8 if m[0] % 2 else 0
            base.physicsManager.setGravity(gravity)
            print "gravity = %s" % gravity
            m[0] = (m[0] + 1) % 2
        
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
        
        self.global_bindings = (
            ("n", base.reset),
            ("escape", sys.exit),
            ("f1",  lambda: (base.hudManager.clear(),
                             base.hudManager.help())),
            ("f4", toggle_controls),
            ("f5", lambda: base.aiManager.clear()),
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
        )
        self.loadKeyBindings(self.global_bindings)
    
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

