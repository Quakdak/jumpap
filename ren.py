from pygame.locals import *
import os
import sys
import random
import pygame


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('JumpAp')
pygame.display.flip()

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Main_Menu:
    background = load_image('background.jpg')

    def __init__(self):
        self.screen = screen
        self.font = pygame.font.SysFont("Halvetica", 40)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    Gameplay().play()
            self.screen.blit(self.font.render(str('Для начала игры нажмите Q'), -1, (0, 0, 0)), (200, 210))
            self.screen.blit(self.font.render(str('Для просмотра таблицы лидеров надмите W'), -1, (0, 0, 0)), (100, 300))
            pygame.display.flip()



class Gameplay:
    default_platform = load_image('platform_green.png')
    moving_platform = load_image('platform_blue.png')
    breaking_platform = load_image('platform_brown.png')
    broke_platform = load_image('platform_brown_2.png')
    doodle_looking_left = load_image('doodle.png')
    doodle_looking_right = load_image('doodle_2.png')
    doodle_jumping_left = load_image('doodle_3.png')
    doodle_jumping_right = load_image('doodle_4.png')
    boost = load_image('boost.png')
    used_boost = load_image('used_boost.png')
    background = load_image('background.jpg')

    def __init__(self):
        self.default_platform = Gameplay.default_platform
        self.moving_platform = Gameplay.moving_platform
        self.breaking_platform = Gameplay.breaking_platform
        self.broke_platform = Gameplay.broke_platform
        self.doodle_looking_left = Gameplay.doodle_looking_left
        self.doodle_looking_right = Gameplay.doodle_looking_right
        self.doodle_jumping_left = Gameplay.doodle_jumping_left
        self.doodle_jumping_right = Gameplay.doodle_jumping_right
        self.boost = Gameplay.boost
        self.used_boost = Gameplay.used_boost
        pygame.font.init()
        self.font = pygame.font.SysFont("Halvetica", 40)
        self.boosts = []
        self.cam_pos = 0
        self.higth = 600
        self.pl_pos_array = [[400, 500, 0, 0]]
        self.default_pl_heigth = self.default_platform.get_height()
        self.default_pl_width = self.default_platform.get_width()
        self.doodle_r1_w = self.doodle_looking_right.get_width()
        self.doodle_r1_h = self.doodle_looking_right.get_height()
        self.boost_w = self.boost.get_width()
        self.boost_h = self.boost.get_height()
        self.doodle_move = 0
        self.trend = 0
        self.screen = screen
        self.gr = 0
        self.up = 0
        self.doodle_pos_x = 400
        self.doodle_pos_y = 400
        self.record = 0



    def Platform_spawn(self):
        while self.higth > -100:
            y = random.randint(0, 1000)
            x = random.randint(0, 700)
            if y < 800:
                y = 0
            elif y < 900:
                y = 1
            else:
                y = 2
            self.pl_pos_array.append([x, self.higth, y, 0])
            self.higth = self.higth - 50


    def Platform_change(self):
        for element in self.pl_pos_array:
            doodle = pygame.Rect(self.doodle_pos_x, self.doodle_pos_y, self.doodle_r1_w - 10, self.doodle_r1_h)
            plat = pygame.Rect(element[0], element[1], self.default_pl_width - 10, self.default_pl_heigth)
            if plat.colliderect(doodle):
                if self.doodle_pos_y < (element[1] - self.cam_pos):
                    if self.gr:
                        if element[2] != 2:
                            self.up = 15
                            self.gr = 0
                        else:
                            element[-1] = 1
            if element[2] == 1:
                if element[-1] == 1:
                    element[0] += 5
                    if element[0] > 550:
                        element[-1] = 0
                else:
                    element[0] -= 5
                    if element[0] <= 0:
                        element[-1] = 1

    def Platform_show(self):
        for el in self.pl_pos_array:
            ex = self.pl_pos_array[1][1] - self.cam_pos
            if ex > 600:
                y = random.randint(0, 1000)
                if y < 800:
                    y = 0
                elif y < 900:
                    y = 1
                else:
                    y = 2

                self.pl_pos_array.append([random.randint(0, 700), self.pl_pos_array[-1][1] - 50, y, 0])
                pos = self.pl_pos_array[-1]
                ex = random.randint(0, 1000)
                if ex > 900 and y == 0:
                    self.boosts.append([pos[0], pos[1] - 25, 0])
                self.pl_pos_array.pop(0)
                self.record += 100
            if el[2] == 0:
                self.screen.blit(self.default_platform, (el[0], el[1] - self.cam_pos))
            elif el[2] == 1:
                self.screen.blit(self.moving_platform, (el[0], el[1] - self.cam_pos))
            elif el[2] == 2:
                if not el[3]:
                    self.screen.blit(self.breaking_platform, (el[0], el[1] - self.cam_pos))
                else:
                    self.screen.blit(self.broke_platform, (el[0], el[1] - self.cam_pos))

        for e in self.boosts:
            if e[-1]:
                self.screen.blit(self.used_boost, (e[0], e[1] - self.cam_pos))
            else:
                self.screen.blit(self.boost, (e[0], e[1] - self.cam_pos))
            if pygame.Rect(e[0], e[1], self.boost_w, self.boost_h).colliderect(
                    pygame.Rect(self.doodle_pos_x, self.doodle_pos_y, self.doodle_r1_w, self.doodle_r1_h)):
                self.up = 50
                self.cam_pos -= 50


    def Doodle(self):
        if not self.up:
            self.doodle_pos_y += self.gr
            self.gr += 1
        elif self.up:
            self.doodle_pos_y -= self.up
            self.up -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.doodle_move < 10:
                self.doodle_move += 1
            self.trend = 0

        elif key[K_LEFT]:
            if self.doodle_move > -10:
                self.doodle_move -= 1
            self.trend = 1
        else:
            if self.doodle_move > 0:
                self.doodle_move -= 1
            elif self.doodle_move < 0:
                self.doodle_move += 1
        if self.doodle_pos_x > 850:
            self.doodle_pos_x = -50
        elif self.doodle_pos_x < -50:
            self.doodle_pos_x = 850
        self.doodle_pos_x += self.doodle_move
        if self.doodle_pos_y - self.cam_pos <= 200:
            self.cam_pos -= 10
        if not self.trend:
            if self.up:
                self.screen.blit(self.doodle_jumping_right, (self.doodle_pos_x, self.doodle_pos_y - self.cam_pos))
            else:
                self.screen.blit(self.doodle_looking_right, (self.doodle_pos_x, self.doodle_pos_y - self.cam_pos))
        else:
            if self.up:
                self.screen.blit(self.doodle_jumping_left, (self.doodle_pos_x, self.doodle_pos_y - self.cam_pos))
            else:
                self.screen.blit(self.doodle_looking_left, (self.doodle_pos_x, self.doodle_pos_y - self.cam_pos))


    def play(self):
        clock = pygame.time.Clock()
        self.Platform_spawn()
        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.doodle_pos_y - self.cam_pos > 700:
                self.cam_pos = 0
                self.record = 0
                self.boosts = []
                self.pl_pos_array = [[400, 500, 0, 0]]
                self.Platform_spawn()
                self.doodle_pos_x = 400
                self.doodle_pos_y = 400
            self.screen.blit(self.font.render(str(self.record), -1, (0, 0, 0)), (25, 25))
            self.Platform_show()
            self.Doodle()
            self.Platform_change()
            pygame.display.flip()


Main_Menu().run()