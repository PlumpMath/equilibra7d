class KeyboardEventHandler(object):
    """
    This class must be inherited by all classes interested in handling
    keyboard events.
    After being registered at a InputHandler, its handleKeyboardEvent 
    method will be called every frame.
    This is an abstract class and should not be instantiated.
    """
    def handleKeyboardEvent(self, keys, dt):
        raise NotImplementedError
    
    # Sequence of key bindings of the handler
    bindings = (
    #    (<event>, <function>, <extra-args>),
    )

