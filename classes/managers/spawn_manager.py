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
        self.topMidSP = Spawner(self.possibleEnemySpawns[1], 2, 1)
        self.topLeftSP = Spawner(self.possibleEnemySpawns[2], 0.1, 2)

        self.botRightSP = Spawner(self.possibleEnemySpawns[3], 9, 3)
        self.botMidSP = Spawner(self.possibleEnemySpawns[4], 8, 4)
        self.botLeftSP = Spawner(self.possibleEnemySpawns[5], 6, 5)

        self.allSpawners = [
            self.topLeftSP,
            self.topRightSP,
            self.topMidSP,
            self.botLeftSP,
            self.botRightSP,
            self.botMidSP,
        ]

    def tickSpawnerTimers(self):
        for spawner in self.allSpawners:
            spawner.tickSpawnTimer()

    def clearSpawner(self, id):
        """Mark a spawner as empty again and reset its timer so it waits before respawning."""
        spawner = self.allSpawners[id]
        spawner.isEmpty = True
        spawner.spawnTimer = 0
