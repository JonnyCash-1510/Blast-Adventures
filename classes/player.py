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
        maxhp: int,
    ):
        self.name = name
        self.pos = pos
        self.size = size
        self.type = type
        self.xp = xp

        self.hp = hp
        self.maxhp = maxhp
        self.speed = speed
        self.dodge = dodge
        self.att = att
        self.cp = cp
        self.defe = defe
        self.shield = 0  # TODO MAKE CHAT DISPLAY THIS IN BLUE
        self.maxShield = 50

        self.items = []

        self.power = 50

        # TODO Make this Character dependent
        self.abilities = ["stab", "stun", "shield"]

        self.playerMoney = 0

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def loadItems(self):
        # * DEBUG
        print("items are being loaded by player.loadItems()")

        # ToDo enter actual balanced stats
        self.hp, self.speed, self.dodge, self.att, self.cp, self.defe = (
            # standart values
            50,
            2,
            0.1,
            15,
            0.2,
            20,
        )

        for item in self.items:

            hpBoost = self.maxhp * item.hpS - self.maxhp
            self.maxhp *= item.hpS
            self.hp += hpBoost
            # if self.hp < 0.5 * self.maxhp:
            #     self.hp *= 1.2
            # elif self.hp < 0.8 * self.maxhp:
            #     self.hp *= 1.05

            self.speed *= item.speedS
            self.dodge *= item.dodgeS
            self.att *= item.attS
            self.cp *= item.cpS
            self.defe *= item.defeS
