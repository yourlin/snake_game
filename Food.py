import pygame


class Food(pygame.sprite.Sprite):
    bg_surf = pygame.image.load('./res/food.png')
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.size = 1.0
        

    def draw(self, surf: pygame.surface):
        transformed_surf = pygame.transform.scale(Food.bg_surf, [self.bg_surf.get_width()*self.size, self.bg_surf.get_height()*self.size])
        
        surf.blit(transformed_surf,
                  [self.location[0] + (Food.bg_surf.get_width() - transformed_surf.get_width()) / 2, 
                   self.location[1] + (Food.bg_surf.get_height() - transformed_surf.get_height()) / 2],
                  [0, 0, 25, 25])
