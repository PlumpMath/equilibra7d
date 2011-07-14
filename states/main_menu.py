# -*- coding: utf-8 -*-
import sys

import managers
from handlers.keyboard import KeyboardEventHandler


class MainMenu(KeyboardEventHandler):
    def __init__(self):
        self._msg = None
        self.bindings = (
            ("escape", sys.exit),
            ("f2", base.start),
        )
    
    def enter(self):
        self.load_bindings()
        
        self.hud = managers.HUDManager()
        img_props = dict(
            pos = (0, 0, 0),
            scale = (1.34, 1, 1.1),
        )
        self.hud.show_image("concept/screen_presenting_v2.png", **img_props)
        self.doMethodLater(0.3, self.blink, "blink msg")
        
        # Play music
        self.audio = managers.AudioManager()
        self.audio.playMusic("Menu")
    
    def exit(self):
        self.unload_bindings()
        self.removeAllTasks()
        self.hud.clear()
        self.audio.clear()
    
    def blink(self, task):
        if self._msg:
            self.hud.clear_one(self._msg)
            self._msg = None
            task.delayTime = 0.4
        else:
            self._msg = self.hud.show_centered(u"Aperte F2 para jogar",
                                               fg=(1.0, 0.5, 0.0, 1),
                                               pos=(0, -0.87),
                                               scale=0.18)
            task.delayTime = 0.6
        return task.again

