import pygame
import os
import random

from pygame import Surface, Rect
from pygame.font import Font

from Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, C_YELLOW, C_WHITE, C_ORANGE

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))
IMAGES_CHARACTER = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento3.png')))
]

pygame.font.init()
pygame.mixer.init()
FONT_POINTS = pygame.font.SysFont('ariel', 50)


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/Menu.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./assets/Menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Super", C_ORANGE, ((WIN_WIDTH / 2), 330))
            self.menu_text(50, "Flappy", C_ORANGE, ((WIN_WIDTH / 2), 380))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], C_YELLOW, ((WIN_WIDTH / 2), 440 + 25 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], C_ORANGE, ((WIN_WIDTH / 2), 440 + 25 * i))
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # End Pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


class Character:
    imgs = IMAGES_CHARACTER
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
        self.img = self.imgs[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # Calculate the displacement
        self.time += 1  # ms
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        # Restrict the displacement
        if displacement > 16:
            displacement = 16
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
            self.img = self.imgs[0]
        elif self.img_position < self.time_anim * 2:
            self.img = self.imgs[1]
        elif self.img_position < self.time_anim * 3:
            self.img = self.imgs[2]
        elif self.img_position < self.time_anim * 4:
            self.img = self.imgs[1]
        elif self.img_position >= self.time_anim * 4 + 1:
            self.img = self.imgs[0]
            self.img_position = 0

        # Down image
        if self.angle <= -80:
            self.img = self.imgs[1]
            self.img_position = self.time_anim * 2

        # Draw image
        rot_img = pygame.transform.rotate(self.img, self.angle)
        pos_center_img = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rot_img.get_rect(center=pos_center_img)
        window.blit(rot_img, rectangle.topleft)

    def get_mask(self):
        #  Collision
        return pygame.mask.from_surface(self.img)


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
        self.height = random.randrange(50, WIN_HEIGHT - 450)
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

        dist_top = (self.x - character.x, self.pos_top - round(character.y))
        dist_bottom = (self.x - character.x, self.pos_bottom - round(character.y))

        top_point = character_mask.overlap(top_mask, dist_top)
        bottom_point = character_mask.overlap(bottom_mask, dist_bottom)

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
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    floor.draw(window)
    pygame.display.update()


def game_over(window, points):
    # Game Over window
    window.fill((0, 0, 0))  # Black window

    # Text "Game Over"
    game_over_text = FONT_POINTS.render("GAME OVER", True, C_YELLOW)
    window.blit(game_over_text, (WIN_WIDTH / 2 - game_over_text.get_width() / 2, WIN_HEIGHT / 3))

    # Final score
    score_text = FONT_POINTS.render(f'Pontuação: {points}', True, C_ORANGE)
    window.blit(score_text, (WIN_WIDTH / 2 - score_text.get_width() / 2, WIN_HEIGHT / 2))

    # Restart or Exit
    line1 = FONT_POINTS.render("Pressione 'R' para Reiniciar", True, C_ORANGE)
    line2 = FONT_POINTS.render("ou 'Q' para Sair", True, C_ORANGE)
    window.blit(line1, (WIN_WIDTH / 2 - line1.get_width() / 2, WIN_HEIGHT / 1.5))
    window.blit(line2, (WIN_WIDTH / 2 - line2.get_width() / 2, WIN_HEIGHT / 1.3))

    pygame.display.flip()

    # User input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    return True
    return False


def main():
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.mixer.music.load('./assets/GameSound.mp3')
    pygame.mixer.music.play(-1)

    # Main loop
    while True:
        menu = Menu(window)
        selected_option = menu.run()

        if selected_option == 'NEW GAME':
            characters = [Character(230, 350)]
            floor = Floor(730)
            pipes = [Pipe(700)]
            tela = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            points = 0
            clock = pygame.time.Clock()

            running = True
            first_move = True

            while running:
                clock.tick(30)

                # Player interactions
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            for character in characters:
                                character.jump()

                # Movement of objects
                for character in characters:
                    character.move()
                    floor.move()

                add_pipes = False
                remove_pipes = []
                for pipe in pipes:
                    for i, character in enumerate(characters):
                        if pipe.clash(character):  # If collision
                            running = False  # Quit loop game
                            if game_over(window, points):  # Game Over
                                break  # Interrupts collisions verification

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
                    if (character.y + character.imgs[0].get_height()) > floor.y or character.y < 0:
                        running = False
                        if game_over(window, points):
                            break

                draw_window(window, characters, pipes, floor, points)

        # "EXIT", Game quit
        elif selected_option == 'EXIT':
            pygame.quit()
            quit()


if __name__ == '__main__':
    main()
