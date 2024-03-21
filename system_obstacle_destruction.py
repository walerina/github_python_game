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
import json

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
    newlevel = Level(map, create_screen())
    newlevel.display_surface = create_screen()
    newlevel.setup_level = map
    newlevel.world_shift = 1
    newlevel.oldY = 0
    newlevel.on_middle = False
    return newlevel

def pre_quit(last_passed_level):
        with open('game_data.txt','w') as file:
            json.dump(last_passed_level,file)
        with open('game_data.txt') as file:
            return json.load(file)

clock = pygame.time.Clock()
pre_quit(2)
menu = Menu()
mess_window = Mess_window()

class System_testting(unittest.TestCase):
#Пачка 3 Юля:
#Прошёл уровень 1 и продолжил из победы со 2
#Прошёл уровень 1 вышел из игры и продолжил со 2

#Пользователь продолжил игру, дошел до разрушаемого препятствия и разрушил его
    def test_obstacle_destruction(self):
        pre_quit(1)
        actions = [
            ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: True,
              pygame.K_SPACE: False}, 0.01),
            ({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: False}, 0.03),
            ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: True}, 0.01),
            ({pygame.K_RIGHT: False, pygame.K_LEFT: True, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: False}, 0.01),
            ({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: False}, 0.03)
            ]
        test_level_map = [
        'XX                          ',
        'XX                          ',
        'XXX B                       ',
        'XXXPB  XXX            XX    ',
        'X                       X   ',
        'XXXX        EXX       BXX   ',
        'XXX  W   FFXX         B X   ',
        'XXX  W XXXXXXXXXXXXXX XX    ',
        'XXXWWWWX  XXXXXXXXXX  XXX   ',
        'XXXXXXXX  XXXXXX  XX  XXXX  ',
        'XXXXXXXX  XXXXXX  XX  XXXX  ']
        menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False,
                                                                       'window': None}), 1, actions,test_level_map, 
                     inc_time=10, i = 0)
        self.assertFalse(len(menu.level.tiles) == 116)


if __name__ == '__main__':
    unittest.main()
