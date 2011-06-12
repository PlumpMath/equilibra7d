from time import sleep

from direct.fsm.FSM import FSM


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
    
    def enterNewGame(self):
        print "enterNewGame"
        # Set up objects
        base.character.setup()
        base.enemy.setup()
        base.landscape.setup()
        base.scenario.setup()
        base.sea.setup()
        
        # Set up managers
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
        
    def enterGameOver(self, func):
        print "enterGameOver"
        func()
        
    def exitGameOver(self):
        print "exitGameOver"
        base.hudManager.clear()
    
    def handleGameOver(self, task):
        enemy_z = base.enemy.getBounds().getCenter().getZ()
        character_z = base.character.getBounds().getCenter().getZ()
    
        if enemy_z < -10:
            self.request("GameOver", base.hudManager.win)
            return task.done
        elif character_z < -10:
            self.request("GameOver", base.hudManager.lose)
            return task.done
        
        return task.cont
    
    def reset(self):
        """Set the initial position of things defined in the world."""
        print "restarting..."
        self.request("NewGame")

