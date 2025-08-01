import sys
from typing import Optional

import pygame
from pdf2image import convert_from_path

from modules.map_converter import image_to_array

# Constants
SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 60


class Game:
    # game init
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager("start")
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)

        self.states = {"start": self.start, "level": self.level}

    # Gameloop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Todo Use Actual Event to Trigger Level
                if event.type == pygame.KEYDOWN:
                    self.gameStateManager.setState("level")

            self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)


# define different gamestates
class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    # Todo Level Run() goes here
    def run(self):
        self.display.fill("blue")


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        # todo Start screen goes here
        self.display.fill("red")


# gamestatemanager
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        self.currentEnemy: Optional[Enemy] = None
        self.enemies = []

    def getState(self):
        return self.currentState

    def setState(self, state):
        self.currentState = state

    def getCurrentEnemy(self):
        return self.currentEnemy

    def setCurrentEnemy(self, currentEnemy):
        self.currentEnemy = currentEnemy


# Ingame Classes
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


class Enemy:
    def __init__(
        self,
        pos: list,
        id,
        type,
        size: int,
        att,
        defe,
        diff,
        gameStateManager: GameStateManager,
    ):
        self.pos = pos
        self.id = id
        self.type = type
        self.size = size
        self.att = att * diff
        self.defe = defe * diff
        self.gameStateManager = gameStateManager

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)


if __name__ == "__main__":
    game = Game()
    game.run()
