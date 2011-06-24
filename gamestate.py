from time import sleep

from direct.fsm.FSM import FSM


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
#        self.defaultTransitions = {
#            'NewGame': ['NewGame', 'InGame', 'Pause', 'GameOver'],
#            'InGame': ['NewGame', 'Pause', 'GameOver'],
#            'Pause': ['NewGame', 'InGame'],
#            'GameOver': ['NewGame'],
#        }
    
    def enterNewGame(self):
        print "enterNewGame"
        # (Re)create objects
        base.createObjects()
        
        # (Re)create managers
        base.createManagers()
        
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
        # Clear managers
        base.keyboardManager.clear()
        base.physicsManager.clear()
        base.collisionManager.clear()
        #base.lightManager.clear()
        #base.hudManager.clear()
        base.aiManager.clear()
    
#    def enterInGame(self):
#        print "enterInGame"
#    
#    def exitInGame(self):
#        print "exitInGame"
#    
#    def enterPause(self):
#        print "enterPause"
#    
#    def exitPause(self):
#        print "exitPause"
    
    def enterGameOver(self, func):
        print "enterGameOver"
        func()
    
    def exitGameOver(self):
        print "exitGameOver"
    
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
        self.request("NewGame")
    
#    def pause(self):
#        self.request("Pause")

