# -*- coding: utf-8 -*-
import managers


class MainMenu:
    @staticmethod
    def enter():
        base.keyboardManager = managers.KeyboardManager()
        base.hudManager = managers.HUDManager()
        base.hudManager.show_centered(u"F2 para começar")
    
    @staticmethod
    def exit():
        base.hudManager.clear()
        base.keyboardManager.clear()

