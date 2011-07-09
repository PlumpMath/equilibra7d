# -*- coding: utf-8 -*-
from direct.fsm.FSM import FSM
from panda3d.core import NodePath

from objects import Character, Landscape, Scenario, Sea
import managers
from handlers.keyboard import KeyboardEventHandler


class Stage1(FSM, KeyboardEventHandler):
    def __init__(self):
        #-----------------------------------------------------------------------
        # FSM initialization
        #-----------------------------------------------------------------------
        FSM.__init__(self, 'Stage1_FSM')
        self.defaultTransitions = {
            'NewGame': ['NewGame', 'Pause', 'GameOver'],
            'InGame': ['NewGame', 'Pause', 'GameOver'],
            'Pause': ['NewGame', 'InGame'],
            'GameOver': ['NewGame'],
        }
        
        #-----------------------------------------------------------------------
        # KeyboardEventHandler initialization
        #-----------------------------------------------------------------------
        state = dict()
        
        self.bindings = [
            ("escape", lambda: base.reset()),
            ("f2", lambda: base.start()),
            ("f6", lambda: self.managers['collision'].clear()),
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
                self.managers['hud'].info(msg)
            self.bindings.append((key, toggle_func))
            return toggle_func
        
        toggle("hud", "f1", lambda: self.managers['hud'].setup(),
                            lambda: self.managers['hud'].clear())
        
        toggle("ai", "f5", lambda: self.managers['ai'].setup(),
                           lambda: self.managers['ai'].clear())
        
        toggle("physics", "f7", lambda: self.managers['physics'].setup(),
                                lambda: self.managers['physics'].clear())
        
        toggle("gravity", "f8", lambda: self.managers['physics'].setGravity(9.8),
                                lambda: self.managers['physics'].setGravity(0.0))
        
        toggle("lights", "f9", lambda: self.managers['light'].setup(),
                               lambda: self.managers['light'].clear())
        
        toggle("pause", "p", lambda: (self.pause(), state.setdefault("paused", True)),
                             lambda: (self.pause(), state.pop("paused")),
                             False)
    
    #---------------------------------------------------------------------------
    # This stage's things
    #---------------------------------------------------------------------------
    def enter(self):
        self.load_bindings()
        
        # Create parent for all objects
        self.objectsNode = NodePath("objects")
        self.objectsNode.reparentTo(render)
        
        self.objects = dict()
        
        self.managers = dict()
        
        self.request("NewGame")
    
    def exit(self):
        self.unload_bindings()
        
        self.objects.clear()
        
        while self.managers:
            self.managers.popitem()[1].clear()
        
        self.objectsNode.removeNode()
    
    #---------------------------------------------------------------------------
    # Helper functions to setup this Stage
    #---------------------------------------------------------------------------
    def createObjects(self):
        """Instantiate objects."""
        self.objects['scenario'] = Scenario(self.objectsNode, "arena2")
        self.objects['character'] = Character(self.objectsNode, "teste")
        self.objects['landscape'] = Landscape(self.objectsNode, "landscape")
        self.objects['sea'] = Sea(self.objectsNode, "sea")
    
    def createManagers(self):
        """Instantiate managers."""
        for kind in "Enemy Physics Collision Light HUD AI Audio".split():
            # Take the *Manager class from the `managers' package
            class_name = "%sManager" % kind
            klass = getattr(managers, class_name)
            
            # Create new Manager. This is similar to
            # self.managers['light'] = managers.LightManager()
            # done for each manager class.
            manager_name = kind.lower()
            self.managers[manager_name] = klass()
    
    #-----------------------------------------------------------------------
    # FSM states
    #-----------------------------------------------------------------------
    def enterNewGame(self):
        print "enterNewGame"
        # Create objects
        self.createObjects()
        
        # Create managers
        self.createManagers()
        
        # Set up objects
        for obj in self.objects.itervalues():
            obj.setup()
        
        # Set up managers
        for mgr in self.managers.itervalues():
            mgr.setup()
        
        # Check for a Game Over
        # TODO: use self.addTask here
        # TODO: remove "gameover_task" when appropriate
        task_name = "gameover_task"
        if taskMgr.hasTaskNamed(task_name):
            taskMgr.remove(task_name)
        taskMgr.add(self.handleGameOver, task_name)
    
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
        self.managers['ai'].clear()
        self.managers['physics'].clear()
        self.managers['enemy'].clear()
        self.managers['hud'].pause()
        
        self.objects['character'].unload_bindings()
    
    def exitPause(self):
        print "exitPause"
        # Re-enable things
        self.managers['ai'].setup()
        self.managers['physics'].setup()
        self.managers['enemy'].setup()
        self.managers['hud'].clear()
        self.managers['hud'].setup()
        
        self.objects['character'].load_bindings()
    
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
        self.managers['ai'].clear()
        self.managers['physics'].clear()
        self.managers['enemy'].clear()
        
        self.objects['character'].unload_bindings()
    
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
#        enemy_z = self.objects['enemy'].getBounds().getCenter().getZ()
        character_z = self.objects['character'].getBounds().getCenter().getZ()
        
#        if enemy_z < -10:
#            self.request("GameOver", self.managers['hud'].win)
#            return task.done
#        elif character_z < -10:
        if character_z < -10:
            self.request("GameOver", self.managers['hud'].lose)
            return task.done
        
        return task.cont
    
    def pause(self):
        """Toggle pause the current game."""
        self.request("Pause")

