import sys
from typing import Optional

import pygame
from pdf2image import convert_from_path

from modules.map_converter import image_to_array

# Funktionen


def RunningMode():
    PLAYER.speed  # Pixel pro Frame

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx = -PLAYER.speed
    if keys[pygame.K_d]:
        dx = PLAYER.speed
    if keys[pygame.K_w]:
        dy = -PLAYER.speed
    if keys[pygame.K_s]:
        dy = PLAYER.speed

    # Neuer Player-Rect mit versetzter Position
    PLAYER.rect = pygame.Rect(
        PLAYER.pos[0] + dx, PLAYER.pos[1] + dy, PLAYER.size, PLAYER.size
    )

    # Kollision prüfen
    collided = False
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 1:  # Wand
                wall_rect = pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                if PLAYER.rect.colliderect(wall_rect):
                    collided = True
                    break
        if collided:
            break

    # Position aktualisieren, wenn keine Wand im Weg
    if not collided:
        PLAYER.pos[0] += dx
        PLAYER.pos[1] += dy

    # Bildschirm löschen
    screen.fill(BLACK)

    # Map zeichnen
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

    # Spieler zeichnen
    pygame.draw.rect(screen, BLUE, PLAYER.rect)

    Enemy1 = Enemy([10, 100], 0, "melee", 20, 10, 40, 1.2)
    Enemy2 = Enemy([100, 200], 1, "melee", 20, 10, 40, 1.2)
    GameState.enemies.append(Enemy1)
    GameState.enemies.append(Enemy2)
    pygame.draw.rect(screen, BLACK, Enemy1.rect)
    pygame.draw.rect(screen, BLACK, Enemy2.rect)

    for enemy in GameState.enemies:
        if PLAYER.rect.colliderect(enemy):
            GameState.CurrentEnemy = enemy
            GameState.mode = 2

    pygame.display.flip()


def EndScreenMode():
    screen.fill(BLACK)
    pygame.display.flip()


def TitleScreenMode():
    title_screen_img = convert_from_path(
        "assets/title_screen_img.pdf", dpi=150
    )  # liste der seiten
    title_screen_img = title_screen_img[0].convert("RGB")  # erste seite als pdf nehmen

    pg_image = pygame.image.fromstring(
        title_screen_img.tobytes(), title_screen_img.size, "RGB"
    )
    pg_image = pygame.transform.scale(pg_image, (800, 600))

    screen.blit(pg_image, (0, 0))
    pygame.display.flip()


def FightingMode(Enemy):
    screen.fill(WHITE)
    fighting_player_size = 40
    player_rect = pygame.Rect(
        SCREEN_WIDTH / 6,
        SCREEN_HEIGHT / 2 - fighting_player_size,
        fighting_player_size,
        fighting_player_size,
    )
    pygame.draw.rect(screen, BLUE, player_rect)

    print(GameState.CurrentEnemy.id)  # type: ignore

    pygame.display.flip()

    # WIN Debug
    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        # PLAYER.pos[0] += Enemy.size
        # PLAYER.pos[1] += Enemy.size
        GameState.CurrentEnemy = None
        GameState.mode = 1


# Klassen
class GameStateManager:
    def __init__(self):
        self.mode = 1
        self.CurrentEnemy: Optional[Enemy] = None
        self.enemies = []


class Player:
    def __init__(
        self,
        pos: list,
        name: str,
        size: int,
        diff: float,
        type: str,
        xp: int,
        hp: int,
        speed: int,
        dodge: float,
        att: int,
        cp: float,
        defe: int,
    ):
        self.name = name
        self.pos = pos
        self.size = size
        self.diff = diff
        self.type = type
        self.xp = xp
        self.hp = hp
        self.speed = speed
        self.dodge = dodge
        self.att = att
        self.cp = cp
        self.defe = defe

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def engage(self, enemy):
        GameState.mode = 2
        GameState.CurrentEnemy = enemy


class Enemy:
    def __init__(self, pos: list, id, type, size: int, att, defe, diff):
        self.pos = pos
        self.id = id
        self.type = type
        self.size = size
        self.att = att * diff
        self.defe = defe * diff

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)


# Init
pygame.init()
GameState = GameStateManager()

# Konstanten
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 10  # Neue Größe der Tiles

# Farben
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blast Adventures")

# Map generation
image_path = "maps/map1.png"  # Ersetze dies durch deinen Dateipfad
array = image_to_array(image_path)
game_map = array

# Spieler starten
player_pos = [TILE_SIZE * 2, TILE_SIZE * 2]  # Startposition
speed = 60  # FPS

# PLAYER Init
PLAYER = Player(
    [10, 10], "Player1", TILE_SIZE - 1, 1.0, "melee", 0, 100, 2, 0.1, 10, 0.1, 20
)

# Debug Init
GlobalDevEnemy = Enemy([10, 10], 0, "melee", 20, 10, 40, 1.0)


# Clock
clock = pygame.time.Clock()
game = True

while game:
    clock.tick(speed)

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if GameState.mode == 1:
        # RunningMode for gameplay
        RunningMode()

        # Check for mode switch with '3' key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            GameState.mode = 2
        if keys[pygame.K_3]:
            GameState.mode = 3
        if keys[pygame.K_4]:
            GameState.mode = 4

    if GameState.mode == 2:
        FightingMode(GameState.CurrentEnemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            GameState.mode = 1
        if keys[pygame.K_3]:
            GameState.mode = 3
        if keys[pygame.K_4]:
            GameState.mode = 4

    if GameState.mode == 3:
        # end screen mode
        EndScreenMode()

        # Check for mode switch back to 1 with '1' key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            GameState.mode = 1
        if keys[pygame.K_2]:
            GameState.mode = 2
        if keys[pygame.K_4]:
            GameState.mode = 4

    if GameState.mode == 4:
        TitleScreenMode()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            GameState.mode = 1
        if keys[pygame.K_2]:
            GameState.mode = 2
        if keys[pygame.K_3]:
            GameState.mode = 3


# Beenden
pygame.quit()
sys.exit()
