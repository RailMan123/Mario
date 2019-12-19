FPS = 50
import pygame
import os
import sys

pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
WIDTH, HEIGHT = 550, 550
screen.fill((255, 255, 255))
player = None
clock = pygame.time.Clock()
running = True
maps = ['map.txt', 'map2.txt', 'map3.txt']
mapname = sys.argv[1]




def terminate():
    pygame.quit()
    sys.exit()


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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "data2/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boxes = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(boxes)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self):
        for sprite in all_sprites:
            camera.apply(sprite)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')
tile_width = tile_height = 50


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


screen.fill((255, 255, 255))
player, level_x, level_y = generate_level(load_level(mapname))

camera = Camera()
camera.update(player)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == 276:
                player.rect.x -= 50
                if pygame.sprite.spritecollide(player, boxes, False) == []:
                    pass
                else:
                    player.rect.x += 50
            elif event.key == 275:
                player.rect.x += 50
                if pygame.sprite.spritecollide(player, boxes, False) == []:
                    pass
                else:
                    player.rect.x -= 50
            elif event.key == 273:
                player.rect.y -= 50
                if pygame.sprite.spritecollide(player, boxes, False) == []:
                    pass
                else:
                    player.rect.y += 50
            elif event.key == 274:
                player.rect.y += 50
                if pygame.sprite.spritecollide(player, boxes, False) == []:
                    pass
                else:
                    player.rect.y -= 50

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()