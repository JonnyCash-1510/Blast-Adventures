class Item:
    def __init__(
        self,
        cost,
        xpBorder,
        locked,
        name,
        type,
        hpS,
        speedS,
        dodgeS,
        attS,
        cpS,
        defeS,
        texture,
    ):
        self.cost = cost
        self.xpBorder = xpBorder
        self.locked = locked
        self.name = name
        self.type = type
        self.texture = texture

        self.hpS = hpS
        self.speedS = speedS
        self.dodgeS = dodgeS
        self.attS = attS
        self.cpS = cpS
        self.defeS = defeS
        self.available = True

    def isUnlocked(self):
        self.locked = False

    def isAvailable(self):
        return self.available
