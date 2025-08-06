import dataclasses
import random
import sys
from typing import List, Optional

import pygame
from pdf2image import convert_from_path

from modules.map_converter import image_to_array

# Constants
SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 60
TILE_SIZE = 10  # Neue Größe der Tiles

# Farben
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


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
        image_path = "maps/map2.png"  # Ersetze dies durch deinen Dateipfad
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


# define different gamestates
class Level:
    def __init__(self, display, gameStateManager, PLAYER, gameMap, enemyManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.enemyManager = enemyManager

        self.gameMap = gameMap
        self.PLAYER = PLAYER

    def run(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -self.PLAYER.speed
        if keys[pygame.K_d]:
            dx = self.PLAYER.speed
        if keys[pygame.K_w]:
            dy = -self.PLAYER.speed
        if keys[pygame.K_s]:
            dy = self.PLAYER.speed

        self.PLAYER.rect = pygame.Rect(
            self.PLAYER.pos[0] + dx,
            self.PLAYER.pos[1] + dy,
            self.PLAYER.size,
            self.PLAYER.size,
        )

        # Kollision prüfen
        collided = False
        for y, row in enumerate(self.gameMap):
            for x, tile in enumerate(row):
                if tile == 1:  # Wand
                    wall_rect = pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    if self.PLAYER.rect.colliderect(wall_rect):
                        collided = True
                        break
            if collided:
                break

        if not collided:
            self.PLAYER.pos[0] += dx
            self.PLAYER.pos[1] += dy

        # Bildschirm löschen
        self.display.fill(BLACK)

        # Map zeichnen
        for y, row in enumerate(self.gameMap):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    pygame.draw.rect(self.display, GRAY, rect)
                else:
                    pygame.draw.rect(self.display, WHITE, rect)

        # Spieler zeichnen
        pygame.draw.rect(self.display, BLUE, self.PLAYER.rect)

        #! check Enemy Collision once / frame

        for enemy in self.enemyManager.allEnemies:
            if self.PLAYER.rect.colliderect(enemy):
                self.gameStateManager.setCurrentEnemy(enemy)
                self.gameStateManager.setState("fight")

        self.enemyManager.renderEnemies()

        pygame.display.flip()


class Fight:
    def __init__(self, display, gamestateManager, PLAYER, enemyManager):
        self.display = display
        self.gameStateManager = gamestateManager
        self.PLAYER = PLAYER
        self.enemyManager = enemyManager

    def run(self):
        self.display.fill("red")


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        # todo Start screen goes here
        self.display.fill("green")


class End:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        # todo End screen goes here
        self.display.fill("black")


# gamestatemanager
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

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
        id,
        pos: list,
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


class EnemyManager:
    def __init__(self, gameStateManager, display):
        self.gameStateManager = gameStateManager
        self.allEnemies = []
        self.display = display

        # Todo enemys can only spawn in said coordinates
        self.allStats = [
            [0, [10, 100], "melee", 30, 10, 40, 1.2],
            [1, [100, 100], "longRange", 15, 15, 25, 1.2],
        ]

    def createEnemy(self):

        #! [id, pos, type, size, att, defe, diff]
        # todo chooses a random enemy from the allStats list above
        # todo change that later depending on game ig
        stats = random.choice(self.allStats)

        enemy = Enemy(
            stats[0],
            stats[1],
            stats[2],
            stats[3],
            stats[4],
            stats[5],
            stats[6],
            self.gameStateManager,
        )

        self.allEnemies.append(enemy)
        return enemy

    def getEnemies(self):
        return self.allEnemies

    def appendEnemy(self, enemy):
        self.allEnemies.append(enemy)

    def removeEnemy(self, enemy):
        self.allEnemies.remove(enemy)

    def renderEnemies(self):
        # Todo render actual artwork dependent on enemy type
        for i in self.allEnemies:
            pygame.draw.rect(self.display, BLACK, i.rect)


if __name__ == "__main__":
    game = Game()
    game.run()
