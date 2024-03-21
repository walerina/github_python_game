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
    def test_pass_1level_and_continue2(self):
        actions = [
                   ({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 0.04),
                   ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 1)]
        test_level_map = [
            'XX                          ',
            'XX                          ',
            'XXX                         ',
            'XXXP X                XX    ',
            'X    X                   X   ',
            'XXXXWXXXXXXXXXXXXXXXXXXBXX   ',
            'XXXX                  B X   ',
            'XXX                   XX    ',
            'XXXXXXXXXXXXXXXXXXX  XXX   ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ']
        menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 2, actions, test_level_map,
                     inc_time=10)
        self.assertEqual(menu.last_passed_level, 1)

#Пользователь продолжил игру, дошел до разрушаемого препятствия и разрушил его




if __name__ == '__main__':
    unittest.main()
