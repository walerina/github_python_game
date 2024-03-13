import unittest
from menu import Menu
from mess_window import *
from player import Player
from tiles import *
from settings import *
from levels import Level
from enemy import Enemy
from pause import Pause

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
#Пачка 2 Аделина:
#Пользователь продолжил игру, добежал до середины уровня, остановился, вышел из игры(проверка не инкрементации)
    def test_continue_game_exit(self):
        events = [
                pygame.event.Event(768, {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 40, 'window': None}),
                pygame.event.Event(1025, {'pos': (581, 559), 'button': 1, 'touch': False,'window': None})
                 ]
        actions = [
            ({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: False}, 0.01),
            ({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
              pygame.K_SPACE: False}, 0.08)]
        level = menu.last_passed_level
        self.assertEqual(
            menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 1, actions, 
                     inc_time=10, dop_event_level= events, i = 0), "exit")
        self.assertEqual(menu.last_passed_level, level)


if __name__ == '__main__':
    unittest.main()
