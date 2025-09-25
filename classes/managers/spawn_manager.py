from classes import Spawner


class SpawnManager:
    def __init__(self):
        self.possibleEnemySpawns = [
            [900, 100],  # Top Right
            [500, 100],  # Top Mid
            [100, 100],  # Top Left
            [900, 500],  # Bot Right
            [500, 300],  # Bot Mid
            [80, 300],  # Bot Left
        ]

        self.topRightSP = Spawner(self.possibleEnemySpawns[0], 0)
        self.topMidSP = Spawner(self.possibleEnemySpawns[1], 1)
        self.topLeftSP = Spawner(self.possibleEnemySpawns[2], 2)

        self.botRightSP = Spawner(self.possibleEnemySpawns[3], 3)
        self.botMidSP = Spawner(self.possibleEnemySpawns[4], 4)
        self.botLeftSP = Spawner(self.possibleEnemySpawns[5], 5)

        self.allSpawners = [
            self.topRightSP,
            self.topMidSP,
            self.topLeftSP,
            self.botRightSP,
            self.botMidSP,
            self.botLeftSP,
        ]

    def tickSpawnerTimers(self):
        for spawner in self.allSpawners:
            spawner.tickSpawnTimer()

    def clearSpawner(self, id):
        """Mark a spawner as empty again and reset its timer so it waits before respawning."""
        spawner = self.allSpawners[id]
        spawner.isEmpty = True
        spawner.spawnTimer = 0
