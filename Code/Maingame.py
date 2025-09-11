from settings import *
from Player import player
from Spritesfile import *
from random import randint , choice
from pytmx.util_pygame import load_pygame
from group import Allsprite

class game:
    def __init__(self):
        #game Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Amazing shooting slime game")
        global virtual_surface 
        virtual_surface = pygame.Surface((Virtual_WINDOW_WIDTH,Virtual_WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.shoot_direction = pygame.Vector2(0,0)
        #sprites
        self.collistion_sprite = pygame.sprite.Group()
        self.all_sprite = Allsprite()
        self.bullet_sprite = pygame.sprite.Group()
        self.enemy_sprite = pygame.sprite.Group()

        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 220   
        #event timer enemy
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1000)
        self.spawn_position = []
        #score
        self.score = 0
        self.load_image()
        self.setup()
        self.font = pygame.font.Font(None, 70)
        self.small_font = pygame.font.Font(None,20)
        # audio 
        self.shoot_sound = pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('audio','ImpactSlime.mp3'))
        self.music = pygame.mixer.Sound(join('audio','retro-gaming-248421.mp3'))
        self.music.set_volume(0.5)
        self.gameover_sound = pygame.mixer.Sound(join('audio','mixkit-player-losing-or-failing-2042.wav'))
        self.gameover_sound.set_volume(0.2)
        self.music.play(loops = -1)

    def display_score(self):
        self.score_text = self.font.render(f"Score: {self.score}", True, 'white')
        self.display_surface.blit(self.score_text,(180,50))
    

    def setup(self):
        map = load_pygame(join('Maps','MapForProjects.tmx'))
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        for x,y,image in map.get_layer_by_name('Object').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        for obj in map.get_layer_by_name('Collistion'):
            CollistionSprite((obj.x,obj.y), pygame.Surface((obj.width,obj.height)),(self.collistion_sprite))
        for obj in map.get_layer_by_name('Entities'):
            #Spawn Player
            if obj.name == 'Player':
                self.player = player((obj.x,obj.y),self.all_sprite,self.collistion_sprite)
            #spawn enemy
            else:
                enemy((obj.x,obj.y),self.enemy_frames_slime.values(),self.player,(self.all_sprite,self.enemy_sprite),self.collistion_sprite)
    def load_image(self):
        self.Ogbullet_surf = pygame.image.load(join('sprites','particles','bullet.png')).convert_alpha()
        self.bullet_surf = pygame.transform.scale_by(self.Ogbullet_surf,0.25)
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('sprites','characters','Player','player_state', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def shoot_input(self):
        pos = self.player.rect.center + self.shoot_direction*17
        key = pygame.key.get_pressed()
        self.shoot_direction.x = int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT])
        self.shoot_direction.y = int(key[pygame.K_DOWN]) - int(key[pygame.K_UP])
        self.shoot_direction = self.shoot_direction.normalize()if self.shoot_direction else self.shoot_direction
        if (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN]) and self.can_shoot :
            bullet(pos,self.bullet_surf,self.shoot_direction,(self.all_sprite,self.bullet_sprite))
            self.shoot_sound.play()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    def gun_timer(self):
        if not self.can_shoot:
            curren_Time = pygame.time.get_ticks()
            if curren_Time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True
                
    def bullet_collision(self):
        if self.bullet_sprite:
            for bullet in self.bullet_sprite:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprite, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    self.update_score()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprite, False, pygame.sprite.collide_mask):
            self.game_over = True
            self.gameover_sound.play()
            self.music.stop()

    def display_score(self):
        self.score_text = self.font.render(f"Score: {self.score}", True, 'white')
        
        self.display_surface.blit(self.score_text,(180,50))
    def update_score(self):
        self.score += 1
    def display_tutorial(self):
        self.tuto_text = self.small_font.render("W,A,S,D to walk Arrow keys to shoot",True,'white')
        self.text = self.small_font.render("Made by Peerapas Sriwangrach 673040397-6 Coe34",True,'white')
        self.display_surface.blit(self.text,(790,670))
        self.display_surface.blit(self.tuto_text,(880,50))
    def handle_game_over(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.restart_game()
    def display_game_over(self):
        game_over_text = self.font.render("Game Over", True, 'red')
        restart_text = self.font.render("Press Enter to Restart", True, 'white')
        self.display_surface.blit(game_over_text, (WINDOW_WIDTH // 2 - 130, WINDOW_HEIGHT // 2 - 50))
        self.display_surface.blit(restart_text, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 + 50))
    def restart_game(self):
        self.__init__()

    def run(self):
        while self.running:
            dt = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    enemy(choice(self.spawn_position),self.player,(self.all_sprite,self.enemy_sprite),self.collistion_sprite)
            if self.game_over:
                self.display_game_over()
                self.handle_game_over()
                
            else:
                #draw
                virtual_surface.fill("black")
                self.all_sprite.draw(virtual_surface)
                pygame.draw.rect(virtual_surface, 'black', pygame.Rect(480,0, 100, 600))
                pygame.draw.rect(virtual_surface, 'black', pygame.Rect(0,320, 600, 60))
                self.scaled_surface = pygame.transform.scale(virtual_surface, (WINDOW_WIDTH,WINDOW_HEIGHT))
                self.display_surface.blit(self.scaled_surface, (160,45))
                #update
                self.all_sprite.update(dt)
                self.shoot_input()
                self.gun_timer()
                self.bullet_collision()
                self.display_score()
                self.player_collision()
                self.display_tutorial()
            pygame.display.update()
        pygame.quit()

    def setup(self):
        map = load_pygame(join('Maps','MapForProjects.tmx'))
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        for x,y,image in map.get_layer_by_name('Object').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        for obj in map.get_layer_by_name('Collistion'):
            CollistionSprite((obj.x,obj.y), pygame.Surface((obj.width,obj.height)),(self.collistion_sprite))
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = player((obj.x, obj.y), self.all_sprite, self.collistion_sprite)
            else:
                self.spawn_position.append((obj.x,obj.y))

            






if __name__ == '__main__':
    Game = game()
    Game.run()

