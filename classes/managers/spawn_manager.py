from classes import Spawner


class SpawnManager:
    def __init__(self):
        self.possibleEnemySpawns = [
            [900, 100],
            [500, 100],
            [100, 100],
            [900, 500],
            [500, 300],
            [80, 300],
        ]

        self.topRightSP = Spawner(self.possibleEnemySpawns[0], 4, 0)
        self.topLeftSP = Spawner(self.possibleEnemySpawns[2], 0.1, 1)
        self.topMidSP = Spawner(self.possibleEnemySpawns[1], 2, 2)

        self.botRightSP = Spawner(self.possibleEnemySpawns[3], 9, 3)
        self.botLeftSP = Spawner(self.possibleEnemySpawns[5], 6, 4)
        self.botMidSP = Spawner(self.possibleEnemySpawns[4], 8, 5)

        self.allSpawners = [
            self.topLeftSP,
            self.topRightSP,
            self.topMidSP,
            self.botLeftSP,
            self.botRightSP,
            self.botMidSP,
        ]

    def tickSpawnerTimers(self):
        self.topRightSP.tickSpawnTimer()
        self.topLeftSP.tickSpawnTimer()
        self.topMidSP.tickSpawnTimer()

        self.botRightSP.tickSpawnTimer()
        self.botLeftSP.tickSpawnTimer()
        self.botMidSP.tickSpawnTimer()

    def clearSpawner(self, id):
        spawner = self.allSpawners[id]
        spawner.spawnTimer = 0
        spawner.isEmpty = True
