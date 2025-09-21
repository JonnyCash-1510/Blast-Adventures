class Spawner:
    def __init__(self, pos, spawnTimerOffset, id):
        self.spawnTimer = spawnTimerOffset * 60  # Seconds
        self.pos = pos
        self.isEmpty = True
        self.id = id

    def tickSpawnTimer(self):
        if self.isEmpty:
            self.spawnTimer += 1
