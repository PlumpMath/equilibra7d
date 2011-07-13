# -*- coding: utf-8 -*-
from direct.fsm.FSM import FSM
from panda3d.core import NodePath

from objects import Equismo, Natans, Landscape, Scenario, Sea
import managers
from handlers.keyboard import KeyboardEventHandler

from debug import print_tasks, print_events


class Stage(FSM, KeyboardEventHandler):
    #---------------------------------------------------------------------------
    # This Stage's definitions
    #---------------------------------------------------------------------------
    #NUMBER_OF_NATANS = 20
    
    def __init__(self):
        #-----------------------------------------------------------------------
        # FSM initialization
        #-----------------------------------------------------------------------
        FSM.__init__(self, 'Stage1_FSM')
        self.defaultTransitions = {
            'NewGame': ['Pause', 'GameOver'],
            'InGame': ['Pause', 'GameOver'],
            'Pause': ['InGame'],
            'GameOver': [],
        }
        
        #-----------------------------------------------------------------------
        # KeyboardEventHandler initialization
        #-----------------------------------------------------------------------
        state = dict()
        
        self.bindings = [
            ("escape", lambda: base.reset()),
            ("f2", lambda: base.start()),
            ("f6", lambda: self.managers['collision'].clear()),
            ("f11", lambda: print_events()),
            ("f12", lambda: print_tasks()),
        ]
        
        def toggle(what, key, on, off, default_on=True, show_on_hud=True):
            status_msgs = ("off", "on")
            def toggle_func():
                # Ignore toggle commands when the game is over
                if self.state == "GameOver":
                    return
                if state.setdefault(what, default_on):
                    off()
                else:
                    on()
                print state
                state[what] = not state[what]
                msg = ("<%s %s>" % (what, status_msgs[state[what]])).upper()
                print msg
                if show_on_hud:
                    hudManager = self.managers['hud']
                    ost = hudManager.info(msg)
                    self.doMethodLater(3.0, hudManager.clear_one, 'clear toggle info', [ost])
            self.bindings.append((key, toggle_func))
            return toggle_func
        
        toggle("hud", "f1", lambda: self.managers['hud'].setup(),
                            lambda: self.managers['hud'].clear())
        
        toggle("ai", "f5", lambda: self.objects['enemy'].resume_ai(),
                           lambda: self.objects['enemy'].pause_ai())
        
        toggle("physics", "f7", lambda: self.managers['physics'].setup(),
                                lambda: self.managers['physics'].clear())
        
        toggle("gravity", "f8", lambda: self.managers['physics'].setGravity(9.8),
                                lambda: self.managers['physics'].setGravity(0.0))
        
        toggle("lights", "f9", lambda: self.managers['light'].setup(),
                               lambda: self.managers['light'].clear())
        
        toggle("pause", "p", lambda: (self.pause(), state.setdefault("paused", True)),
                             lambda: (self.pause(), state.pop("paused")),
                             False, False)
    
    #---------------------------------------------------------------------------
    # This Stage's things
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
        
        self.objects['equismo'].clear()
        self.objects['enemy'].clear()
        self.objects.clear()
        
        while self.managers:
            self.managers.popitem()[1].clear()
        
        self.objectsNode.removeNode()
        
        self.removeAllTasks()
    
    def pause(self):
        """Toggle pause the current game."""
        self.request("Pause")
    
    #---------------------------------------------------------------------------
    # Helper methods to setup this Stage
    #---------------------------------------------------------------------------
    def createObjects(self):
        """Instantiate objects."""
        self.objects['scenario'] = Scenario(self.objectsNode, "stage1")
        self.objects['equismo'] = Equismo(self.objectsNode, "equismo")
        self.objects['enemy'] = Natans(self.objectsNode,
                                       ["enemyfish_red",
                                        "enemyfish_green",
                                        "enemyfish_blue"],
                                       self.NUMBER_OF_NATANS)
        self.objects['landscape'] = Landscape(self.objectsNode, "landscape")
        self.objects['sea'] = Sea(self.objectsNode, "sea")
    
    def createManagers(self):
        """Instantiate managers."""
        for kind in "Collision Light HUD Audio Physics".split():
            # Take the *Manager class from the `managers' package
            class_name = "%sManager" % kind
            klass = getattr(managers, class_name)
            
            # Create new Manager. This is similar to
            # self.managers['light'] = managers.LightManager()
            # done for each manager class.
            manager_name = kind.lower()
            self.managers[manager_name] = klass()
    
    #---------------------------------------------------------------------------
    # FSM states
    #---------------------------------------------------------------------------
    @debug(['fsm'])
    def enterNewGame(self):
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
        
        # Display stage name
        ost = self.managers['hud'].show_centered(self.NAME, fg=(1.0, 0.5, 0.0, 1))
        self.doMethodLater(2, self.managers['hud'].clear_one, "clear stage name", [ost])
        
        # Check for a Game Over
        self.addTask(self.handleGameOver, "gameover_task")
    
    @debug(['fsm'])
    def exitNewGame(self):
        pass
    
    @debug(['fsm'])
    def enterInGame(self):
        pass
    
    @debug(['fsm'])
    def exitInGame(self):
        pass
    
    @debug(['fsm'])
    def enterPause(self):
        # Disable some things
        self.managers['physics'].clear()
        self.objects['equismo'].clear()
        self.objects['enemy'].clear()
        
        self.managers['hud'].pause()
    
    @debug(['fsm'])
    def exitPause(self):
        # Re-enable things
        self.managers['physics'].setup()
        self.objects['equismo'].setup()
        self.objects['enemy'].setup()
        
        self.managers['hud'].clear()
        self.managers['hud'].setup()
    
    def filterPause(self, request, args):
        if request == "Pause":
            # Unpause game, go to "InGame"
            return ("InGame",) + args
        else:
            return (request,) + args
    
    @debug(['fsm'])
    def enterGameOver(self, func):
        # Disable some things
        self.managers['physics'].clear()
        self.objects['equismo'].clear()
        self.objects['enemy'].clear()
        
        # Display HUD win/lose
        func()
        
        # Hacky implementation to decide which state to go next
        def next():
            if func.func_name == "win" and self.__class__.__name__ == "Stage1":
                base.gameState.request("Stage2")
            else:
                base.gameState.request("MainMenu")
        
        self.doMethodLater(5, next, "next state after game over", [])
    
    @debug(['fsm'])
    def exitGameOver(self):
        pass
    
    def filterGameOver(self, request, args):
        # No transition allowed after 'GameOver'
        return None
    
    #---------------------------------------------------------------------------
    # Tasks
    #---------------------------------------------------------------------------
    def handleGameOver(self, task):
        """Task that determines whether the game has finished.
        
        When Equismo or the enemy is under water, the state changes to
        GameOver and the HUD shows the winner."""
        #-----------------------------------------------------------------------
        # Check for a defeat
        # You lose the game if you fall from the platform
        #-----------------------------------------------------------------------
        equismo_z = self.objects['equismo'].getBounds().getCenter().getZ()
        if equismo_z < -10:
            self.request("GameOver", self.managers['hud'].lose)
            return task.done
        
        #-----------------------------------------------------------------------
        # Check for a victory
        # You win the game if all enemies are dead
        #-----------------------------------------------------------------------
        def enemy_is_dead(enemy):
            enemy_z = enemy.getBounds().getCenter().getZ()
            return enemy_z < -2
        dead_enemies = len(filter(enemy_is_dead, self.objects['enemy'].enemies))
        enemies_left = self.objects['enemy'].amount - dead_enemies
        
        # We don't want negative enemies left...
        enemies_left = max(enemies_left, 0)
        
        # Update natans left count on HUD
        self.managers['hud'].natans(enemies_left)
        
        if enemies_left == 0:
            self.request("GameOver", self.managers['hud'].win)
            return task.done
        
        return task.cont
