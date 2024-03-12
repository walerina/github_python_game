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



class All_window_testting(unittest.TestCase):

#Пачка 1: Лера
#Смерть от врага
#sadfq
    def test_enemy_death(self):
        level = create_level()
        level.enemy.sprite.rect.x, level.player.sprite.rect.x =  0, level.enemy.sprite.w - 1
        level.run(create_screen())
        self.assertEqual(level.player.sprite.healf, 0)

#Смерть от потери здоровья
    def test_loosing_health(self):
        level = create_level()
        level.player.sprite.healf = 0
        self.assertEqual(level.run(create_screen()), "loose")

#Уничтожение блока
    def test_destruct_block(self):
        level, keys = create_level(), create_keys()
        tile = Barrier_fragile((0, 0), 64)
        level.tiles = [tile]
        keys[pygame.K_SPACE] = True
        level.destruct(level.tiles[0], keys)
        self.assertEqual(len(level.tiles), 0)
        self.assertTrue(tile.broken)

#Урон от препятствия
    def test_get_hurt_block(self):
        level = create_level([' PE  '])
        level.player.sprite.healf = 4
        level.get_hurt(Barrier_enemy((0, 0), 64), level.player.sprite)
        self.assertEqual(level.player.sprite.healf, 0)

#Ошибки при нажатии кнопок удара (что-то не пробел, 0 реакции)
    def test_dont_hurt_fragile(self):
        level, keys = Level(level_maps[0], create_screen()), create_keys()
        tile = Barrier_fragile((0, 0), 64)
        level.tiles = [tile]
        keys[pygame.K_SPACE] = True
        level.destruct(level.tiles[0], create_keys())
        self.assertEqual(len(level.tiles), 1)
        self.assertFalse(tile.broken)

#Прыжок в пригибе
    def test_jump_after_down(self):
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

#Разгиб под препятствием
    def test_unbeding_under_block(self):
        keys, player = create_keys(), create_player()
        keys[pygame.K_DOWN] = True
        player.get_input(keys)
        player.is_pressed = True
        keys[pygame.K_DOWN], keys[pygame.K_UP], y = False, True, player.rect.y
        player.get_input(keys)
        self.assertEqual(player.rect.y, y)


#Пачка 2: Юля
#Не прохождение через стены при передвижение по карте
    def test_wall_collision(self):
        level = create_level(['XP    ',
                              'XXXXXXX'])
        keys = create_keys()
        begin_x = level.player.sprite.rect.x
        keys[pygame.K_LEFT] = True
        level.player.sprite.update(keys)
        level.horizontal_movement_collision()
        self.assertTrue(level.player.sprite.rect.x == begin_x)      

#Прыжок без проваливания за пределы карты
    def test_ground_collision_after_jump(self):
        level = create_level(['P     ',
                              'XXXXXXX'])
        keys = create_keys()
        begin_y = level.player.sprite.rect.y
        keys[pygame.K_UP] = True
        level.player.sprite.update(keys)
        keys[pygame.K_UP] = False
        level.player.sprite.update(keys)
        level.player.sprite.update(keys)
        level.player.sprite.update(keys)
        self.assertTrue(level.player.sprite.rect.y == begin_y)

#Передвижение по карте (не проваливание под пол)
    def test_horizontal_movement(self):
        level = create_level(['P     ',
                              'XXXXXXX'])
        keys = create_keys()
        begin_y = level.player.sprite.rect.y
        keys[pygame.K_RIGHT] = True
        level.player.sprite.update(keys)
        self.assertTrue(level.player.sprite.rect.y == begin_y)                  

#Горизонтальный ‘скролл’ камеры
    def test_horizontal_scroll(self):
        level = create_level(['XP                 X',
                              'X                  X',
                              'XXXXXXXXXXXXXXXXXXXX'])
        keys = create_keys()
        keys[pygame.K_LEFT] = True
        level.player.sprite.update(keys)
        level.scroll_x()
        self.assertFalse(level.world_shift == 0)

#Вертикальный ‘скролл’ камеры
    def test_vertical_scroll(self):
        level = create_level(['XP                 X',
                              'X                  X',
                              'XXXXXXXXXXXXXXXXXXXX'])
        keys = create_keys()
        keys[pygame.K_UP] = True
        level.player.sprite.update(keys)
        level.player.sprite.update(keys)
        level.scroll_x()
        self.assertTrue(level.world_shift == 0)

