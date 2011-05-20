from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText


class HUDManager():
    def __init__(self):
        text = """\
Comandos:
    WASD - Movimentar jogador
    ESC - Exit
"""
        pos = (-1, -0.6)
        scale = 0.06
        align = TextNode.ALeft
        fg = (1, 1, 1, 1)
        
        textNode = OnscreenText(text=text, pos=pos, scale=scale, 
                                align=align, fg=fg)

