class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self, events):
        # todo Start screen goes here
        self.display.fill("green")
