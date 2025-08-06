class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def getState(self):
        return self.currentState

    def setState(self, state):
        self.currentState = state

    def getCurrentEnemy(self):
        return self.currentEnemy

    def setCurrentEnemy(self, currentEnemy):
        self.currentEnemy = currentEnemy
