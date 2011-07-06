from panda3d.ai import AIWorld, AICharacter

from base import Manager


class AIManager(Manager):
    def __init__(self):
        # Creating AI World
        self.aiWorld = AIWorld(render)
        self.aiChar = None
    
    def setup(self):
        base.enemyManager.addAI()
        taskMgr.add(self.update, "AIUpdate")
    
    def update(self, task):
        """Update the AI World"""
        self.aiWorld.update()
        return task.cont
    
    def addEnemy(self, modelNode, mass, movtForce, maxForce):
        self.aiChar = AICharacter("seeker", modelNode.actor, mass, movtForce, maxForce)
        self.aiWorld.addAiChar(self.aiChar)
        aiBehaviors = self.aiChar.getAiBehaviors()
        aiBehaviors.pursue(base.character.actor)
        
    def clear(self):
        self.aiWorld.removeAiChar("seeker")
        taskMgr.remove("AIUpdate")

