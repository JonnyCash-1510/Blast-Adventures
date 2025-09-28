import random
import time

import pygame


class Fight:
    def __init__(self, display, gameStateManager, player, enemyManager, spawnManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = player
        self.enemyManager = enemyManager
        self.spawnManager = spawnManager

        self.width, self.height = self.display.get_size()

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (200, 200, 200)
        self.BLUE = (0, 150, 255)

        # UI Layout
        self.enemySize = int(self.player.size * 3)
        self.playerSize = int(self.player.size * 3)
        self.enemyPos = (self.width * 0.65, self.height * 0.25)
        self.playerPos = (self.width * 0.15, self.height * 0.45)
        self.barHeight = 150

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.smallFont = pygame.font.Font(None, 22)

        # Turn handling
        self.turnDelay = 1
        self.lastActionTime = time.time()
        self.playerTurn = True

        # Fight state
        self.currentEnemy = None
        self.enemyMaxHp = 0
        self.enemyHp = 0
        self.fightActive = False

    def initFight(self):
        self.currentEnemy = self.gameStateManager.getCurrentEnemy()
        if self.currentEnemy is None:
            self.fightActive = False
            self.gameStateManager.setState("level")
            return

        # Restore player resources
        self.player.power += 35
        self.nextAttReduction = 0
        self.bonusShield = 0

        self.enemyMaxHp = self.currentEnemy.hp
        self.enemyHp = self.enemyMaxHp

        self.playerTurn = True
        self.lastActionTime = time.time()
        self.fightActive = True

    def drawAbilityButtons(self):
        self.abilities = ["Stab", "Stun", "Shield"]
        self.buttonWidth = 200
        self.buttonHeight = 50

        def renderTextInBox(text, font_obj, boxRect, color=(0, 0, 0)):
            surface = font_obj.render(text, True, color)
            if surface.get_width() > boxRect.width - 10:
                ratio = (boxRect.width - 10) / surface.get_width()
                newW = int(surface.get_width() * ratio)
                newH = int(surface.get_height() * ratio)
                surface = pygame.transform.smoothscale(surface, (newW, newH))
            rect = surface.get_rect(center=boxRect.center)
            self.display.blit(surface, rect)

        self.abilityRects = []
        for i, ability in enumerate(self.abilities):
            boxRect = pygame.Rect(
                30 + (i + 1) * (self.buttonWidth + 20),
                self.height - self.barHeight + 30,
                self.buttonWidth,
                self.buttonHeight,
            )
            pygame.draw.rect(self.display, self.BLACK, boxRect, 2)
            self.abilityRects.append(boxRect)
            renderTextInBox(ability, self.font, boxRect, self.BLACK)

        if len(self.abilityRects) == 3:
            self.ability1Rect, self.ability2Rect, self.ability3Rect = self.abilityRects

    def drawHealthBar(
        self,
        x,
        y,
        currentHp,
        maxHp,
        dynamic=False,
        barWidth=150,
        barHeight=14,
        showTicks=False,
        color=(0, 255, 0),
        backColor=(255, 0, 0),
    ):
        if dynamic:
            barWidth = int(maxHp * 1.5)

        ratio = max(currentHp / maxHp, 0)
        pygame.draw.rect(self.display, self.BLACK, (x, y, barWidth, barHeight), 2)
        pygame.draw.rect(
            self.display, backColor, (x + 2, y + 2, barWidth - 4, barHeight - 4)
        )
        pygame.draw.rect(
            self.display,
            color,
            (x + 2, y + 2, int((barWidth - 4) * ratio), barHeight - 4),
        )

        if showTicks:
            pixels_per_hp = (barWidth - 4) / maxHp
            for hp_tick in range(10, maxHp, 10):
                tick_x = x + 2 + int(hp_tick * pixels_per_hp)
                pygame.draw.line(
                    self.display,
                    self.BLACK,
                    (tick_x, y + 2),
                    (tick_x, y + barHeight - 2),
                    1,
                )

    def drawPlayer(self):
        pygame.draw.rect(
            self.display,
            (0, 0, 255),
            (*self.playerPos, self.playerSize, self.playerSize),
        )
        # HP bar
        self.drawHealthBar(
            self.playerPos[0],
            self.playerPos[1] - 25,
            self.player.hp,
            self.player.maxhp,
            dynamic=True,
            color=self.GREEN,
            backColor=self.RED,
        )
        # Shield bar (only if > 0)
        if self.player.shield > 0:
            self.drawHealthBar(
                self.playerPos[0],
                self.playerPos[1] - 45,  # above HP bar
                self.player.shield,
                self.player.maxShield,
                dynamic=True,
                color=self.BLUE,
                backColor=(50, 50, 50),
            )

    def drawEnemy(self):
        enemyRect = pygame.Rect(*self.enemyPos, self.enemySize, self.enemySize)
        pygame.draw.rect(self.display, (255, 0, 0), enemyRect)
        self.drawHealthBar(
            enemyRect.x,
            enemyRect.y - 25,
            self.enemyHp,
            self.enemyMaxHp,
            dynamic=False,
            color=self.GREEN,
            backColor=self.RED,
            showTicks=True,
        )

    def drawBottomBar(self):
        pygame.draw.rect(
            self.display,
            self.GRAY,
            (0, self.height - self.barHeight, self.width, self.barHeight),
        )
        self.drawAbilityButtons()

        statsX = self.width - 250
        statsY = self.height - self.barHeight + 10
        panelHeight = self.barHeight + 20
        pygame.draw.rect(
            self.display, self.BLACK, (statsX, statsY, 220, panelHeight), 2
        )

        stats = [
            f"HP: {self.player.hp}/{self.player.maxhp}",
            f"ATK: {self.player.att}",
            f"DEF: {self.player.defe}",
            f"CRIT: {int(self.player.cp * 100)}%",
            f"DODGE: {int(self.player.dodge * 100)}%",
        ]
        for i, stat in enumerate(stats):
            statSurface = self.smallFont.render(stat, True, self.BLACK)
            self.display.blit(statSurface, (statsX + 10, statsY + 10 + i * 22))

    def rollProbability(self, prob: float) -> bool:
        return random.random() < prob

    def handleAction(self, action):
        if action == "stab":
            reduction = (
                self.currentEnemy.defe / (self.currentEnemy.defe + 100) * 0.4
            ) * 0.75
            damage = round(self.player.att * (1 - reduction))
            self.player.power -= 5
            self.enemyHp = max(self.enemyHp - damage, 0)
            self.playerTurn = False

        elif action == "stun":
            dodge = self.rollProbability(0.2)
            if dodge:
                print("Enemy Dodged")
                self.playerTurn = False
                return
            reduction = self.currentEnemy.defe / (self.currentEnemy.defe + 100) * 0.4
            self.nextAttReduction = 0.5
            crit = self.rollProbability(self.player.cp)
            if crit:
                print("PLAYER CRIT - STUN")
                damage = round(self.player.att * (1 - reduction))
            else:
                damage = round(self.player.att * 0.5 * (1 - reduction))
            self.player.power -= 10
            self.enemyHp = max(self.enemyHp - damage, 0)
            self.playerTurn = False

        elif action == "shield":
            self.bonusShield = 50
            self.player.power -= 15
            self.playerTurn = False

    def handleTurns(self, events):
        if not self.fightActive:
            return

        if self.player.hp <= 0 or self.enemyHp <= 0:
            self.fightActive = False
            self.enemyManager.removeEnemy(self.currentEnemy)
            self.spawnManager.clearSpawner(self.currentEnemy.spawnID)
            self.gameStateManager.setCurrentEnemy(None)
            return

        if self.playerTurn:  # * PLAYER TURN
            if self.bonusShield != 0:
                self.player.shield = min(
                    self.player.shield + self.bonusShield, self.player.maxShield
                )
                print("SHIELD ACTIVATED")
                self.bonusShield = 0

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.ability1Rect.collidepoint(event.pos):
                        self.handleAction(self.player.abilities[0])
                    elif self.ability2Rect.collidepoint(event.pos):
                        self.handleAction(self.player.abilities[1])
                    elif self.ability3Rect.collidepoint(event.pos):
                        self.handleAction(self.player.abilities[2])

        else:  # * ENEMY TURN
            dodge = self.rollProbability(self.player.dodge)
            if dodge:
                print("player DODGED")
            else:
                reduction = (self.player.defe / (self.player.defe + 100)) * 0.4
                crit = self.rollProbability(0.2)  # * (ENEMY CRIT CHANCE 0.2)
                if crit:
                    damage = (self.currentEnemy.att * 1.5) * (1 - reduction)
                    print("ENEMY CRIT")
                else:
                    damage = (self.currentEnemy.att) * (1 - reduction)
                if self.nextAttReduction != 0:
                    damage *= 1 - self.nextAttReduction
                    self.nextAttReduction = 0
                damage = round(damage)

                if self.player.shield > 0:
                    absorbed = min(damage, self.player.shield)
                    self.player.shield -= absorbed
                    damage -= absorbed

                if damage > 0:
                    self.player.hp = max(self.player.hp - damage, 0)

            # always hand turn back
            self.playerTurn = True

    def run(self, events):
        if not self.fightActive:
            self.initFight()
            if not self.fightActive:
                return
        self.display.fill(self.WHITE)
        self.drawPlayer()
        self.drawEnemy()
        self.drawBottomBar()
        self.handleTurns(events)
