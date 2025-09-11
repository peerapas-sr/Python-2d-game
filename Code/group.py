from settings import *
class Allsprite(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
    def draw(self,surface):
        ground_sprite= [sprite for sprite in self if hasattr(sprite,'ground')]
        object_sprite = [sprite for sprite in self if not hasattr(sprite,'ground')]
        for layer in [ground_sprite,object_sprite]:
            for sprite in sorted(layer,key= lambda sprite:sprite.rect.centery):
                 surface.blits([(sprite.image,sprite.rect.topleft)])