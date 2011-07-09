# -*- coding: utf-8 -*-
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText

from base import Manager


class HUDManager(Manager):
    def __init__(self):
        self._hud = []
        self._info = None
    
    def setup(self):
        self.help()
    
    def clear(self, ost=None):
        """Remove one or every text from the screen.
        
        If given a OnscreenText, remove it."""
        if ost is None:
            # We could remove everything from `aspect2d', however
            # it's cleaner to just destroy what we have created.
            #aspect2d.removeChildren()
            while self._hud:
                self._hud.pop().destroy()
        else:
            if ost in self._hud:
                self._hud.remove(ost)
            ost.destroy()
    
    def show(self, text, **props):
        """Show text on the screen."""
        ost = OnscreenText(text=text, **props)
        self._hud.append(ost)
        return ost
    
    def show_centered(self, text, **kwargs):
        """Display text centered in the HUD."""
        props = dict(
            pos = (0, +0.5),
            scale = 0.26,
            align = TextNode.ACenter,
            shadow = (0, 0, 0, 1),
        )
        props.update(kwargs)
        self.show(text, **props)
    
    def help(self):
        """Display informative text on HUD."""
        text = u"""\
Comandos:

         W
      A S D   - Movimentar jogador

    <setas> - Movimentar jogador
"""
        commands = (
            ("F2", "Novo jogo"),
            ("P", "Pausar/Continuar"),
            ("F5", "Ligar/Desligar IA"),
            ("Esc", "Sair do jogo"),
        )
        props = dict(
            pos = (-1.1, -0.55),
            scale = 0.07,
            align = TextNode.ALeft,
            fg = (0.8, 0.8, 0.8, 0.4),
            shadow = (0, 0, 0, 1),
        )
        self.show(text, **props)
        
        props.update(
            pos = (0.2, -0.70)
        )
        self.show("\n".join(map(lambda t: t[0], commands)), **props)
        
        props.update(
            pos = (0.42, -0.70)
        )
        self.show("\n".join(map(lambda t: "- %s" % t[1], commands)), **props)
    
    def win(self):
        text = u"Você venceu!"
        self.show_centered(text, fg=(0.3, 1, 0.2, 1))
    
    def lose(self):
        text = u"Você perdeu!"
        self.show_centered(text, fg=(1, 0.3, 0.2, 1))
    
    def pause(self):
        text = u"Pausado"
        self.show_centered(text, fg=(0.8, 0.8, 0.2, 1))
    
    def info(self, msg):
        """Display information in the HUD."""
        props = dict(
            pos = (0, -0.6),
            scale = 0.05,
            align = TextNode.ACenter,
            fg = (0.9, 0.8, 0.4, 1),
            shadow = (0, 0, 0, 1),
        )
        if self._info:
            self.clear(self._info)
        self._info = self.show(msg, **props)
        return self._info

