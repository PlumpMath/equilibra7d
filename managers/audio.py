from random import random

from base import Manager
from debug import debug


class AudioManager(Manager):
    """Handles game"s sound effects and music.
    
    It uses WAV files for sound effects.
    """
    
    SFX_FILE_NAMES = ["water_jumping1", "water_jumping2", "water_jumping3",
                      "water_jumping4", "water_jumping5", "water_jumping6", 
                      "water_jumping7"]
    
    def __init__(self):
        self.musicMgr = base.musicManager
        self.sfxMgr = base.sfxManagerList[0]
        
        self.sounds = {}
        for fileName in self.SFX_FILE_NAMES:
            self.sounds[fileName] = loader.loadSfx("sfx/%s.wav" % (fileName,))
    
    @debug(['managers'])
    def setup(self):
        pass
    
    @debug(['managers'])
    def clear(self):
        pass
    
    def playRandomEffect(self, name, n):
        index = int(random() * n) + 1
        name += str(index)
        
        sound = self.sounds[name]
        sound.play()
