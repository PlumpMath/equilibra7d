from random import random

from base import Manager


class AudioManager(Manager):
    """Handles game's sound effects and music.
    
    It uses WAV files for sound effects.
    """
    
    SFX_FILE_NAMES = ["water_jumping1", "water_jumping2", "water_jumping3",
                      "water_jumping4", "water_jumping5", "water_jumping6", 
                      "water_jumping7"]
    
    MUSIC_FILE_NAMES = ["MainTheme", "GameOver"]
    
    def __init__(self):
        self.sfxMgr = base.sfxManagerList[0]
        self.musicMgr = base.musicManager
        
        self.sounds = {}
        for fileName in self.SFX_FILE_NAMES:
            self.sounds[fileName] = loader.loadSfx("sfx/%s.wav" % (fileName,))
            
        self.musics = {}
        for fileName in self.MUSIC_FILE_NAMES:
            self.musics[fileName] = loader.loadSfx("music/%s.ogg" % (fileName,))
            
    @debug(['managers'])
    def setup(self):
        pass
    
    @debug(['managers'])
    def clear(self):
        for sfx in self.sounds.itervalues():
            sfx.stop()
        
        for music in self.musics.itervalues():
            music.stop()
    
    def playRandomEffect(self, name, n):
        index = int(random() * n) + 1
        name += str(index)
        
        sound = self.sounds[name]
        sound.play()

    def playMusic(self, name):
        music = self.musics[name]
        music.setLoop(True)
        music.play()
