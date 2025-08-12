import pygame

from constants import *

TILE_SIZE = 10  # Neue Größe der Tiles


class Level:
    def __init__(
        self, display, gameStateManager, PLAYER, enemyManager, gameEventManager
    ):
        self.display = display
        self.gameStateManager = gameStateManager
        self.enemyManager = enemyManager
        self.gameEventManager = gameEventManager

        self.gameMap = self.gameStateManager.currentMap
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

        self.gameEventManager.timer()
        self.gameEventManager.enemySpawner()

        self.enemyManager.renderEnemies()

        pygame.display.flip()