#Проходимость уровней
    def test_level_win(self):
        screen = create_screen()
        level = create_level([' PWX   ',
                              'XXXXXXX'])
        level.player.sprite.w = 64
        keys = create_keys()
        keys[pygame.K_RIGHT] = True
        for x in range (0, 10):
            level.player.sprite.update(keys)

        self.assertEqual(level.run(screen, keys), "win")

#Пачка 3: Аделина
#Включить паузу из уровня
    @patch('pause.Pause.pause', return_value=False)
    def test_pause_on (self,pause):
        level = create_level()
        screen = create_screen()
        event = [pygame.event.Event(768, {'unicode': 'x', 'key': 120, 'mod': 0, 'scancode': 27, 'window': None}),
                 pygame.event.Event(768, {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 40, 'window': None})]
        result = "running"
        i = 0
        while result == "running":
            screen.fill('grey')
            result = level.run(screen)
            if event[i].type == pygame.KEYDOWN:
                if event[i].key == pygame.K_RETURN:
                    Pause.pause(screen,clock,menu.last_passed_level)
                    result = "pause"
            i+=1        
        self.assertEqual(result, "pause") 

#Начало новой игры и переход к уровню
    @patch('menu.Menu.start_the_game', return_value=0)
    def test_new_game_menu(self,start_the_game):
        screen = create_screen()
        new_game_button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        exit_button = Button(550, 550, 100, 30, (0, 0, 0), "Выход")
        screen.fill((0, 0, 139))
        new_game_button.draw(screen)
        continue_button.draw(screen)
        exit_button.draw(screen)
        menu.last_passed_level = 1
        event = pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False, 'window': None})
        mouse_pos = event.__dict__['pos']
        if new_game_button.rect.collidepoint(mouse_pos):
            menu.last_passed_level = menu.start_the_game(screen,clock)
        self.assertEqual( menu.last_passed_level, 0)

#Продолжить игру из меню
    def test_continue_menu (self):
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
            menu.last_passed_level = 2             
        self.assertEqual( menu.last_passed_level, 2)
    
#Продолжить игру с паузы
    def test_continue_pause (self):
        screen = create_screen()
        screen.fill((0, 0, 139))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Пауза", True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 150, 5, 5).center)
        screen.blit(text, text_rect)
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        exit_button = Button(550, 550, 100, 30, (0, 0, 0), "Выход")
        exit_button.draw(screen)
        event = pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False, 'window': None})
        mouse_pos = event.__dict__['pos']
        paused = True
        if continue_button.rect.collidepoint(mouse_pos):
            paused = False
        self.assertEqual( paused, False)

#Продолжить игру с окна победы
    def test_continue_wins(self):
        screen = create_screen()
        mess_window.first_time = False
        event =pygame.event.Event(1025, {'pos': (580, 366), 'button': 1, 'touch': False, 
                                                                             'window': None})
        screen.fill((0, 0, 139))
        font = pygame.font.SysFont(None, 100)
        all_pobeda = "ПОБЕДА"
        text = font.render(all_pobeda, True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 100, 5, 5).center)
        screen.blit(text, text_rect)
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.__dict__['pos']
            if continue_button.rect.collidepoint(mouse_pos):
                mess_window.first_time = True         
        #mess_window3.win(last_passed_level_param, screen, dop_event = event)
        self.assertEqual(mess_window.first_time,True)    
    
#Продолжить игру с окна проигрыша
    def test_continue_loose (self):
        screen = create_screen()
        mess_window2 = Mess_window()
        mess_window2.first_time = False
        screen.fill((0, 0, 139))
        font = pygame.font.SysFont(None, 100)
        all_loose = "ПРОИГРЫШ"
        text = font.render(all_loose, True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 100, 5, 5).center)
        screen.blit(text, text_rect)
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        event =pygame.event.Event(1025, {'pos': (552, 355), 'button': 1, 'touch': False, 
                                                                             'window': None})
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.__dict__['pos']
            if continue_button.rect.collidepoint(mouse_pos):
                mess_window2.first_time = True        
        self.assertEqual(mess_window2.first_time,True)            
        
#Ошибка при вызове паузы ( нажимать что-то не энтер, должно ничего не происходить)
    @patch('pause.Pause.pause', return_value=False)
    def test_pause_on_err (self,pause):
        level = create_level()
        screen = create_screen()
        event = pygame.event.Event(768, {'unicode': 'x', 'key': 120, 'mod': 0, 'scancode': 27, 'window': None})
        level.run(create_screen())
        resulting = 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                resulting = Pause.pause(screen,clock,last_passed_level=1)
            else: 
                resulting = True        
        self.assertEqual(resulting,True)

if __name__ == '__main__':
    unittest.main()