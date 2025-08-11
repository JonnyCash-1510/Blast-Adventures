class GameStateManager:
    def __init__(self, currentState, map):
        self.currentState = currentState
        self.currentMap = map

    def getState(self):
        return self.currentState

    def setState(self, state):
        self.currentState = state

    def getCurrentEnemy(self):
        return self.currentEnemy

    def setCurrentEnemy(self, currentEnemy):
        self.currentEnemy = currentEnemy

    def setMap(self, map):
        self.currentMap = map
