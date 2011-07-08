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
        
        global_bindings = [
            ("escape", sys.exit),
            ("f2", base.reset),
            ("f6", lambda: base.collisionManager.clear()),
            ("f11", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.win())),
            ("f12", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.lose())),
            ("p", base.pause),
        ]
        
        self._state = state = defaultdict(lambda: True)
        
        def toggle(what, key, on, off):
            status_msgs = ("off", "on")
            def toggle_func():
                if state[what]:
                    off()
                else:
                    on()
                state[what] = not state[what]
                print ("<%s %s>" % (what, status_msgs[state[what]])).upper()
            global_bindings.append((key, toggle_func))
            return toggle_func
        
        toggle("hud", "f1", lambda: base.hudManager.setup(),
                            lambda: base.hudManager.clear())
        
        toggle("controls", "f4",
            lambda: [self.addKeyboardEventHandler(handler) for
                        handler in state.get("controls-backup", [])][:0],
            lambda: state.__setitem__("controls-backup", self.clear()))
        
        toggle("ai", "f5", lambda: base.aiManager.setup(),
                           lambda: base.aiManager.clear())
        
        toggle("physics", "f7", lambda: base.physicsManager.setup(),
                                lambda: base.physicsManager.clear())
        
        toggle("gravity", "f8", lambda: base.physicsManager.setGravity(9.8),
                                lambda: base.physicsManager.setGravity(0.0))
        
        toggle("lights", "f9", lambda: base.lightManager.setup(),
                               lambda: base.lightManager.clear())
        
        self.__loadKeyBindings(global_bindings)
    
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

