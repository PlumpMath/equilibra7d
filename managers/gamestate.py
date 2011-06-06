class GameStateManager:
    def __init__(self, world):
        self.world = world
        taskMgr.add(self.handleGameOver, "gameover_task")

    def handleGameOver(self, task):
        world = self.world
        enemy_z = world.enemy.getBounds().getCenter().getZ()
        character_z = world.character.getBounds().getCenter().getZ()
        
        hudManager = world.hudManager
    
        if enemy_z < -10:
            hudManager.win()
            return task.done
        elif character_z < -10:
            hudManager.lose()
            return task.done
            
        # reset the game after some time / keypress ...
        # NotImplemented
        
        return task.cont
