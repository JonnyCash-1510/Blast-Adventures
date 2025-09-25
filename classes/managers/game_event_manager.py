class GameEventManager:
    def __init__(self, enemyManager, spawnManager):
        self.gameTime = 0
        self.secondsTime = 0

        self.enemyManager = enemyManager
        self.spawnManager = spawnManager

        # how long (in frames) before a spawner can respawn again
        self.spawnCooldown = 20 * 60  # 20 seconds

    def gameTimer(self):
        self.gameTime += 1

    def timer(self):
        self.secondsTime = self.gameTime / 60
        self.spawnManager.tickSpawnerTimers()

    def enemySpawner(self):
        for spawn in self.spawnManager.allSpawners:
            if spawn.isEmpty and spawn.spawnTimer >= self.spawnCooldown:
                self.enemyManager.createEnemy(spawn.pos, spawn.id)
                spawn.isEmpty = False
                spawn.spawnTimer = 0

    def defaultSpawn(self):
        for spawn in self.spawnManager.allSpawners:
            self.enemyManager.createEnemy(spawn.pos, spawn.id)
            spawn.isEmpty = False
            spawn.spawnTimer = 0
