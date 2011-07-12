import random

from direct.showbase.DirectObject import DirectObject


class AudioHandler(DirectObject):
    """Handles game's sound effects and music."""
    SFX_FILES = []
    
    @debug(['audio'])
    def loadSounds(self):
        self.sounds = dict()
        for filename in self.SFX_FILES:
            self.sounds[filename] = loader.loadSfx("sfx/%s" % (filename,))
    
    @debug(['audio'])
    def playRandomEffect(self):
        if not hasattr(self, "sounds"):
            self.loadSounds()
        sound = random.choice(self.sounds.values())
        sound.play()

