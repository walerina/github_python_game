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
#Пачка 2 Аделина:
#Пользователь продолжил игру, добежал до середины уровня, остановился, вышел из игры(проверка не инкрементации)
    def test_continue_game_exit(self):
        Pause.pre_quit(1)
        screen = create_screen()
        event = pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False, 'window': None})

        screen = create_screen()
        new_game_button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        exit_button = Button(550, 550, 100, 30, (0, 0, 0), "Выход")
        screen.fill((0, 0, 139))
        new_game_button.draw(screen)
        continue_button.draw(screen)
        exit_button.draw(screen)
        menu.last_passed_level = 1
        event = pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False, 'window': None})
        mouse_pos = event.__dict__['pos']
        if new_game_button.rect.collidepoint(mouse_pos):
            menu.last_passed_level = 0
        elif continue_button.rect.collidepoint(mouse_pos) and menu.last_passed_level != 0:
            menu.last_passed_level = Menu.pre_start()

        level = create_level(level_maps[1])
        keys = create_keys()
        keys[pygame.K_RIGHT] = True
        for x in range (0, 10):
            level.player.sprite.update(keys)

        event = [pygame.event.Event(768, {'unicode': 'x', 'key': 120, 'mod': 0, 'scancode': 27, 'window': None}),
                 pygame.event.Event(768, {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 40, 'window': None})]
        result = "running"
        i = 0
        while result == "running":
            screen.fill('grey')
            result = level.run(screen)
            if result == "win":
                menu.last_passed_level+=1

            if event[i].type == pygame.KEYDOWN:
                if event[i].key == pygame.K_RETURN:
                    Pause.pre_quit(menu.last_passed_level)
                    result = "quit"
            i+=1

        self.assertEqual(menu.last_passed_level,1)

#Прошёл уровень 3 и продолжил с 0
    def test_pass_3level_and_continue0(self):
        self.assertTrue(True)
#Пользователь начал новую игру, включил паузу, продолжил игру,включил паузу, вышел из игры
    def test_new_game_and_pause_exit(self):
        self.assertTrue(True)
#Пачка 3 Юля:
#Прошёл уровень 1 и продолжил из победы со 2

#Прошёл уровень 1 вышел из игры и продолжил со 2

#Пользователь продолжил игру, дошел до разрушаемого препятствия и разрушил его

#Доп сценарий, который надо утверждать (вроде между собой договорились на тестирование скрола камеры при хождении: сам сценарий - новая игра, пробегает расстояние N+3, проверяем скрол камеры )

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(System_testting)
    #unittest.TextTestRunner().run(suite)