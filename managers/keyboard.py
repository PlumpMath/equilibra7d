from collections import defaultdict
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
        self._keyboardEventHandlers = []
        
        self._state = state = defaultdict(lambda: True)
        status_msgs = ("off", "on")
        
        def toggle_lights():
            if state["lights"]:
                base.lightManager.clear()
            else:
                base.lightManager.setup()
            state["lights"] = not state["lights"]
            print "<Lights %s>" % status_msgs[state["lights"]].upper()
        
        def toggle_gravity():
            if state["gravity"]:
                gravity = 0
            else:
                gravity = 9.8
            base.physicsManager.setGravity(gravity)
            state["gravity"] = not state["gravity"]
            print "<Gravity %s>" % status_msgs[state["gravity"]].upper()
        
        def toggle_controls():
            if state["controls"]:
                state["controls-backup"] = self.clear()
            else:
                for handler in state["controls-backup"]:
                    self.addKeyboardEventHandler(handler)
            state["controls"] = not state["controls"]
            print "<Controls %s>" % status_msgs[state["controls"]].upper()
        
        def toggle_ai():
            if state["ai"]:
                base.aiManager.clear()
            else:
                base.aiManager.setup()
            state["ai"] = not state["ai"]
            print "<AI %s>" % status_msgs[state["ai"]].upper()
        
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
            ("pause", base.pause),
        )
        self.__loadKeyBindings(self.global_bindings)
    
    def setup(self):
        self.addKeyboardEventHandler(base.character)
    
    def clear(self):
        """Ignore all events registered by all handlers.
        
        Global bindings are kept.
        """
        # Clear the state used in toggle functions
        self._state.clear()
        # Remove registered keyboard handlers
        old_handlers = self._keyboardEventHandlers[:]
        while self._keyboardEventHandlers:
            handler = self._keyboardEventHandlers.pop()
            for binding in handler.bindings:
                base.ignore(binding[0])
        return old_handlers
    
    def __loadKeyBindings(self, bindings):
        for binding in bindings:
            base.accept(*binding)
    
    def addKeyboardEventHandler(self, handler):
        """Registers a keyboard event handler.
        
        The given object must inherit from the KeyboardEventHandler 
        class. Its 'handleKeyboardEvent' method will be called at each 
        frame.
        """
        self._keyboardEventHandlers.append(handler)
        self.__loadKeyBindings(handler.bindings)

