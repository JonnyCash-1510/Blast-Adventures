import pygame


class Enemy:
    def __init__(
        self,
        id,
        pos: list,
        type,
        size: int,
        att,
        defe,
        diff,
        hp,
    ):
        self.pos = pos
        self.id = id
        self.type = type
        self.size = size
        self.att = att * diff
        self.defe = defe * diff
        self.hp = hp

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
