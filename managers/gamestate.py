from time import sleep

from direct.fsm.FSM import FSM


class GameStateManager(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
        taskMgr.add(self.handleGameOver, "gameover_task")
    
    def enterNewGame(self):
        print "enterNewGame"
        
    def exitNewGame(self):
        print "exitNewGame"
        
    def enterGameOver(self):
        print "enterGameOver"
        
    def exitGameOver(self):
        print "exitGameOver"
    
    def handleGameOver(self, task):
        enemy_z = base.enemy.getBounds().getCenter().getZ()
        character_z = base.character.getBounds().getCenter().getZ()
        
        hudManager = base.hudManager
    
        if enemy_z < -10:
            self.request("GameOver")
            hudManager.win()
            return task.done
        elif character_z < -10:
            self.request("GameOver")
            hudManager.lose()
            return task.done
            
        # reset the game after some time / keypress ...
        # NotImplemented
        
        return task.cont
    
    def reset(self):
        """Set the initial position of things defined in the world."""
        print "restarting..."
        base._removeFeatures()
        base.initFeatures()
        
        # Reset keyboardManager
        #self.keyboardManager.reset()

