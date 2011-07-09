# -*- coding: utf-8 -*-
from objects import Character, Landscape, Scenario, Sea
import managers
from handlers.keyboard import KeyboardEventHandler


class Stage1(KeyboardEventHandler):
    def __init__(self):
        state = dict()
        
        self.bindings = [
            ("escape", lambda: base.gameState.request("MainMenu")),
            ("f2", base.reset),
            ("f6", lambda: base.collisionManager.clear()),
            ("f11", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.win())),
            ("f12", lambda: (base.hudManager.clear(),
                             base.hudManager.help(),
                             base.hudManager.lose())),
        ]
        
        def toggle(what, key, on, off, default_on=True):
            status_msgs = ("off", "on")
            def toggle_func():
                if state.setdefault(what, default_on):
                    off()
                else:
                    on()
                print state
                state[what] = not state[what]
                msg = ("<%s %s>" % (what, status_msgs[state[what]])).upper()
                print msg
                base.hudManager.info(msg)
            self.bindings.append((key, toggle_func))
            return toggle_func
        
        toggle("hud", "f1", lambda: base.hudManager.setup(),
                            lambda: base.hudManager.clear())
        
        toggle("ai", "f5", lambda: base.aiManager.setup(),
                           lambda: base.aiManager.clear())
        
        toggle("physics", "f7", lambda: base.physicsManager.setup(),
                                lambda: base.physicsManager.clear())
        
        toggle("gravity", "f8", lambda: base.physicsManager.setGravity(9.8),
                                lambda: base.physicsManager.setGravity(0.0))
        
        toggle("lights", "f9", lambda: base.lightManager.setup(),
                               lambda: base.lightManager.clear())
       
        toggle("pause", "p", lambda: (base.pause(), state.setdefault("paused", True)),
                             lambda: (base.pause(), state.pop("paused")),
                             False)
    
    def enter(self, game_over_handler):
        self.load_bindings()
        
        # (Re)create objects
        self.createObjects()
        
        # (Re)create managers
        self.createManagers()
        
        # Set up objects
        base.character.setup()
        base.landscape.setup()
        base.scenario.setup()
        base.sea.setup()
        
        # Set up managers
        base.enemyManager.setup()
        base.physicsManager.setup()
        base.collisionManager.setup()
        base.lightManager.setup()
        base.hudManager.setup()
        base.aiManager.setup()
        base.audioManager.setup()
        
        # Check for a Game Over
        # TODO: use self.addTask here
        task_name = "gameover_task"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(game_over_handler, task_name)
    
    def exit(self):
        self.unload_bindings()
    
    def createObjects(self):
        """Instantiate objects.
        
        Can be run multiple times to recreate all objects."""
        # Remove nodes if they already exist.
        base.objectsNode.removeChildren()
        base.scenario = Scenario(base.objectsNode, "arena2")
        base.character = Character(base.objectsNode, "teste")
        base.landscape = Landscape(base.objectsNode, "landscape")
        base.sea = Sea(base.objectsNode, "sea")
    
    def createManagers(self):
        """Instantiate managers.
        
        Can be run multiple times to clear all managers."""
        for kind in "Enemy Physics Collision Light HUD AI Audio".split():
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
                # base.lightManager = managers.LightManager()
                # done for each manager class.
                manager = klass()
                setattr(base, manager_attribute_name, manager)
            base.managers.add(manager)

