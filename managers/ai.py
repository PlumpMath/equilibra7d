from panda3d.ai import AIWorld, AICharacter

from manager import Manager


class AIManager(Manager):
    def __init__(self):
        # Creating AI World
        self.aiWorld = AIWorld(render)
        self.aiChar = AICharacter("seeker", base.enemy.actor, 100, 0.05, 1.0)
        self.setup()
        
    def setup(self):
        self.aiWorld.addAiChar(self.aiChar)
        aiBehaviors = self.aiChar.getAiBehaviors()
        aiBehaviors.pursue(base.character.actor)
        taskMgr.add(self.update, "AIUpdate")
        
    def update(self, task):
        """Update the AI World"""
        self.aiWorld.update()
        return task.cont
    
    def clear(self):
        self.aiWorld.removeAiChar("seeker")
        taskMgr.remove("AIUpdate")

