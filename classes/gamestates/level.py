import pygame

from constants import *


class Level:
    def __init__(
        self, display, gameStateManager, PLAYER, enemyManager, gameEventManager, shop
    ):
        self.display = display
        self.gameStateManager = gameStateManager
        self.enemyManager = enemyManager
        self.gameEventManager = gameEventManager
        self.shop = shop

        self.gameMap = self.gameStateManager.currentMap
        self.PLAYER = PLAYER

        # LOAD TEXTURES

        self.floorTtr = self.loadTextureAsTtr("floor/cobble_blood_1_old.png")

        self.dirtTtr1 = self.loadTextureAsTtr("floor/dirt_0_new.png")

        self.closedShopTtr = self.loadTextureAsTtr("shop/abandoned_shop.png")

        self.openedShopTtr = self.loadTextureAsTtr("shop/enter_shop.png")

    def loadTextureAsTtr(self, path):
        path = "./assets/textures/" + path
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.scale(texture, (TILE_SIZE, TILE_SIZE))
        return texture

    def buildMapSurface(self):
        mapSurface = pygame.Surface(self.display.get_size())
        for y, row in enumerate(self.gameMap):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    mapSurface.blit(self.floorTtr, rect)
                elif tile == 0:
                    mapSurface.blit(self.dirtTtr1, rect)
                elif tile == 2:
                    mapSurface.blit(self.closedShopTtr, rect)
                elif tile == 3:
                    mapSurface.blit(self.openedShopTtr, rect)
        return mapSurface

    def detectPlayerCollision(
        self, x, y
    ):  # DETECTS IF PLAYER COLLIDES WITH A CERTAIN TILE IN MAP-ARRAY (X & Y COORDS FROM ARRAY REPRESENTS A TILE ON MAP)
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if self.PLAYER.rect.colliderect(rect):
            return True
        else:
            return False

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
                    if self.detectPlayerCollision(x, y):
                        collided = True
                        break
                if tile == 2:  # Closed Shop
                    if self.detectPlayerCollision(x, y):
                        # ToDo create screen that displays the shop is closed still
                        print("cant enter... still closed")
                        collided = True
                        break
                if tile == 3:  # Opened Shop
                    if self.detectPlayerCollision(x, y):
                        shopRect = pygame.Rect(
                            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                        )
                        if self.PLAYER.rect.colliderect(shopRect):
                            # Get distances from each side of the shop
                            left_dist = abs(self.PLAYER.rect.right - shopRect.left)
                            right_dist = abs(self.PLAYER.rect.left - shopRect.right)
                            top_dist = abs(self.PLAYER.rect.bottom - shopRect.top)
                            bottom_dist = abs(self.PLAYER.rect.top - shopRect.bottom)

                            # Find the smallest overlap → that's the side the player entered from
                            min_dist = min(left_dist, right_dist, top_dist, bottom_dist)

                            if min_dist == left_dist:
                                self.shop.enteredFrom = "left"
                            elif min_dist == right_dist:
                                self.shop.enteredFrom = "right"
                            elif min_dist == top_dist:
                                self.shop.enteredFrom = "top"
                            elif min_dist == bottom_dist:
                                self.shop.enteredFrom = "bottom"

                            self.gameStateManager.setState("shop")
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

        # * check Enemy Collision once / frame

        for enemy in self.enemyManager.allEnemies:
            if self.PLAYER.rect.colliderect(enemy):
                self.gameStateManager.setCurrentEnemy(enemy)
                self.gameStateManager.setState("fight")

        self.gameEventManager.timer()
        self.gameEventManager.enemySpawner()

        self.enemyManager.renderEnemies()

        pygame.display.flip()
