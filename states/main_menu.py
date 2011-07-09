# -*- coding: utf-8 -*-
import sys

import managers
from handlers.keyboard import KeyboardEventHandler


class MainMenu(KeyboardEventHandler):
    def __init__(self):
        self.bindings = (
            ("escape", sys.exit),
            ("f2", base.reset),
        )
    
    def enter(self):
        self.load_bindings()
        
        # destroy potential trash
        for manager in base.managers:
            manager.clear()
        base.objectsNode.removeChildren()
        # -------------------------
        
        base.hudManager = managers.HUDManager()
        base.hudManager.show_centered(u"F2 para começar")
    
    def exit(self):
        self.unload_bindings()
        
        base.hudManager.clear()

