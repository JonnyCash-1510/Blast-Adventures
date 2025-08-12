import pygame


class Player:
    def __init__(
        self,
        pos: list,
        name: str,
        size: int,
        diff: float,
        type: str,
        xp: int,
        hp: int,
        speed: int,
        dodge: float,
        att: int,
        cp: float,
        defe: int,
    ):
        self.name = name
        self.pos = pos
        self.size = size
        self.type = type
        self.xp = xp

        self.hp = hp
        self.speed = speed
        self.dodge = dodge
        self.att = att
        self.cp = cp
        self.defe = defe

        self.items = []

        self.playerMoney = 0

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def loadItems(self):
        # * DEBUG
        print("items are being loaded by player.loadItems()")

        # ToDo enter actual balanced stats
        self.hp, self.speed, self.dodge, self.att, self.cp, self.defe = (
            # standart values
            100,
            2,
            0.1,
            10,
            0.1,
            20,
        )

        for item in self.items:

            self.hp *= item.hpS
            self.speed *= item.speedS
            self.dodge *= item.dodgeS
            self.att *= item.attS
            self.cp *= item.cpS
            self.defe *= item.defeS
