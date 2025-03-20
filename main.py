import pygame
import os
import random

W_WIDTH = 500
W_HEIGHT = 800

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))
IMAGES_CHARACTER = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird3.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'SuperBento2.png')))
]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('ariel', 50)


class Character:
    img = IMAGES_CHARACTER
    # Rotation animations
    rot_max = 25
    rot_speed = 20
    time_anim = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.img_position = self.img[0]

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
        # Sequence of images
        self.img_position += 1

        if self.img_position < self.time_anim:
            self.img = self.img[0]
        elif self.img_position < self.time_anim * 2:
            self.img = self.img[1]
        elif self.img_position < self.time_anim * 3:
            self.img = self.img[2]
        elif self.img_position < self.time_anim * 4:
            self.img = self.img[1]
        elif self.img_position >= self.time_anim * 4 + 1:
            self.img = self.img[0]
            self.img_position = 0

        # Down image
        if self.angle <= -80:
            self.img = self.img[1]
            self.img_position = self.time_anim * 2

        # Draw image
        rot_img = pygame.transform.rotate(self.img, self.angle)
        pos_center_img = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rot_img.get_rect(center=pos_center_img)
        window.blit(rot_img, rectangle.topleft)


class Pipe:
    pass


class Floor:
    pass
