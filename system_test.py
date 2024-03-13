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
#Пачка 3 Юля:
#Прошёл уровень 1 и продолжил из победы со 2
 def test_something(self):
     self.assertTrue(True)
#Прошёл уровень 1 вышел из игры и продолжил со 2

#Пользователь продолжил игру, дошел до разрушаемого препятствия и разрушил его

#Доп сценарий, который надо утверждать (вроде между собой договорились на тестирование скрола камеры при хождении: сам сценарий - новая игра, пробегает расстояние N+3, проверяем скрол камеры )


if __name__ == '__main__':
    unittest.main()
