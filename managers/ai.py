from panda3d.ai import AIWorld, AICharacter


class AIManager():
    def __init__(self, world):
        # Creating AI World
        self.AIWorld = AIWorld(world.render)

        self.AIchar = AICharacter("seeker", world.enemy.model, 100, 0.05, 1.0)
        self.AIWorld.addAiChar(self.AIchar)
        
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(world.character.model)

        # AI World update
        taskMgr.add(self.update, "AIUpdate")
        
    def update(self, task):
        """Update the AIWorld"""
        self.AIWorld.update()
        return task.cont

