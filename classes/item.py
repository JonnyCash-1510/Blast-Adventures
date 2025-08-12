class Item:
    def __init__(
        self, cost, xpBorder, locked, name, type, hpS, speedS, dodgeS, attS, cpS, defeS
    ):
        self.cost = cost
        self.xpBorder = xpBorder
        self.locked = locked
        self.name = name
        self.type = type

        self.hpS = hpS
        self.speedS = speedS
        self.dodgeS = dodgeS
        self.attS = attS
        self.cpS = cpS
        self.defeS = defeS

    def isUnlocked(self):
        self.locked = False
