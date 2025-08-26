import pygame

from constants import *

TILE_SIZE = 40  # Neue Größe der Tiles


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

        # LOAD TEXTURES
        self.floorTexture = pygame.image.load(
            "./assets/textures/floor/cobble_blood_1_old.png"
        ).convert()
        self.floorTexture = pygame.transform.scale(
            self.floorTexture, (TILE_SIZE, TILE_SIZE)
        )

        self.dirtTexture1 = pygame.image.load(
            "./assets/textures/floor/dirt_0_new.png"
        ).convert()
        self.dirtTexture1 = pygame.transform.scale(
            self.dirtTexture1, (TILE_SIZE, TILE_SIZE)
        )

    def buildMapSurface(self):
        mapSurface = pygame.Surface(self.display.get_size())
        for y, row in enumerate(self.gameMap):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    mapSurface.blit(self.floorTexture, rect)
                else:
                    mapSurface.blit(self.dirtTexture1, rect)
        return mapSurface

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
        self.mapSurface = self.buildMapSurface()
        self.display.blit(self.mapSurface, (0, 0))

        # Spieler zeichnen
        pygame.draw.rect(self.display, WHITE, self.PLAYER.rect)

        #! check Enemy Collision once / frame

        for enemy in self.enemyManager.allEnemies:
            if self.PLAYER.rect.colliderect(enemy):
                self.gameStateManager.setCurrentEnemy(enemy)
                self.gameStateManager.setState("fight")

        self.gameEventManager.timer()
        self.gameEventManager.enemySpawner()

        self.enemyManager.renderEnemies()

        pygame.display.flip()
