import pygame
import os
import random

W_WIDTH = 500
W_HEIGHT = 800

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))
IMAGES_CHARACTER = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento3.png')))
]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('ariel', 50)


class Character:
    img = IMAGES_CHARACTER
    # Rotation animations
    rot_max = 25
    rot_speed = 20
    time_anim = 5
    scale_factor = 0.2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.img_position = 0

        self.img = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor),
                                                   int(image.get_height() * self.scale_factor))) for image in self.img]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # Calculate the displacement
        self.time += 1  # ms
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        # Restrict the displacement
        if displacement > 10:
            displacement = 10
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # Character angle
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.rot_max:
                self.angle = self.rot_max
        else:
            if self.angle > -90:
                self.angle -= self.rot_speed

    def draw(self, window):
        # Animate image frames
        self.img_position += 1
        if self.img_position < self.time_anim:
            img = self.img[0]
        elif self.img_position < self.time_anim * 2:
            img = self.img[1]
        elif self.img_position < self.time_anim * 3:
            img = self.img[2]
        elif self.img_position < self.time_anim * 4:
            img = self.img[1]
        else:
            img = self.img[0]
            self.img_position = 0  # Reset animation cycle

        # Down image
        if self.angle <= -80:
            img = self.img[1]
            self.img_position = self.time_anim * 2

        # Draw image
        rot_img = pygame.transform.rotate(img, self.angle)
        pos_center_img = img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rot_img.get_rect(center=pos_center_img)
        window.blit(rot_img, rectangle.topleft)

    def get_mask(self):
        #  Collision
        return pygame.mask.from_surface(self.img[0])


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_bottom = 0
        self.pipe_top = pygame.transform.flip(IMAGE_PIPE, False, True)
        self.pipe_bottom = IMAGE_PIPE
        self.passed = False  # If passed the character
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.pipe_top.get_height()
        self.pos_bottom = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.pos_top))
        window.blit(self.pipe_bottom, (self.x, self.pos_bottom))

    def clash(self, character):
        character_mask = character.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        distance_top = (self.x - character.x, self.pos_top - round(character.y))
        distance_bottom = (self.x - character.x, self.pos_bottom - round(character.y))

        top_point = character_mask.overlap(top_mask, distance_top)
        bottom_point = character_mask.overlap(bottom_mask, distance_bottom)

        if bottom_point or top_point:
            return True
        else:
            return False


class Floor:
    SPEED = 5
    WIDTH = IMAGE_FLOOR.get_width()
    IMAGE = IMAGE_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMAGE, (self.x1, self.y))
        window.blit(self.IMAGE, (self.x2, self.y))


def draw_window(window, characters, pipes, floor, points):
    # Drawing game
    window.blit(IMAGE_BACKGROUND, (0, 0))
    for character in characters:
        character.draw(window)
    for pipe in pipes:
        pipe.draw(window)

    text = FONT_POINTS.render(f'Pontuação: {points}', 1, (255, 255, 255))
    window.blit(text, (W_WIDTH - 10 - text.get_width(), 10))
    floor.draw(window)
    pygame.display.update()


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

        # User interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for character in characters:
                        character.jump()

        # Moving objects
        for character in characters:
            character.move()
            floor.move()

        add_pipes = False
        remove_pipes = []
        for pipe in pipes:
            for i, character in enumerate(characters):
                if pipe.clash(character):
                    characters.pop(i)
                if not pipe.passed and character.x > pipe.x:
                    pipe.passed = True
                    add_pipes = True
            pipe.move()
            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipes:
            points += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, character in enumerate(characters):
            if (character.y + character.img[0].get_height()) > floor.y or character.y < 0:
                characters.pop(i)

        draw_window(window, characters, pipes, floor, points)


if __name__ == '__main__':
    main()
