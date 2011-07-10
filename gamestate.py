from direct.fsm.FSM import FSM

from debug import debug
import states.stage1
import states.main_menu


class GameState(FSM):
    """This is the main FSM to control game state."""
    
    def __init__(self):
        FSM.__init__(self, 'Equilibra7d_FSM')
        self.defaultTransitions = {
            'MainMenu': ['Stage1'],
            'Stage1': ['MainMenu', 'Stage1'],
        }
        self.currentState = None
    
    @debug(['fsm'])
    def enterMainMenu(self):
        self.currentState = states.main_menu.MainMenu()
        self.currentState.enter()
    
    @debug(['fsm'])
    def exitMainMenu(self):
        self.currentState.exit()
    
    @debug(['fsm'])
    def enterStage1(self):
        self.currentState = states.stage1.Stage1()
        self.currentState.enter()
    
    @debug(['fsm'])
    def exitStage1(self):
        self.currentState.exit()
    
    def reset(self):
        """Return to main menu."""
        self.request("MainMenu")
    
    def start(self):
        """Start a new game."""
        self.request("Stage1")

