import pygame
from Button import Button

class Opening(pygame.sprite.Sprite):
    bg_surf = pygame.image.load('./res/bg.png')
    logo_suf = pygame.image.load('./res/pygame_tiny.png')

    def __init__(self, location,font, width=800, height=800, crop_y=0):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.width = width
        self.height = height
        self.crop_y = crop_y
        self.display_button = False
        self.font = font
        self.play_btn = None

    def draw(self, surf: pygame.surface):
        resized_height = self.width / Opening.bg_surf.get_width()  * \
            Opening.bg_surf.get_height()
        transformed_surf = pygame.transform.scale(
            Opening.bg_surf, [self.width, resized_height])
        surf.blit(transformed_surf, self.location, [
                  0, self.crop_y, self.width, self.height])
        if self.display_button:
            self.play_btn = Button(pygame.image.load('./res/play.png'),
                    [(self.width - 100) / 2, self.height*0.6],
                    100, 100)
            self.play_btn.draw(surf)
        
            surf.blit(Opening.logo_suf, [(self.width - Opening.logo_suf.get_width()) / 2,
                            (self.height - Opening.logo_suf.get_height()) / 2])
            
            title_surf = self.font.render(('Greedy Snake'), 1, (0, 0, 0))
            title_pos = [(self.width - title_surf.get_width()) / 2,
                            (self.height - title_surf.get_height()) / 2  - 100]
            surf.blit(title_surf, title_pos)
