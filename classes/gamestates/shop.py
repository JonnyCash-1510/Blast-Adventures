import random

import pygame

from classes.item import Item


class Shop:
    def __init__(self, display, gameStateManager, player, economy):
        self.player = player
        self.economy = economy
        self.display = display
        self.gameStateManager = gameStateManager
        self.shopActive = True

        self.screenWidth, self.screenHeight = self.display.get_size()

        self.paddingX = 100
        self.paddingTop = 150

        self.itemSize = 120
        self.itemGap = 216 - self.itemSize

        # Y position stays constant (center vertically)
        self.yPos = self.paddingTop

        # declare all available items:
        swordI = Item(
            10,
            0,
            True,
            "Sword",
            "melee",
            1,
            1,
            0.9,
            1.5,
            1.2,
            1,
            "./assets/textures/items/sword.png",
        )
        shieldI = Item(
            10,
            0,
            False,
            "Shield",
            "defence",
            1,
            0.8,
            1.2,
            1,
            1,
            1.5,
            "./assets/textures/items/shield.png",
        )
        trinketI = Item(
            5,
            0,
            False,
            "Trinket",
            "potion",
            1.5,
            1.5,
            1,
            1,
            0.5,
            1,
            "./assets/textures/items/trinket.png",
        )

        maskI = Item(
            50,
            10,
            True,
            "Mask",
            "longrange",
            1,
            1.5,
            1,
            2,
            1.8,
            0.8,
            "./assets/textures/items/mask.png",
        )

        # ToDo Item Class & add allItems
        self.allItems = [swordI, shieldI, trinketI, maskI]

        self.itemRow1 = [swordI, shieldI, trinketI]
        self.itemRow2 = [maskI]
        self.itemRow3 = []

    def unlockItems(self):
        for item in self.allItems:
            if self.player.xp > item.xpBorder:  # ToDo player xp & xpBorder
                item.locked = False

    def closeShop(self):
        self.gameStateManager.setState("level")

    def drawItems(self):  # CHATGPTs work :D

        # row 1
        for i, item in enumerate(self.itemRow1):

            xPos = self.paddingX + i * (self.itemSize + self.itemGap)

            # Draw item box
            rect = pygame.Rect(xPos, self.yPos, self.itemSize, self.itemSize)

            item.rect = rect

            textureSurface = pygame.image.load(item.texture).convert()
            scaledTextureSurface = pygame.transform.scale(
                textureSurface, (self.itemSize, self.itemSize)
            )

            self.display.blit(scaledTextureSurface, (xPos, self.yPos))

            font = pygame.font.SysFont("arial", 24)
            textSurface = font.render(item.name, True, (0, 0, 0))

            if item.locked:
                lockTexture = pygame.image.load(
                    "./assets/textures/lock.png"
                ).convert_alpha()
                scaledLockTexture = pygame.transform.scale(
                    lockTexture, (self.itemSize, self.itemSize)
                )
                self.display.blit(scaledLockTexture, (xPos, self.yPos))

                greyedOutRect = pygame.Surface((self.itemSize, self.itemSize))
                greyedOutRect.set_alpha(150)
                greyedOutRect.fill((0, 0, 0))
                self.display.blit(greyedOutRect, (xPos, self.yPos))

            elif item.isAvailable():
                # Draw item name centered
                textRect = textSurface.get_rect(
                    midtop=(item.rect.centerx, item.rect.bottom)
                )
                pygame.draw.rect(self.display, (150, 150, 150), textRect)
                self.display.blit(textSurface, textRect)
            else:
                greyedOutRect = pygame.Surface((self.itemSize, self.itemSize))
                greyedOutRect.set_alpha(170)
                greyedOutRect.fill((0, 0, 0))
                self.display.blit(greyedOutRect, (xPos, self.yPos))

    def drawShop(self):
        screenWidth, screenHeight = self.display.get_size()

        font = pygame.font.SysFont("arial", 100)
        textSurface = font.render(" -- THE SHOP -- ", True, "black")
        textRect = textSurface.get_rect()
        textRect.center = (screenWidth / 2, 75)

        texture = pygame.image.load("./assets/textures/wooden_plank.png").convert()
        scaledTexture = pygame.transform.scale(texture, self.display.get_size())

        self.display.blit(scaledTexture, (0, 0))

        pygame.draw.rect(self.display, (200, 200, 200), textRect)
        self.display.blit(textSurface, textRect)

    def run(self):
        if self.shopActive:
            #! display Shop here
            self.display.fill("white")
            self.drawShop()

            self.drawItems()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.allItems:
                        if item.rect.collidepoint(event.pos):
                            #!TRIES TO BUY ITEM
                            buy = self.economy.buyItem(item)
                            if buy != 0:  # ERROR NOT BOUGHT
                                print("ITEM LOCKED OR ALREADY BOUGHT")
                            else:
                                print(f"ITEM BOUGHT: {item.name}")
                                print(f"YOU CURRENTLY OWN THESE ITEMS: ")
                                for i in self.player.items:
                                    print(i.name)

            keys = pygame.key.get_pressed()

            #! buys random item if r is pressed
            if keys[pygame.K_r]:
                item = random.choice(self.allItems)

                #!!! MAYBE DOENST WORK
                buy = self.economy.buyItem(item)
                if buy != 0:  # -- not bought
                    print("ITEM LOCKED OR ALREADY BOUGHT")
                else:  # bought
                    print("ITEM BOUGHT")  # ToDo display that shit
                    for item in self.allItems:
                        print(item.isAvailable())

                    for item in self.player.items:
                        print(item.name)
                    # time.sleep(3)
                    self.closeShop()

            pygame.display.flip()
