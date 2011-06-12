from panda3d.ai import AIWorld, AICharacter

from manager import Manager


class AIManager(Manager):
    def __init__(self):
        # Creating AI World
        self.aiWorld = AIWorld(render)

        self.aiChar = AICharacter("seeker", base.enemy.actor, 100, 0.05, 1.0)
        self.aiWorld.addAiChar(self.aiChar)
        
        self.aiBehaviors = self.aiChar.getAiBehaviors()
        self.aiBehaviors.pursue(base.character.actor)

        # AI World update
        taskMgr.add(self.update, "AIUpdate")
        
    def update(self, task):
        """Update the AI World"""
        self.aiWorld.update()
        return task.cont
    
    def clear(self):
        self.aiWorld.removeAiChar("seeker")
        taskMgr.remove("AIUpdate")

