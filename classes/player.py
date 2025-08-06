import pygame

from classes.managers.gamestate_manager import GameStateManager


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
        gameStateManager: GameStateManager,
    ):
        self.name = name
        self.pos = pos
        self.size = size
        self.diff = diff
        self.type = type
        self.xp = xp
        self.hp = hp
        self.speed = speed
        self.dodge = dodge
        self.att = att
        self.cp = cp
        self.defe = defe
        self.gameStateManager = gameStateManager

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def engage(
        self,
        enemy,
    ):
        self.gameStateManager.setState("fight")
        self.gameStateManager.currentEnemy = enemy
