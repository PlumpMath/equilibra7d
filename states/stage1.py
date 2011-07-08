# -*- coding: utf-8 -*-
from objects import Character, Landscape, Scenario, Sea
import managers

class Stage1:
    @staticmethod
    def enter(game_over_handler):
        # (Re)create objects
        Stage1.createObjects()
        
        # (Re)create managers
        Stage1.createManagers()
        
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
    
    @staticmethod
    def createObjects():
        """Instantiate objects.
        
        Can be run multiple times to recreate all objects."""
        # Remove nodes if they already exist.
        base.objectsNode.removeChildren()
        base.scenario = Scenario(base.objectsNode, "arena2")
        base.character = Character(base.objectsNode, "teste")
        base.landscape = Landscape(base.objectsNode, "landscape")
        base.sea = Sea(base.objectsNode, "sea")
    
    @staticmethod
    def createManagers():
        """Instantiate managers.
        
        Can be run multiple times to clear all managers."""
        for kind in "Keyboard Enemy Physics Collision Light HUD AI Audio".split():
            manager_attribute_name = "%sManager" % kind.lower()
            if hasattr(base, manager_attribute_name):
                manager = getattr(base, manager_attribute_name)
                # Clear the manager since it already exists
                manager.clear()
            else:
                # Take the *Manager class from the `managers' package
                class_name = "%sManager" % kind
                klass = getattr(managers, class_name)
                
                # Create new Manager. This is similar to
                # base.keyboardManager = managers.KeyboardManager()
                # done for each manager class.
                setattr(base, manager_attribute_name, klass())

