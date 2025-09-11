from typing import Any
from settings import *
class player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collistion_sprites):
        super().__init__(groups)
        self.load_image()
        self.image = pygame.image.load(join('sprites','characters','Player','Player_idle_front','0.png')).convert_alpha()
        self.state,self.frames_index = 'right',0
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(0,0)
        self.shoot_direction = pygame.Vector2(0,0)
        self.hitbox_rect = self.rect.inflate(-20,-20)
        self.speed = 80
        self.collistion_sprites = collistion_sprites
        self.player_pos = self.rect.center
    #load animation
    def load_image(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('sprites','characters','Player','player_state', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        key = pygame.key.get_pressed()
        self.direction.x = key[pygame.K_d]-(key[pygame.K_a])
        self.direction.y = key[pygame.K_s]-(key[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()


    def shoot_input(self):
        key = pygame.key.get_pressed()
        self.shoot_direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])
        self.shoot_direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        if self.shoot_direction.length_squared() > 0:
            self.shoot_direction = self.shoot_direction.normalize()
    def screen_boundary_check(self):
        if self.hitbox_rect.left < 0:
            self.hitbox_rect.left = 0
        if self.hitbox_rect.right > WINDOW_WIDTH:
            self.hitbox_rect.right = WINDOW_WIDTH

        if self.hitbox_rect.top < 0:
            self.hitbox_rect.top = 0
        if self.hitbox_rect.bottom > WINDOW_HEIGHT:
            self.hitbox_rect.bottom = WINDOW_HEIGHT

    def move(self,dt):
        self.hitbox_rect.x += self.direction.x*self.speed*dt 
        self.collision('horizontal')
        self.screen_boundary_check()
        self.hitbox_rect.y += self.direction.y*self.speed*dt 
        self.collision('vertical')
        self.screen_boundary_check()
        
        self.rect.center=self.hitbox_rect.center
        self.player_pos = self.rect.center

    
    def collision(self, direction):
        for sprite in self.collistion_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def animate(self,dt):
        if self.direction.x != 0:
                self.state = 'right' if self.direction.x >0 else "left"
        if self.direction.y != 0:
                self.state = 'up' if self.direction.y<0 else 'down'
            
        self.animatetion = int(self.frames_index%len(self.frames[self.state]))

        self.frames_index += 5*dt if self.direction else 0

        self.image = self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]
    def update(self,dt):
        self.input()
        self.animate(dt)
        self.shoot_input()
        self.move(dt)
        
        
    

