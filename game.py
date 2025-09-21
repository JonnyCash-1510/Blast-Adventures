import sys

import pygame

from classes import Map, Player
from classes.gamestates import End, Fight, Level, Shop, Start
from classes.managers import (
    Economy,
    EnemyManager,
    GameEventManager,
    GameStateManager,
    SpawnManager,
)
from constants import *


class Game:
    # game init
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.map1 = Map("assets/maps/map2.png")

        self.gameStateManager = GameStateManager("level", self.map1.imageToArray())
        self.enemyManager = EnemyManager(self.gameStateManager, self.screen)
        self.spawnManager = SpawnManager()
        self.gameEventManager = GameEventManager(self.enemyManager, self.spawnManager)

        self.itemsIsLoaded = False
        self.PLAYER = Player(
            [40, 40],
            "Player1",
            10,
            1.0,
            "melee",
            0,
            100,
            2,
            0.1,
            10,
            0.1,
            20,
        )

        self.economy = Economy(self.PLAYER)
        self.shop = Shop(self.screen, self.gameStateManager, self.PLAYER, self.economy)
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(
            self.screen,
            self.gameStateManager,
            self.PLAYER,
            self.enemyManager,
            self.gameEventManager,
            self.shop,
        )
        self.fight = Fight(
            self.screen,
            self.gameStateManager,
            self.PLAYER,
            self.enemyManager,
            self.spawnManager,
        )
        self.end = End(self.screen, self.gameStateManager)

        self.states = {
            "start": self.start,
            "level": self.level,
            "fight": self.fight,
            "end": self.end,
            "shop": self.shop,
        }

        # * spawn default enemys in the beginning
        self.gameEventManager.defaultSpawn()

    # Gameloop
    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # ToDo change this
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p]:
                    self.gameStateManager.setState("shop")
                if keys[pygame.K_SPACE]:
                    self.gameStateManager.setState("level")

            self.states[self.gameStateManager.getState()].run()

            self.gameEventManager.gameTimer()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
