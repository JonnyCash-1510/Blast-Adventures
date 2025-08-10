from classes.managers import EnemyManager


class GameEventManager:
    def __init__(self, enemyManager):
        self.gameTime = 0
        self.secondsTime = 0
        self.spawnTimer = 0
        self.enemyManager = enemyManager

    def timer(self):
        self.gameTime += 1
        self.secondsTime = self.gameTime / 60
        self.spawnTimer += 1

    def enemySpawner(self):
        if self.spawnTimer > 600:
            self.enemyManager.createEnemy()
            self.spawnTimer = 0
