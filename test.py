import pygame

pygame.init()
clock = pygame.time.Clock()

running = True

timer = 0

while running:
    timer += 1
    if timer / 600 % 2:

        print(timer)
    clock.tick(60)
