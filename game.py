import sys

import pygame

from classes import Player
from classes.gamestates import End, Fight, Level, Start
from classes.managers import EnemyManager, GameStateManager
from constants import *
from modules.map_converter import image_to_array


class Game:
    # game init
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager("start")
        self.enemyManager = EnemyManager(self.gameStateManager, self.screen)

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
            self.gameStateManager,
        )

        # Map generation
        image_path = "assets/maps/map2.png"  # Ersetze dies durch deinen Dateipfad
        array = image_to_array(image_path)
        self.gameMap = array

        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(
            self.screen,
            self.gameStateManager,
            self.PLAYER,
            self.gameMap,
            self.enemyManager,
        )
        self.fight = Fight(
            self.screen, self.gameStateManager, self.PLAYER, self.enemyManager
        )
        self.end = End(self.screen, self.gameStateManager)

        self.states = {
            "start": self.start,
            "level": self.level,
            "fight": self.fight,
            "end": self.end,
        }

        self.enemyManager.createEnemy()

        #! debug
        print(self.enemyManager.allEnemies[0].type)

    # Gameloop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.gameStateManager.setState("level")

            self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
