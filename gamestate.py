from direct.fsm.FSM import FSM

import states.stage1
import states.main_menu


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
        self.defaultTransitions = {
            'MainMenu': ['NewGame'],
            'NewGame': ['MainMenu', 'NewGame', 'Pause', 'GameOver'],
            'InGame': ['MainMenu', 'NewGame', 'Pause', 'GameOver'],
            'Pause': ['MainMenu', 'NewGame', 'InGame'],
            'GameOver': ['MainMenu', 'NewGame'],
        }
        self.currentState = None
    
    def enterMainMenu(self):
        self.currentState = states.main_menu.MainMenu()
        self.currentState.enter()
    
    def exitMainMenu(self):
        self.currentState.exit()
    
    def enterNewGame(self):
        print "enterNewGame"
        self.currentState = states.stage1.Stage1()
        self.currentState.enter(self.handleGameOver)
        self.printTasks()
    
    def exitNewGame(self):
        print "exitNewGame"
        self.currentState.exit()
    
    def enterInGame(self):
        print "enterInGame"
        # Does nothing
    
    def exitInGame(self):
        print "exitInGame"
        # Does nothing
    
    def enterPause(self):
        print "enterPause"
        # Disable some things
        base.aiManager.clear()
        base.physicsManager.clear()
        base.enemyManager.clear()
        base.hudManager.pause()
        
        base.character.unload_bindings()
    
    def exitPause(self):
        print "exitPause"
        # Re-enable things
        base.aiManager.setup()
        base.physicsManager.setup()
        base.enemyManager.setup()
        base.hudManager.clear()
        base.hudManager.setup()
        
        base.character.load_bindings()
    
    def filterPause(self, request, args):
        if request == "Pause":
            # Unpause game, go to "InGame"
            return ("InGame",) + args
        else:
            return (request,) + args
    
    def enterGameOver(self, func):
        print "enterGameOver"
        func()
        # Clear managers
        base.aiManager.clear()
        base.physicsManager.clear()
        base.enemyManager.clear()
        
        base.character.unload_bindings()
    
    def exitGameOver(self):
        print "exitGameOver"
        # Does nothing
    
    def filterGameOver(self, request, args):
        # The only transition allowed from `GameOver' is `NewGame'
        if request == "NewGame":
            return (request,) + args
        else:
            return None
    
    def handleGameOver(self, task):
        """Task that determines whether the gamer has finished.
        
        When the character or the enemy are under water, the state changes to
        GameOver and the HUD shows the winner."""
#        enemy_z = base.enemyManager.enemy.getBounds().getCenter().getZ()
        character_z = base.character.getBounds().getCenter().getZ()
        
#        if enemy_z < -10:
#            self.request("GameOver", base.hudManager.win)
#            return task.done
#        elif character_z < -10:
        if character_z < -10:
            self.request("GameOver", base.hudManager.lose)
            return task.done
        
        return task.cont
    
    def reset(self):
        """Start a new game."""
        self.request("NewGame")
    
    def pause(self):
        """Toggle pause the current game."""
        self.request("Pause")
    
    def printTasks(self):
        print
        print "# tasks"
        _tasks = sorted([t.name for t in taskMgr.getAllTasks()])
        for i, name in enumerate(_tasks, 1):
            c = _tasks.count(name)
            if c > 1:
                if i == _tasks.index(name) + 1:
                    print "%02d. %s [%d]" % (i, name, c)
                else:
                    # don't print anything
                    pass
            else:
                print "%02d. %s" % (i, name)
        print

