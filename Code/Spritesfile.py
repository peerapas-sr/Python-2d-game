from typing import Any

from settings import *
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground= True

class CollistionSprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf,(Virtual_WINDOW_WIDTH/WINDOW_WIDTH ))
        self.rect = self.image.get_frect(topleft=pos)

class bullet(pygame.sprite.Sprite):
    def __init__(self,pos,surf,direction,groups):
        super().__init__(groups)
        self.direction = direction
        self.image = surf
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 200
        self.distance = 150
        self.player_direction = pygame.Vector2(0,0)

        self.rect = self.image.get_frect(center = pos)


        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 2000
        
    def update(self,dt):
        self.rect.center += self.direction*dt*self.speed
        if pygame.time.get_ticks()-self.spawn_time >= self.life_time:
            self.kill()


class enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, collision_sprite):
        super().__init__(groups)
        self.collision_sprite = collision_sprite
        self.image = pygame.image.load(join('sprites', 'characters', 'Enemy', 'SlimeSprite', '0.png'))
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.direction = pygame.Vector2()
        self.enemy_speed = 50
        self.player = player
        self.update_timer = 500  # 0.5 seconds
        self.last_update_time = pygame.time.get_ticks()
        self.target_pos = self.player.rect.center 
        #timer
        self.death_duration = 100
        self.death_time = 0
    def move_enemy_toward_position(self, dt):
        target_pos = pygame.Vector2(self.target_pos)
        enemy_pos = pygame.Vector2(self.hitbox_rect.center)
        if self.direction !=0:
            self.direction = (target_pos - enemy_pos).normalize()
        self.hitbox_rect.x += self.direction.x * self.enemy_speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.enemy_speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
            
    def update_target_position(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_timer:
            self.target_pos = self.player.rect.center
            self.last_update_time = current_time

    def load_image(self):
        self.Ogbullet_surf = pygame.image.load(join('sprites','particles','bullet.png')).convert_alpha()
        self.bullet_surf = pygame.transform.scale_by(self.Ogbullet_surf,0.25)
        self.enemy_frames_slime = {'idle':[]}  
        for state in self.enemy_frames_slime.keys():
            for folder_path,sub_folders,file_name in walk(join('sprites','characters','Enemy','SlimeSprite')):
                if file_name:
                    for file_name in sorted(file_name, key = lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.enemy_frames_slime[state].append(surf)


    def collision(self, direction):
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom      
    
    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.image).to_surface()
        surf.set_colorkey("black")

        self.image=surf
    def death_timer(self):
        if pygame.time.get_ticks()-self.death_time >= self.death_duration:
            self.kill()
    def update(self, dt):
        if self.death_time == 0:

            self.update_target_position()
            self.move_enemy_toward_position(dt)
            self.rect.center = self.hitbox_rect.center
        else:
            self.death_timer()