import random


class GameEventManager:
    def __init__(self, enemyManager, spawnManager):
        self.gameTime = 0
        self.secondsTime = 0

        self.enemyManager = enemyManager
        self.spawnManager = spawnManager

    def gameTimer(self):
        self.gameTime += 1

    def timer(self):
        self.secondsTime = self.gameTime / 60
        self.spawnManager.tickSpawnerTimers()

    def enemySpawner(self):
        for spawn in self.spawnManager.allSpawners:  #! FALSCHE LOGIK!!!!!!!
            if spawn.isEmpty:
                if spawn.spawnTimer % (20 * 60) == 0:  # alle 20 Sekunden
                    self.enemyManager.createEnemy(spawn.pos, spawn.id)

    def defaultSpawn(self):
        for spawn in self.spawnManager.allSpawners:
            self.enemyManager.createEnemy(spawn.pos, spawn.id)
