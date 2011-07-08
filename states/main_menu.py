# -*- coding: utf-8 -*-
import sys

import managers


class MainMenu:
    @staticmethod
    def enter():
        # destroy potential trash
        
        for manager in base.managers:
            manager.clear()
        base.objectsNode.removeChildren()
        
        # -------------------------
    
        base.keyboardManager = managers.KeyboardManager()
        base.hudManager = managers.HUDManager()
        base.hudManager.show_centered(u"F2 para começar")
        
        #----------------------------------------------------------------------
        state = base.keyboardManager._state
        
        global_bindings = [
            ("escape", sys.exit),
            ("f2", base.reset),
        ]
        
        base.keyboardManager.loadKeyBindings(global_bindings)
    
    @staticmethod
    def exit():
        base.hudManager.clear()
        base.keyboardManager.clear()

