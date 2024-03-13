import unittest
from menu import Menu
from tiles import *
from settings import *

pygame.init()
clock = pygame.time.Clock()
menu = Menu()

def create_screen():
    return pygame.display.set_mode((screen_width, screen_height))

class System_testting(unittest.TestCase):
    # Пользователь начал новую игру, добежал до середины уровня, остановился, умер от столкновения с догнавшим врагом.
    def test_enemy_death(self):
        actions = [({pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 0.15)]
        test_level_map = [
            'XX                   W      ',
            'XX                   W      ',
            'XXX                  W      ',
            'XXXP                 WXX    ',
            'X                    W   X   ',
            'XXXXXXXXXXXXXXXXXXXXXWBXX   ',
            'XXXX      FXX        WB X   ',
            'XXX    XXXXXXXXXXXXXXWXX    ',
            'XXX  E X  XXXXXXXXXX  XXX   ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ']
        self.assertEqual(
            menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 0, actions, test_level_map,
                     inc_time=10), "loose")
if __name__ == '__main__':
    unittest.main()