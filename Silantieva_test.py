import unittest
from levels import *
from tiles import *
from player import *

pygame.init()
screen_width = 1200
screen_height = len(level_map) * tile_size
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0, 0, 139))

test_map1 = [' XX']
test_map2 = [' PP']
test_map3 = [' FF']
test_map4 = [' BB']
test_map5 = [' EE']
test_map6 = [' WW']
test_map7 = [' P   ']
test_map8 = [' PE  ']
test_map9 = [' P   ',
             '     ',
             ' X   ']
level_test = [test_map1, test_map2, test_map3, test_map4, test_map5, test_map6, test_map7, test_map8, test_map9]

class Enemy_Test (unittest.TestCase):
    def test_enemy_update (self):
        enemy_sprite = Enemy((0, 0))
        enemy_sprite.update()
        self.assertEqual(enemy_sprite.rect.x, 3)

class Levels_test2(unittest.TestCase):
    ##level_setup
    def test_level_setup_tile_location (self):
        level = Level(level_test[0], screen)
        level.setup_level(level_test[0])
        spritelist = level.tiles.sprites()
        sprite = spritelist[1]
        self.assertEqual(sprite.rect.x, 128)
        self.assertEqual(sprite.rect.y, 0)

    def test_level_setup_tile (self):
        level = Level(level_test[0], screen)
        level.setup_level(level_test[0])
        spritelist = level.tiles.sprites()
        sprite = spritelist[1]
        self.assertTrue(type(sprite) is Tile)

    def test_level_setup_player (self):
        level = Level(level_test[1], screen)
        level.setup_level(level_test[1])
        spritelist = level.player.sprites()
        sprite = spritelist[0]
        self.assertTrue(type(sprite) is Player)

    def test_level_setup_barrier_fragile (self):
        level = Level(level_test[2], screen)
        level.setup_level(level_test[2])
        spritelist = level.tiles.sprites()
        sprite = spritelist[1]
        self.assertTrue(type(sprite) is Barrier_fragile)

    def test_level_setup_barrier (self):
        level = Level(level_test[3], screen)
        level.setup_level(level_test[3])
        spritelist = level.tiles.sprites()
        sprite = spritelist[1]
        self.assertTrue(type(sprite) is Barrier)

    def test_level_setup_barrier_enemy (self):
        level = Level(level_test[4], screen)
        level.setup_level(level_test[4])
        spritelist = level.tiles.sprites()
        sprite = spritelist[1]
        self.assertTrue(type(sprite) is Barrier_enemy)

    def test_level_setup_win (self):
        level = Level(level_test[5], screen)
        level.setup_level(level_test[5])
        spritelist = level.win.sprites()
        sprite = spritelist[0]
        self.assertTrue(type(sprite) is Tile)

    ##эквивалентное разделение
    ##scroll_x
    def test_scroll_x_direction_left (self):
        level = Level(level_test[6], screen)
        level.player.sprite.rect.centerx = 200
        level.player.sprite.direction.x = -1
        level.scroll_x()
        self.assertEqual(level.world_shift, 8)

    def test_scroll_x_direction_right (self):
        level = Level(level_test[6], screen)
        level.player.sprite.rect.centerx = 1000
        level.player.sprite.direction.x = 1
        level.scroll_x()
        self.assertEqual(level.world_shift, -8)

    def test_scroll_x_direction_none (self):
        level = Level(level_test[6], screen)
        level.player.sprite.rect.centerx = 300
        level.player.sprite.direction.x = 0
        level.scroll_x()
        self.assertEqual(level.world_shift, 0)

    ##detect_hor_collision
    def test_detect_hor_collision_none_right (self):
        level = Level(level_test[7], screen)
        player = Player((0, 0))
        tile = Tile((31, 0), 64)
        self.assertTrue(level.detect_hor_collision(player, tile))

    def test_detect_hor_collision_none_left (self):
        level = Level(level_test[7], screen)
        player = Player((63, 0))
        tile = Tile((0, 0), 64)
        self.assertTrue(level.detect_hor_collision(player, tile))

    def test_detect_hor_collision_side (self):
        level = Level(level_test[7], screen)
        player = Player((64, 0))
        tile = Tile((0, 0), 64)
        self.assertFalse(level.detect_hor_collision(player, tile))

    ##таблица
    ##horizontal_movement_collision
    def test_horizontal_movement_collision_none (self):
        level = Level(level_test[7], screen)
        spritelist = level.tiles.sprites()
        sprite = spritelist[0]
        level.horizontal_movement_collision()
        self.assertFalse(level.is_near_destruction_now)

    def test_horizontal_movement_collision_no_action (self):
        level = Level(level_test[7], screen)
        level.player.sprite.rect.left += 128
        spritelist = level.tiles.sprites()
        sprite = spritelist[0]
        level.horizontal_movement_collision()
        self.assertTrue(level.is_near_destruction_now)

    def test_horizontal_movement_collision_side (self):
        level = Level(level_test[7], screen)
        level.player.sprite.rect.x += 34
        spritelist = level.tiles.sprites()
        sprite = spritelist[0]
        level.horizontal_movement_collision()
        self.assertFalse(level.player.sprite.rect.right == sprite.rect.left)

    def test_horizontal_movement_collision_side_directed (self):
        level = Level(level_test[7], screen)
        level.player.sprite.rect.x += 33
        level.player.sprite.direction.x = 0.5
        spritelist = level.tiles.sprites()
        sprite = spritelist[0]
        level.horizontal_movement_collision()
        self.assertTrue(level.player.sprite.rect.right == sprite.rect.left)
        level.player.sprite.direction.x = -0.5
        level.horizontal_movement_collision()
        self.assertFalse(level.player.sprite.rect.right == sprite.rect.left)

    ##метод граничных значений
    ##vertical_movement_collision
    def test_vertical_movement_collision_none (self):
        level = Level(level_test[7], screen)
        level.vertical_movement_collision()
        self.assertFalse(level.player.sprite.is_pressed)

    def test_vertical_movement_collision_bottom (self):
        level = Level(level_test[8], screen)
        level.player.sprite.rect.y += 32
        spritelist = level.tiles.sprites()
        sprite = spritelist[0]
        level.vertical_movement_collision()
        self.assertTrue(level.player.sprite.rect.bottom == sprite.rect.top)
        self.assertFalse(level.player.sprite.is_pressed)

    def test_vertical_movement_collision_bottom_directed (self):
        level = Level(level_test[8], screen)
        level.player.sprite.rect.y += 32
        level.player.sprite.direction.y = 0.5
        level.vertical_movement_collision()
        self.assertTrue(level.player.sprite.direction.y == 0)
        self.assertFalse(level.player.sprite.is_pressed)

    ##get hurt
    def test_get_hurt_no_enemy (self):
        level = Level(level_test[7], screen)
        level.get_hurt(Tile((0, 0), 64), level.player.sprite)
        self.assertFalse(level.is_near_destruction_now)

    def test_get_hurt_barrier_enemy (self):
        level = Level(level_test[7], screen)
        level.get_hurt(Barrier_enemy((0, 0), 64), level.player.sprite)
        self.assertTrue(level.is_near_destruction_now)
        self.assertTrue(level.is_near_destruction)

    def test_get_hurt_double_call (self):
        level = Level(level_test[7], screen)
        level.get_hurt(Barrier_enemy((0, 0), 64), level.player.sprite)
        level.get_hurt(Barrier_enemy((0, 0), 64), level.player.sprite)
        self.assertEqual(level.player.sprite.healf, 6)

    def test_get_hurt_loss (self):
        level = Level(level_test[7], screen)
        level.player.sprite.healf = 4
        level.get_hurt(Barrier_enemy((0, 0), 64), level.player.sprite)
        self.assertEqual(level.player.sprite.healf, 0)


