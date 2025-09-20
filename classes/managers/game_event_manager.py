from classes.managers import EnemyManager


class GameEventManager:
    def __init__(self, enemyManager):
        self.gameTime = 0
        self.secondsTime = 0
        self.spawnTimer = 0
        self.enemyManager = enemyManager

    def gameTimer(self):
        self.gameTime += 1

    def timer(self):
        self.secondsTime = self.gameTime / 60
        self.spawnTimer += 1

    def enemySpawner(self):
        if self.spawnTimer > 5 * 60:  # first value is seconds
            self.enemyManager.createEnemy()
            self.spawnTimer = 0
