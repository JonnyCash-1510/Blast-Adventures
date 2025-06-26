import pygame
import sys
from modules.map_converter import image_to_array
from pdf2image import convert_from_path


# Initialisieren
pygame.init()

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

# MODES

# Mode 1
# Map generation
image_path = "maps/map1.png"  # Ersetze dies durch deinen Dateipfad
array = image_to_array(image_path)

game_map = array

# Spieler starten
player_pos = [TILE_SIZE * 2, TILE_SIZE * 2]  # Startposition
speed = 60 # FPS


#Funktionen

    


def running_mode():
    move_speed = PLAYER.speed  # Pixel pro Frame


    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx = -move_speed
    if keys[pygame.K_d]:
        dx = move_speed
    if keys[pygame.K_w]:
        dy = -move_speed
    if keys[pygame.K_s]:
        dy = move_speed


    # Neuer Player-Rect mit versetzter Position
    PLAYER.rect = pygame.Rect(PLAYER.pos[0] + dx, PLAYER.pos[1] + dy, PLAYER.size, PLAYER.size)

    # Kollision prüfen
    collided = False
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 1:  # Wand
                wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
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
    pygame.draw.rect(screen, BLACK, Enemy1.rect)

    if PLAYER.rect.colliderect(Enemy1.rect):
        MODE = 2



    pygame.display.flip()

def end_screen_mode():
   screen.fill(BLACK)
   pygame.display.flip()

def title_screen_mode():
    title_screen_img = convert_from_path('assets/title_screen_img.pdf', dpi=150) #liste der seiten
    title_screen_img = title_screen_img[0].convert("RGB") #erste seite als pdf nehmen

    pg_image = pygame.image.fromstring(title_screen_img.tobytes(), title_screen_img.size, 'RGB')
    pg_image = pygame.transform.scale(pg_image, (800, 600)) 

    screen.blit(pg_image, (0, 0))
    pygame.display.flip()

def fighting_mode(Enemy):
    screen.fill(WHITE)
    fighting_player_size = 40
    player_rect = pygame.Rect(SCREEN_WIDTH/6, SCREEN_HEIGHT/2 - fighting_player_size, fighting_player_size, fighting_player_size)
    pygame.draw.rect(screen, BLUE, player_rect)

    print(Enemy.size)

    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        global MODE
        MODE = 1


#Klassen
class Player:
    def __init__(self, pos: list, name: str, size: int, diff: float, type: str, xp: int, hp: int, speed: int, dodge: float, att: int, cp: float, defe: int):
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
        MODE = 2
        fighting_mode(enemy)


PLAYER = Player([10, 10], "Player1", TILE_SIZE - 1, 1.0, "melee", 0, 100, 2, 0.1, 10, 0.1, 20)

class Enemy:
    def __init__(self, pos: list, id, type, size, att, defe, diff):
        self.pos = pos
        self.id = id
        self.type = type
        self.size = size
        self.att = att * diff
        self.defe = defe * diff

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)





MODE = 4

clock = pygame.time.Clock()

game = True

while game:
    clock.tick(speed)

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    

    if MODE == 1:
        # running_mode for gameplay
        running_mode()

        # Check for mode switch with '3' key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            MODE = 2
        if keys[pygame.K_3]:
            MODE = 3
        if keys[pygame.K_4]:
            MODE = 4

    if MODE == 2:
        fighting_mode(Enemy1????)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            MODE = 1
        if keys[pygame.K_3]:
            MODE = 3
        if keys[pygame.K_4]:
            MODE = 4

    if MODE == 3:
        # end screen mode
        end_screen_mode()

        # Check for mode switch back to 1 with '1' key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            MODE = 1
        if keys[pygame.K_2]:
            MODE = 2
        if keys[pygame.K_4]:
            MODE = 4

    if MODE == 4:
            title_screen_mode()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                MODE = 1
            if keys[pygame.K_2]:
                MODE = 2
            if keys[pygame.K_3]:
                MODE = 3


# Beenden
pygame.quit()
sys.exit()
