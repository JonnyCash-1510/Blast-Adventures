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
        # [id,size,att,defe,diff,hp]
        self.easyStats = [
            [0, "melee", 30, 12, 20, 0.5, 60],
            [1, "longRange", 15, 18, 15, 0.5, 40],
        ]

        self.midStats = [
            [0, "melee", 30, 12, 20, 1, 60],
            [1, "longRange", 15, 18, 15, 1, 40],
        ]

        self.hardStats = [
            [0, "melee", 30, 12, 20, 1.5, 60],
            [1, "longRange", 15, 18, 15, 1.5, 40],
        ]

        self.allStats = [self.easyStats, self.midStats, self.hardStats]

    def createEnemy(self, pos, spawnID, diff):
        statsSet = self.allStats[diff]
        #! [id, pos, type, size, att, defe, diff]
        # todo chooses a random enemy from the allStats list above
        # todo change that later depending on game ig
        stats = random.choice(statsSet)

        enemy = Enemy(
            stats[0],  # id
            pos,  # pos
            stats[1],  # type
            stats[2],  # size
            stats[3],  # ATT
            stats[4],  # DEFE
            stats[5],  # DIFF
            stats[6],  # HP
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
