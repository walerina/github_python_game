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
    newlevel = Level(map, create_screen())
    newlevel.display_surface = create_screen()
    newlevel.setup_level = map
    newlevel.world_shift = 1
    newlevel.oldY = 0
    newlevel.on_middle = False
    return newlevel

class System_testting(unittest.TestCase):
#Пачка 3 Юля:
#Прошёл уровень 1 и продолжил из победы со 2
#Прошёл уровень 1 вышел из игры и продолжил со 2
#Пользователь продолжил игру, дошел до разрушаемого препятствия и разрушил его

#Доп сценарий, который надо утверждать (вроде между собой договорились на тестирование скрола камеры при хождении: сам сценарий - новая игра, пробегает расстояние N+3, проверяем скрол камеры )
    def test_new_game_scroll(self):
        Pause.pre_quit(2)
        menu.last_passed_level=2

        actions = [
                   ({pygame.K_RIGHT: False, pygame.K_LEFT: True, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 0.03),
                   ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 1)]
        test_level_map = [
            'XX                          ',
            'XX                          ',
            'XWX                         ',
            'XW P                  XX    ',
            'XW                       X   ',
            'XXXX                  BXX   ',
            'XXXX                  B X   ',
            'XXX                   XX    ',
            'XXXXXXXXXXXXXXXXXXXXXXXXX   ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ']
        level = create_level(test_level_map)
        menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 0, actions, test_level_map,
                     inc_time=10)
        self.assertFalse(level.world_shift == 0)



if __name__ == '__main__':
    unittest.main()
