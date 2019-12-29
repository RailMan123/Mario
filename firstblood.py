import random

import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data2', name)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey((255, 255, 255))
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb2.png")
    image_boom = load_image("boom.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        x = 0
        y = 0
        while 1:
            x = random.randrange(width - self.image.get_size()[0])
            y = random.randrange(height - self.image.get_size()[1])
            self.rect.x = x
            self.rect.y = y
            if len(pygame.sprite.spritecollide(self, group, False)) == 1:
                break

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom
            self.rect.x -= 40
            self.rect.y -= 30


running = True
all_sprites = pygame.sprite.Group()

for _ in range(10):
    Bomb(all_sprites)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()