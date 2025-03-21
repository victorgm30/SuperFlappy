import pygame.display

from SuperFlappy import Character, Floor, W_WIDTH, W_HEIGHT, Pipe


def main():
    characters = [Character(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)
