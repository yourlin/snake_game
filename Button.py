import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, location=[0, 0], width=100, height=100):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.width = width
        self.height = height
        # 缩放图片尺寸
        self.btn_surf = pygame.transform.scale(surf, [width, height])

    def draw(self, surf: pygame.surface):
    
        surf.blit(self.btn_surf,
                  [self.location[0], self.location[1]],
                  [0, 0, self.btn_surf.get_width(), self.btn_surf.get_height()])

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.location, [self.width, self.height])
