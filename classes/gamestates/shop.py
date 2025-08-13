import random
import time

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
        swordI = Item(10, 0, False, "sword", "melee", 1, 1, 0.9, 1.5, 1.2, 1)
        shieldI = Item(10, 0, False, "shield", "defence", 1, 0.8, 1.2, 1, 1, 1.5)
        trinketI = Item(5, 0, False, "trinket", "potion", 1.5, 1.5, 1, 1, 0.5, 1)

        # ToDo Item Class & add allItems
        self.allItems = [swordI, shieldI, trinketI]

    def unlockItems(self):
        for item in self.allItems:
            if self.player.xp > item.xpBorder:  # ToDo player xp & xpBorder
                item.locked = False

    def closeShop(self):
        self.gameStateManager.setState("level")

    def drawItems(self):  # CHATGPTs work :D
        screenWidth, screenHeight = self.display.get_size()

        # Padding and sizing
        paddingX = 50  # Space at left/right edges
        paddingY = 500
        itemGap = 20  # Space between items

        # Dynamic rectangle width
        numItems = len(self.allItems)
        rectWidth = (
            screenWidth - (2 * paddingX) - (itemGap * (numItems - 1))
        ) / numItems
        rectHeight = screenHeight - (2 * paddingY)

        # Y position stays constant (center vertically)
        yPos = paddingY

        for i, item in enumerate(self.allItems):
            xPos = paddingX + i * (rectWidth + itemGap)

            # Draw item box
            rect = pygame.Rect(xPos, yPos, rectWidth, rectHeight)

            if item.locked == True:
                color = (150, 150, 150)  # Greyed out -- locked
            elif item.locked == False and item.isAvailable() == False:
                color = (100, 100, 100)  # bought
            else:
                color = (0, 200, 0)  # Green for available

            pygame.draw.rect(self.display, color, rect, border_radius=10)

            # Draw item name centered
            font = pygame.font.SysFont("arial", 24)
            textSurface = font.render(item.name, True, (0, 0, 0))
            textRect = textSurface.get_rect(center=rect.center)
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
        self.drawItems()

        pygame.display.flip()
