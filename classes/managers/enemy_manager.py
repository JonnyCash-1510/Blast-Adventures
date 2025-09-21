import random

import pygame

from classes.enemy import Enemy
from constants import *


class EnemyManager:
    def __init__(self, gameStateManager, display):
        self.gameStateManager = gameStateManager
        self.allEnemies = []
        self.display = display

        # Todo enemys can only spawn in said coordinates
        self.allStats = [
            [0, "melee", 30, 10, 40, 1.2, 10],
            [1, "longRange", 15, 15, 25, 1.2, 8],
        ]

    def createEnemy(self, pos, spawnID):

        #! [id, pos, type, size, att, defe, diff]
        # todo chooses a random enemy from the allStats list above
        # todo change that later depending on game ig
        stats = random.choice(self.allStats)

        enemy = Enemy(
            stats[0],
            pos,
            stats[1],
            stats[2],
            stats[3],
            stats[4],
            stats[5],
            stats[6],
            spawnID,
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
