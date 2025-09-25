class Spawner:
    def __init__(self, pos, id):
        # start each spawner at a delay so they don't all trigger together
        self.spawnTimer = 0
        self.pos = pos
        self.isEmpty = False
        self.id = id

    def tickSpawnTimer(self):
        if self.isEmpty:
            self.spawnTimer += 1
