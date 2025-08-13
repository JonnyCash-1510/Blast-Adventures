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

        # declare all available items:
        swordI = Item(
            10,
            0,
            False,
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
        screenWidth, screenHeight = self.display.get_size()

        paddingX = 100
        paddingTop = 150

        itemSize = 120
        itemGap = 216 - itemSize

        # Y position stays constant (center vertically)
        yPos = paddingTop

        # row 1
        for i, item in enumerate(self.itemRow1):

            xPos = paddingX + i * (itemSize + itemGap)

            # Draw item box
            rect = pygame.Rect(xPos, yPos, itemSize, itemSize)

            # if item.locked == True:
            #     color = (150, 150, 150)  # Greyed out -- locked
            # elif item.locked == False and item.isAvailable() == False:
            #     color = (100, 100, 100)  # bought
            # else:
            #     color = (0, 200, 0)  # Green for available

            # pygame.draw.rect(self.display, color, rect, border_radius=5)

            textureSurface = pygame.image.load(item.texture).convert()
            scaledTextureSurface = pygame.transform.scale(
                textureSurface, (itemSize, itemSize)
            )

            self.display.blit(scaledTextureSurface, (xPos, yPos))

            # Draw item name centered
            font = pygame.font.SysFont("arial", 24)
            textSurface = font.render(item.name, True, (0, 0, 0))
            textRect = textSurface.get_rect(midtop=(rect.centerx, rect.bottom))

            pygame.draw.rect(self.display, (150, 150, 150), textRect)

            self.display.blit(textSurface, textRect)

    def drawShop(self):
        screenWidth, screenHeight = self.display.get_size()

        font = pygame.font.SysFont("arial", 100)
        textSurface = font.render("-- THE SHOP --", True, "black")
        textRect = textSurface.get_rect()
        textRect.center = (screenWidth / 2, 75)

        texture = pygame.image.load("./assets/textures/wooden_plank.png").convert()
        scaledTexture = pygame.transform.scale(texture, self.display.get_size())

        self.display.blit(scaledTexture, (0, 0))

        pygame.draw.rect(self.display, (200, 200, 200), textRect)
        self.display.blit(textSurface, textRect)

    def run(self):
        if self.shopActive == True:
            for item in self.allItems:
                if item.locked == False:
                    # display item
                    pass
                else:
                    # display item as locked
                    pass

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

        #! display Shop here
        self.display.fill("white")
        self.drawShop()

        self.drawItems()

        pygame.display.flip()
