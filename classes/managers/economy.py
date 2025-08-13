class Economy:
    def __init__(self, player):
        self.player = player
        self.moneyScaling = 1
        pass

    def buyItem(self, item):
        if item.locked == False and item.available == True:
            self.player.items.append(item)
            self.player.playerMoney -= item.cost
            item.available = False

            # * DEBUG
            print("Item is available: ")
            print(item.available)

            self.player.loadItems()

            return 0
        else:
            return 1

    def generateMoney(self):  # called once per 60 frames (1/s)
        self.player.playerMoney += 10 * self.moneyScaling


# ToDo
