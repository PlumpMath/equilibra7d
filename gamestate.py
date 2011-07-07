from time import sleep

from direct.fsm.FSM import FSM


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'EquilibraFSM')
        self.defaultTransitions = {
            'NewGame': ['NewGame', 'Pause', 'GameOver'],
            'InGame': ['NewGame', 'Pause', 'GameOver'],
            'Pause': ['NewGame', 'InGame'],
            'GameOver': ['NewGame'],
        }
    
    def enterNewGame(self):
        print "enterNewGame"
        # (Re)create objects
        base.createObjects()
        
        # (Re)create managers
        base.createManagers()
        
        # Set up objects
        base.character.setup()
        base.landscape.setup()
        base.scenario.setup()
        base.sea.setup()
        
        # Set up managers
        base.keyboardManager.setup()
        base.enemyManager.setup()
        base.physicsManager.setup()
        base.collisionManager.setup()
        base.lightManager.setup()
        base.hudManager.setup()
        base.aiManager.setup()
        
        # Check for a Game Over
        task_name = "gameover_task"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(self.handleGameOver, task_name)
        
        self.printTasks()
    
    def exitNewGame(self):
        print "exitNewGame"
        # Does nothing
    
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
        self._kb_handlers = base.keyboardManager.clear()
        base.physicsManager.clear()
        base.hudManager.pause()
    
    def exitPause(self):
        print "exitPause"
        # Re-enable things
        base.aiManager.setup()
        for handler in self._kb_handlers:
            base.keyboardManager.addKeyboardEventHandler(handler)
        base.physicsManager.setup()
        base.hudManager.clear()
        base.hudManager.setup()
    
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
        base.keyboardManager.clear()
        base.physicsManager.clear()
    
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

