import sys

import pygame

from classes import Map, Player
from classes.gamestates import End, Fight, Level, Shop, Start
from classes.managers import Economy, EnemyManager, GameEventManager, GameStateManager
from constants import *


class Game:
    # game init
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.map1 = Map("assets/maps/map2.png")

        self.gameStateManager = GameStateManager("start", self.map1.imageToArray())
        self.enemyManager = EnemyManager(self.gameStateManager, self.screen)
        self.gameEventManager = GameEventManager(self.enemyManager)

        self.itemsIsLoaded = False
        self.PLAYER = Player(
            [10, 10],
            "Player1",
            TILE_SIZE - 1,
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

        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(
            self.screen,
            self.gameStateManager,
            self.PLAYER,
            self.enemyManager,
            self.gameEventManager,
        )
        self.fight = Fight(
            self.screen, self.gameStateManager, self.PLAYER, self.enemyManager
        )
        self.end = End(self.screen, self.gameStateManager)
        self.shop = Shop(self.screen, self.gameStateManager, self.PLAYER, self.economy)
        self.states = {
            "start": self.start,
            "level": self.level,
            "fight": self.fight,
            "end": self.end,
            "shop": self.shop,
        }

        # self.enemyManager.createEnemy()

        # #! debug
        # print(self.enemyManager.allEnemies[0].type)

    # Gameloop
    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
