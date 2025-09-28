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

        # UI Layout (bigger characters)
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
        self.playerTurn = False

        # Fight state (initialized later)
        self.currentEnemy = None
        self.enemyMaxHp = 0
        self.enemyHp = 0

        self.fightActive = False

    def initFight(self):
        self.currentEnemy = self.gameStateManager.getCurrentEnemy()
        if self.currentEnemy is None:
            # No enemy available, do not initialize fight
            self.fightActive = False
            self.gameStateManager.setState("level")
            return
        self.enemyMaxHp = self.currentEnemy.hp
        self.enemyHp = self.enemyMaxHp

        self.playerTurn = False
        self.lastActionTime = time.time()
        self.fightActive = True

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
    ):
        if dynamic:
            # Scale bar for player depending on max HP
            barWidth = int(maxHp * 1.5)

        ratio = max(currentHp / maxHp, 0)
        # Outline
        pygame.draw.rect(self.display, self.BLACK, (x, y, barWidth, barHeight), 2)
        # Background (red)
        pygame.draw.rect(
            self.display, self.RED, (x + 2, y + 2, barWidth - 4, barHeight - 4)
        )
        # Current HP (green)
        pygame.draw.rect(
            self.display,
            self.GREEN,
            (x + 2, y + 2, int((barWidth - 4) * ratio), barHeight - 4),
        )

        # Optional tick marks (every 10 HP)
        if showTicks:
            pixels_per_hp = (barWidth - 4) / maxHp
            for hp_tick in range(10, maxHp, 10):  # draw at 10, 20, 30... maxHp
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
        self.drawHealthBar(
            self.playerPos[0],
            self.playerPos[1] - 25,
            self.player.hp,
            self.player.maxhp,
            dynamic=True,
            showTicks=False,
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
            showTicks=True,
        )

    def drawBottomBar(self):
        pygame.draw.rect(
            self.display,
            self.GRAY,
            (0, self.height - self.barHeight, self.width, self.barHeight),
        )
        # Ability buttons
        abilities = ["Slash", "Shield Bash", "Critical Strike"]
        buttonWidth = 200
        buttonHeight = 50
        for i, ability in enumerate(abilities):
            x = 30 + i * (buttonWidth + 20)
            y = self.height - self.barHeight + 30
            pygame.draw.rect(
                self.display, self.BLACK, (x, y, buttonWidth, buttonHeight), 2
            )
            textSurface = self.font.render(ability, True, self.BLACK)
            textRect = textSurface.get_rect(
                center=(x + buttonWidth / 2, y + buttonHeight / 2)
            )
            self.display.blit(textSurface, textRect)

        # Player stats panel
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

    def handleTurns(self):
        if not self.fightActive:
            return

        # * Checks if one side DIED
        if self.player.hp <= 0 or self.enemyHp <= 0:
            self.fightActive = False
            self.enemyManager.removeEnemy(self.currentEnemy)

            self.spawnManager.clearSpawner(self.currentEnemy.spawnID)  # type: ignore

            self.gameStateManager.setCurrentEnemy(None)
            return

        now = time.time()

        # CALC DAMAGE
        if now - self.lastActionTime >= self.turnDelay:
            if not self.playerTurn:
                # Enemy turn
                dodge = self.rollProbability(self.player.dodge)
                if dodge:
                    print("player DODGED")
                    time.sleep(1)
                    self.playerTurn = True
                else:
                    reduction = (self.player.defe / (self.player.defe + 100)) * 0.4
                    damage = self.currentEnemy.att * (1 - reduction)  # type: ignore
                    damage = round(damage)
                    self.player.hp = max(self.player.hp - damage, 0)
                    self.playerTurn = True
            else:
                # Player turn (auto-attack for now)
                reduction = (
                    self.currentEnemy.defe / (self.currentEnemy.defe + 100) * 0.4  # type: ignore
                )
                crit = self.rollProbability(self.player.cp)
                if crit:
                    print("PLAYER CRIT")
                    damage = (self.player.att * 1.5) * (1 - reduction)
                    damage = round(damage)
                else:
                    damage = (self.player.att) * (1 - reduction)
                    damage = round(damage)

                self.enemyHp = max(self.enemyHp - damage, 0)
                self.playerTurn = False
            self.lastActionTime = now

    def run(self):
        # Only initialize fight if we actually have an enemy
        if not self.fightActive:
            self.initFight()
            if not self.fightActive:
                return  # Nothing to draw, fight is over
        self.handleTurns()
        self.display.fill(self.WHITE)
        self.drawPlayer()
        self.drawEnemy()
        self.drawBottomBar()
