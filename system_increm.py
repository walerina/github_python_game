import unittest
from menu import Menu
from mess_window import *
from player import Player
from tiles import *
from settings import *
from levels import Level
from enemy import Enemy
from pause import Pause
from unittest.mock import patch

pygame.init()
clock = pygame.time.Clock()
menu = Menu()
mess_window = Mess_window()

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

class System_testting(unittest.TestCase):
#Прошёл уровень 3 и продолжил с 0
    def test_pass_3level_and_continue0(self):
        Pause.pre_quit(2)
        menu.last_passed_level=2

        actions = [
                   ({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 0.03),
                   ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 1)]
        test_level_map = [
            'XX                   W      ',
            'XX                   W      ',
            'XXX                  W      ',
            'XXXP                 WXX    ',
            'X                    W   X   ',
            'XXXX                 WBXX   ',
            'XXXX                 WB X   ',
            'XXX                  WXX    ',
            'XXX EWEEEEEEEEEEEE  XXX   ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ']

        menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 2, actions, test_level_map,
                     inc_time=10)
        self.assertEqual(menu.last_passed_level, 0)

if __name__ == '__main__':
    unittest.main()
