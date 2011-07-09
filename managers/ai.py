from panda3d.ai import AIWorld, AICharacter

from base import Manager


class AIManager(Manager):
    def __init__(self):
        # Creating AI World
        self.aiWorld = AIWorld(render)
        self.aiCharList = []
    
    def setup(self):
        base.gameState.currentState.managers['enemy'].addAI()
        taskMgr.add(self.update, "AIUpdate")
    
    def update(self, task):
        """Update the AI World"""
        self.aiWorld.update()
        return task.cont
    
    def addEnemy(self, modelNode, mass, movtForce, maxForce):
        aiChar = AICharacter("seeker", modelNode.actor, mass, movtForce, maxForce)
        self.aiWorld.addAiChar(aiChar)
        aiBehaviors = aiChar.getAiBehaviors()
        character = base.gameState.currentState.objects['character']
        aiBehaviors.pursue(character.actor)
        
        self.aiCharList.append(aiChar)
        
    def clear(self):
        self.aiWorld.removeAiChar("seeker")
        taskMgr.remove("AIUpdate")
        
        self.aiCharList = []
