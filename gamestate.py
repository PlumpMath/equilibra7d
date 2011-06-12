from time import sleep

from direct.fsm.FSM import FSM


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
    
    def enterNewGame(self):
        print "enterNewGame"
        base.keyboardManager.setup()
        base.physicsManager.setup()
        base.collisionManager.setup()
        base.lightManager.setup()
        base.hudManager.setup()
        base.aiManager.setup()
        
        # Check for a Game Over
        taskMgr.add(self.handleGameOver, "gameover_task")
        
    def exitNewGame(self):
        print "exitNewGame"
        base.keyboardManager.clear()
        base.physicsManager.clear()
        base.collisionManager.clear()
        #base.lightManager.clear()
        #base.hudManager.clear()
        base.aiManager.clear()
        
    def enterGameOver(self):
        print "enterGameOver"
        
    def exitGameOver(self):
        print "exitGameOver"
        base.hudManager.clear()
    
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
        
        return task.cont
    
    def reset(self):
        """Set the initial position of things defined in the world."""
        print "restarting..."
        base._removeFeatures()
        base.initFeatures()
        
        self.request("NewGame")

