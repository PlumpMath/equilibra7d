from direct.showbase.DirectObject import DirectObject


class KeyboardEventHandler(DirectObject):
    """Mixin for classes interested in handling keyboard events.
    
    Remember to call `self.load_bindings()' and `self.unload_bindings()' when
    appropriate."""
    
    # Sequence of key bindings of the handler
    bindings = (
    #    (<event>, <function>, <extra-args>),
    )
    
    def load_bindings(self):
        """Registers all key bindings."""
        for binding in self.bindings:
            self.accept(*binding)
    
    def unload_bindings(self):
        """Ignores all key bindings."""
        self.ignoreAll()

