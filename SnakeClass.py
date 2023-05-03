import pygame
from enum import Enum


class SnakeDirect(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class SnakeClass(pygame.sprite.Sprite):
    head_surf_list: list = []
    body_surf = pygame.image.load('./res/body.png')

    def __init__(self, location, init_length=5):
        pygame.sprite.Sprite.__init__(self)
        self.init_length = init_length
        self.body_size = 25
        self.body = [location]
        self.direct = SnakeDirect.RIGHT

        if len(SnakeClass.head_surf_list) == 0:
            SnakeClass.head_surf_list.append(pygame.image.load('./res/up.png'))
            SnakeClass.head_surf_list.append(pygame.image.load('./res/right.png'))
            SnakeClass.head_surf_list.append(pygame.image.load('./res/down.png'))
            SnakeClass.head_surf_list.append(pygame.image.load('./res/left.png'))
        
        self.head_forward_surf : pygame.surface = SnakeClass.head_surf_list[self.direct.value]

        for i in range(1, self.init_length):
            self.body.append([self.body[i-1][0],
                              self.body[i-1][1]+self.body_size])
        self.eat_sound = pygame.mixer.Sound('./res/eat.wav')
        
        
    def move(self):
        self.body.pop()
        if self.direct == SnakeDirect.UP:
            self.body.insert(0, [self.body[0][0],
                                 self.body[0][1] - self.body_size])

        if self.direct == SnakeDirect.LEFT:
            self.body.insert(0, [self.body[0][0] - self.body_size,
                                 self.body[0][1]])
        if self.direct == SnakeDirect.DOWN:
            self.body.insert(0, [self.body[0][0],
                             self.body[0][1] + self.body_size])
        if self.direct == SnakeDirect.RIGHT:
            self.body.insert(0, [self.body[0][0] + self.body_size,
                                 self.body[0][1]])

    def draw(self, surf: pygame.Surface):
        for i in range(len(self.body)):
            if i == 0:
                self.head_forward_surf = SnakeClass.head_surf_list[self.direct.value]
                surf.blit(self.head_forward_surf,
                          [self.body[i][0],
                           self.body[i][1],self.body_size, self.body_size],
                          [0, 0, 25, 25])
            else:
                surf.blit(SnakeClass.body_surf,
                          [self.body[i][0], self.body[i][1],self.body_size, self.body_size],
                          [0, 0, 25, 25])

    def eat(self):
        # 通过最后2节身体的位置，确定新增身体的位置
        a = self.body[-1]
        b = self.body[-2]
        diff = [a[0]-b[0], a[1] - b[1]]
        new_body = [a[0] + diff[0], b[1] + diff[1]]
        
        self.body.append(new_body)
        self.eat_sound.play()