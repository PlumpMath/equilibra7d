# -*- coding: utf-8 -*-
import sys

import managers
from handlers.keyboard import KeyboardEventHandler


class MainMenu(KeyboardEventHandler):
    def __init__(self):
        self.bindings = (
            ("escape", sys.exit),
            ("f2", base.start),
        )
    
    def enter(self):
        self.load_bindings()
        
        self.hudManager = managers.HUDManager()
        self.hudManager.show_centered(u"F2 para começar")
    
    def exit(self):
        self.unload_bindings()
        
        self.hudManager.clear()

