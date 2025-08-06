class Fight:
    def __init__(self, display, gamestateManager, PLAYER, enemyManager):
        self.display = display
        self.gameStateManager = gamestateManager
        self.PLAYER = PLAYER
        self.enemyManager = enemyManager

    def run(self):
        self.display.fill("red")
