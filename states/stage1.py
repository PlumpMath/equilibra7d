class Stage1:
    @staticmethod
    def enter(game_over_handler):
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
        base.audioManager.setup()
        
        # Check for a Game Over
        task_name = "gameover_task"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(game_over_handler, task_name)
    
    @staticmethod
    def exit():
        pass
