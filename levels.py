from tiles import Tile, Barrier_fragile, Barrier_enemy, Barrier
from player import Player
from enemy import Enemy
from mess_window import *

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.oldY = 0
        self.on_middle = False
        self.is_near_destruction = False
        self.is_near_destruction_now = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.GroupSingle()
        self.win = pygame.sprite.GroupSingle()
        enemy_sprite = Enemy((0, 0))
        self.enemy.add(enemy_sprite)
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                y = row_index * tile_size
                x = column_index * tile_size
                if column == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if column == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if column == 'F':
                    tile = Barrier_fragile((x, y), tile_size)
                    self.tiles.add(tile)
                if column == 'E':
                    tile = Barrier_enemy((x, y), tile_size)
                    self.tiles.add(tile)
                if column == 'B':
                    tile = Barrier((x, y), tile_size)
                    self.tiles.add(tile)
                if column == 'W':
                    win  = Tile((x, y), tile_size)
                    self.win.add(win)    

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 7

    def detect_hor_collision(self, player, sprite):
        if sprite.rect.colliderect(player):
            if player.rect.left <= sprite.rect.right and player.rect.right > sprite.rect.right:
                return True
            return player.rect.right >= sprite.rect.left and player.rect.left < sprite.rect.left
        return False

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        coll_rect = pygame.Rect(player.rect.left - 1, player.rect.top, player.rect.width + 2, player.rect.height)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(coll_rect):
                self.destruct(sprite)
                self.get_hurt(sprite, player)
                if coll_rect.left <= sprite.rect.right and coll_rect.right > sprite.rect.right: #если преграда слева
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                if coll_rect.right >= sprite.rect.left and coll_rect.left < sprite.rect.left: #если преграда справа
                    if player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        is_smth_up = False
        dist = 7
        coll_rect = pygame.Rect(player.rect.left, player.rect.top - dist - 1, player.rect.width, player.rect.height + 2)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(coll_rect):
                self.destruct(sprite)
                self.get_hurt(sprite, player)
                if coll_rect.top <= sprite.rect.bottom and coll_rect.top > sprite.rect.top: #если преграда сверху
                    is_smth_up = True
                    if player.direction.y < 0: #если во время прыжка
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.jump = player.gravity_speed
                if coll_rect.bottom >= sprite.rect.top and coll_rect.bottom < sprite.rect.bottom: #если преграда снизу
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.is_jump = False
        player.is_pressed = is_smth_up

    def destruct(self, tile, keys = {}):
        if keys == {}:
            keys = pygame.key.get_pressed()
        if tile.__class__ == Barrier_fragile and keys[pygame.K_SPACE]:
            tile.broke()
            self.tiles.remove(tile)

    def get_hurt(self, tile, player):
        if tile.__class__ == Barrier_enemy:
            self.is_near_destruction_now = True
            if not self.is_near_destruction:
                player.healf -= 5
                if player.healf < 0:
                    player.healf = 0
                self.is_near_destruction = True

    def run(self, screen, level_events = [], return_player = False, inc_time = 1):
      
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        
        self.win.update(self.world_shift)
        self.win.draw(self.display_surface)

        self.player.update(level_events, inc_time)
        #print(self.player.sprite.action_number)
        #print(len(level_events))
        if self.player.sprite.action_number == len(level_events) and return_player:
            print("return")
            return self.player.sprite
        self.scroll_x()
        player = self.player.sprite
        if player.healf == 0:
            return ("loose")
        self.is_near_destruction_now = False
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        if not self.is_near_destruction_now:
            self.is_near_destruction = False
        self.player.draw(self.display_surface)
        if player.rect.x >= 600:
            self.on_middle = True

        font = pygame.font.SysFont(None, 100)
        shkala = str(player.healf) + "/11"
        text = font.render(shkala, True, (255, 0, 0))
        text_rect = text.get_rect(center=pygame.Rect(950, -300, 250, 700).center)
        screen.blit(text, text_rect)

        if self.on_middle:
            self.enemy.update()
            self.enemy.draw(self.display_surface)

        if player.rect.colliderect(self.enemy.sprite.rect):
            player.healf = 0

        if player.rect.colliderect(self.win.sprite.rect):
            return "win"
        else:
            return "running"