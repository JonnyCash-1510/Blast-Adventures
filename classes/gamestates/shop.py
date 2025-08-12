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

    def run(self):
        if self.shopActive == True:
            for item in self.allItems:
                if item.locked == False:
                    # display item
                    pass
                else:
                    # display item as locked
                    pass
            #! display Shop here
            self.display.fill("white")

            keys = pygame.key.get_pressed()

            #! buys random item if r is pressed
            if keys[pygame.K_r]:
                item = random.choice(self.allItems)

                #!!! MAYBE DOENST WORK

                if self.economy.buyItem(item) != 0:
                    print("ITEM LOCKED")
                else:
                    print("ITEM BOUGHT")  # ToDo display that shit
                    for item in self.player.items:
                        print(item.name)
                    # time.sleep(3)
                    self.closeShop()
