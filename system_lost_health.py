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
    # Пользователь начал новую игру, прыгнул, упал на враждебное препятствие, потерял часть здоровья
    def test_lost_health(self):
        actions = [({pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: True, pygame.K_DOWN: False,
                     pygame.K_SPACE: False}, 0.01),
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
            'XXXX        EXX      WBXX   ',
            'XXXX      FXX        WB X   ',
            'XXX    EEXXXXXXXXXXXXWXX    ',
            'XXX EEEX  XXXXXXXXXX  XXX   ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ',
            'XXXXXXXX  XXXXXX  XX  XXXX  ']
        self.assertEqual(
            menu.run(create_screen(), clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False,
                                                                       'window': None}), 0, actions, test_level_map,
                     return_player=True, inc_time=10).healf, 6)

if __name__ == '__main__':
    unittest.main()        