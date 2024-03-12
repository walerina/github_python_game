import unittest
from player import Player
import time
from tiles import *
from settings import *
from levels import Level
from enemy import Enemy

pygame.init()

def create_keys():
    return {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}

def create_player():
    global_player = pygame.sprite.GroupSingle()
    global_player.add(Player((0, 0)))
    return global_player.sprite

def create_screen():
    return pygame.display.set_mode((screen_width, screen_height))

def create_level(map = level_maps[0]):
    return Level(map, create_screen())

class Player_Test(unittest.TestCase):
    def test_apply_gravity(self):
        keys, player = create_keys(), create_player()
        player.apply_gravity()
        self.assertEqual(player.direction.y, player.gravity_speed)
        self.assertEqual(player.rect.y, player.gravity_speed)

    def test_right_moving(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_RIGHT] = True
        player.get_input(keys)
        self.assertEqual(player.direction.x, 1)

    def test_left_moving(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_LEFT] = True
        player.get_input(keys)
        self.assertEqual(player.direction.x, -1)

    # Прогнозирование ошибок
    def test_pressing(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_DOWN] = True
        player.get_input(keys)
        player.is_pressed = True
        keys[pygame.K_DOWN], keys[pygame.K_UP], y = False, True, player.rect.y
        player.get_input(keys)
        self.assertEqual(player.rect.y, y)

    def test_update(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_RIGHT] = True
        player.update(keys)
        self.assertEqual(player.rect.x, player.speed)

    #Прогнозирование ошибок
    def test_all_keys(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_UP] = True, True, True, True
        player.get_input(keys)
        self.assertEqual(player.direction.x, 1)

    #Переход состояний
    #0, 1, 2 - разогнутый, прыжок, согнутый
    #0 -> (up) -> 1
    def test_jumping(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_UP] = True
        player.get_input(keys)
        self.assertEqual(player.jump, player.jump_speed)
        time.sleep(0.1)
        self.assertEqual(player.jump, player.jump_speed)
        time.sleep(0.2)
        self.assertEqual(player.jump, player.gravity_speed)

    #1 -> (up) -> 1
    def test_jump_after_jumping(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_UP] = True
        player.get_input(keys)
        player.apply_gravity()
        self.assertEqual(player.rect.y, player.jump_speed)
        player.get_input(keys)
        self.assertEqual(player.rect.y, player.jump_speed)

    # 1 -> (down) -> 2
    def test_down_after_jumping(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_UP] = True
        player.get_input(keys)
        player.apply_gravity()
        y = player.rect.y
        keys[pygame.K_DOWN], keys[pygame.K_UP] = True, False
        self.assertEqual(player.rect.y, y)

    #0 -> (down) -> 2; 2 -> (down) -> 2
    def test_down_moving(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_DOWN], y = True, player.rect.y
        player.get_input(keys)
        self.assertEqual(player.rect.y, y + player.mh)
        player.get_input(keys)
        self.assertEqual(player.rect.y, y + player.mh)

    #2 -> (up) -> 0
    def test_unbending(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_DOWN] = True
        player.get_input(keys)
        keys[pygame.K_DOWN], keys[pygame.K_UP], y = False, True, player.rect.y
        player.get_input(keys)
        self.assertEqual(player.rect.y, y - player.mh)

    #2 -> (up) -> 1 (возможно только через разгиб)
    def test_double_up(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_DOWN] = True
        player.get_input(keys)
        keys[pygame.K_DOWN], keys[pygame.K_UP] = False, True
        player.get_input(keys)
        keys[pygame.K_UP] = False
        player.get_input(keys)
        keys[pygame.K_UP] = True
        player.get_input(keys)
        self.assertEqual(player.jump, player.jump_speed)

class Levels_test(unittest.TestCase):
    def test_destruct_usual(self):
        level = Level(level_maps[0], create_screen())
        level.tiles = [Tile((0, 0), 64)]
        level.destruct(level.tiles[0], create_keys())
        self.assertEqual(len(level.tiles), 1)

    def test_ignore_broken(self):
        level = Level(level_maps[0], create_screen())
        tile = Barrier_fragile((0, 0), 64)
        level.tiles = [tile]
        level.destruct(level.tiles[0], create_keys())
        self.assertEqual(len(level.tiles), 1)
        self.assertFalse(tile.broken)

    def test_destruct_broken(self):
        level, keys = create_level(), create_keys()
        tile = Barrier_fragile((0, 0), 64)
        level.tiles = [tile]
        keys[pygame.K_SPACE] = True
        level.destruct(level.tiles[0], keys)
        self.assertEqual(len(level.tiles), 0)
        self.assertTrue(tile.broken)

    def test_loose(self):
        level = create_level()
        level.player.sprite.healf = 0
        self.assertEqual(level.run(create_screen()), "loose")

    #Граничные значения: 599, 600
    def test_not_middle(self):
        level = create_level()
        level.player.sprite.rect.x = 599
        level.run(create_screen())
        self.assertFalse(level.on_middle)

    def test_middle(self):
        level = create_level()
        level.player.sprite.rect.x = 600
        level.run(create_screen())
        self.assertTrue(level.on_middle)

    def test_collide_win(self):
        level = create_level()
        level.player.sprite.rect.x, level.win.sprite.rect.x =  0, level.player.sprite.w - 1
        level.player.sprite.rect.y, level.win.sprite.rect.y = 0, 0
        self.assertEqual(level.run(create_screen()), "win")

    def test_running(self):
        level = create_level()
        level.player.sprite.rect.x, level.win.sprite.rect.x =  0, level.player.sprite.w - 1
        level.player.sprite.rect.y, level.win.sprite.rect.y = 0, level.player.sprite.h
        self.assertEqual(level.run(create_screen()), "running")

    def test_map_pressing(self):
        test_map = ['X',
                     'P',
                     ' '
                    'W']
        level = create_level(test_map)
        level.run(create_screen())
        self.assertTrue(level.player.sprite.is_pressed)

    def test_map_free(self):
        test_map = ['X',
                     ' ',
                     'P'
                    'W']
        level = create_level(test_map)
        level.player.sprite.direction.y = -0.5
        level.run(create_screen())
        self.assertFalse(level.player.sprite.is_pressed)

class Enemy_test(unittest.TestCase):
    def test_enemy_size(self):
        enemy = Enemy((0, 0))
        for level_map in level_maps:
            self.assertEqual(enemy.return_h(), len(level_map) * tile_size)
            self.assertEqual(enemy.return_w(), tile_size / 2)

    def test_appearing_enemy(self):
        level = create_level()
        level.enemy.sprite.direction.x, level.on_middle = 1, True
        level.run(create_screen())
        self.assertEqual(level.enemy.sprite.return_x(), 3)

    def test_collide_enemy(self):
        level = create_level()
        level.enemy.sprite.rect.x, level.player.sprite.rect.x =  0, level.enemy.sprite.w - 1
        level.run(create_screen())
        self.assertEqual(level.player.sprite.healf, 0)
