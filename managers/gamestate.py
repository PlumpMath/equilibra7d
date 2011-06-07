from direct.fsm.FSM import FSM


class GameStateManager(FSM):
    def __init__(self, world):
        FSM.__init__(self, 'EquilibraFSM')
        
        self.world = world
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
        world = self.world
        enemy_z = world.enemy.getBounds().getCenter().getZ()
        character_z = world.character.getBounds().getCenter().getZ()
        
        hudManager = world.hudManager
    
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
        world = self.world
        world._removeFeatures()
        world.initFeatures()
        
        # Reset keyboardManager
        #self.keyboardManager.reset()

