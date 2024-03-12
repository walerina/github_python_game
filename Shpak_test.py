import unittest
from menu import *
from mess_window import *
import os
from parameterized import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
menu = Menu()
mess_window = Mess_window()
event = pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False, 'window': None})

class Button_Test (unittest.TestCase):
    def test_draw (self):
        button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        self.assertEqual (button.draw(screen), False)
    
    def test_draw_logic (self):
        button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        self.assertEqual ({button.draw(screen,(559, 152),1),button.clicked}, {True,True})
        self.assertEqual ({button.draw(screen,(569, 160),0),button.clicked}, {False,False})
    
    def test_clic (self):
        button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        button.draw(screen,(559, 152),1)
        self.assertEqual (button.clicked, True) 
        button.draw(screen,(569, 160),0)      
        self.assertEqual (button.clicked, False)     

    def test_action (self):
        button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        self.assertEqual (button.draw(screen, (569, 160),1), True)    
        self.assertEqual (button.draw(screen, (569, 16),1), False)
        self.assertEqual (button.draw(screen, (569, 160),0), False)

class Menu_Test (unittest.TestCase):
    def test_pre_start (self):
        with open('game_data.txt','w') as file:
            json.dump(1,file)
        self.assertEqual (Menu.pre_start(), 1) 
        os.remove('game_data.txt')
        self.assertEqual (Menu.pre_start(), 0)     

    def test_continue (self):
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1025, {'pos': (600, 360), 'button': 1, 'touch': False, 
                                                                           'window': None}), 1), "continue")
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1025,
                                                                    {'pos': (600, 360), 'button': 1, 'touch': False,
                                                                     'window': None}), 0), "mouse")

    def test_new_game (self):
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1025, {'pos': (589, 163), 'button': 1, 'touch': False, 
                                                                           'window': None}), 1), "start")

    def test_quit (self):
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1025, {'pos': (600, 565), 'button': 1, 'touch': False, 
                                                                           'window': None}), 1), "exit")

    def test_mouse (self):
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1025, {'pos': (141, 151), 'button': 1, 'touch': False, 
                                                                           'window': None}), 1), "mouse")

    def test_not_mouse(self):
        self.assertEqual(menu.run(screen, clock, pygame.event.Event(1026,
                                                                    {'pos': (141, 151), 'button': 1, 'touch': False,
                                                                     'window': None}), 1), "not_mouse")

    def test_pause(self):
        self.assertEqual(menu.start_the_game(screen, clock, 0, pygame.event.Event(768, {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 40, 
                                                                                        'window': None})),"pause")
 
    def test_win_window(self):
       self.assertEqual(menu.start_the_game(screen, clock, 0, test=1, test_result="win" ),"waiting")
 
    def test_loose_window(self):
        self.assertEqual(menu.start_the_game(screen, clock, 0, test=1, test_result="loose" ),"waiting")
 
    def test_win_continue(self):
        self.assertEqual(menu.start_the_game(screen, clock, 0, test=2, test_result="win" ),"continue")
 
    def test_loose_continue(self):
        self.assertEqual(menu.start_the_game(screen, clock, 0, test=2, test_result="loose" ),"continue")
 
    def test_increment_level(self):
        menu.last_passed_level=0
        self.assertEqual(menu.start_the_game(screen, clock, 0, test=3, test_result="win" ),1)
        self.assertEqual(menu.start_the_game(screen, clock, 0, test=3, test_result="loose" ),1)   
       

class Mess_Window_Test (unittest.TestCase):
    def test_win_mes (self):
        last_passed_level_param = [menu.last_passed_level]
        self.assertEqual (mess_window.win(last_passed_level_param, screen), "waiting") 
          
    def test_first_time_if (self):
        menu.last_passed_level = 0
        last_passed_level_param = [menu.last_passed_level]
        mess_window.first_time = True
        self.assertEqual (mess_window.win(last_passed_level_param, screen,test=1), 1)  

    @parameterized.expand([
        [0, 1],
        [1, 2],
        [2, 0],
    ])
    def test_increment_inside (self, last_passed_level, waited):
        mess_window.first_time = True
        menu.last_passed_level = last_passed_level
        last_passed_level_param = [menu.last_passed_level]
        self.assertEqual (mess_window.win(last_passed_level_param, screen, test = 2), waited)
    
    @parameterized.expand([
        [0, "Not all"],
        [1, "Not all"],
        [2, "all"],
    ])
    def test_last_level (self,last_passed_level, waited):
        mess_window.first_time = True
        menu.last_passed_level = last_passed_level
        last_passed_level_param = [menu.last_passed_level]
        self.assertEqual (mess_window.win(last_passed_level_param, screen, test = 3), waited)  
  
    #def test_win_continue_inside(self):
    #    mess_window3 = Mess_window()
    #    menu.last_passed_level = 0
    #    last_passed_level_param = [menu.last_passed_level]
    #    print("warning")
    #    self.assertEqual (mess_window3.win(last_passed_level_param, screen, dop_event=pygame.event.Event(1025, {'pos': (586, 375), 'button': 1, 'touch': False, 
    #                                                                                               'window': None})), "continue")    
    #    self.assertEqual (mess_window3.win(last_passed_level_param, screen,pygame.event.Event(1025, {'pos': (55, 36), 'button': 1, 'touch': False, 
    #                                                                                                'window': None})), "waiting")    
        
    def test_loose_mes (self):
        self.assertEqual (mess_window.loose( screen),"waiting") 
    
    def test_loose_continue_inside (self):
        mess_window2 = Mess_window()
        self.assertEqual (mess_window2.loose(screen,pygame.event.Event(1025, {'pos': (552, 355), 'button': 1, 'touch': False, 
                                                                             'window': None})), "continue")    
        self.assertEqual (mess_window2.loose(screen,pygame.event.Event(1025, {'pos': (55, 362), 'button': 1, 'touch': False, 
                                                                             'window': None})), "waiting")    


class Pause_Test (unittest.TestCase):

    def test_pause_off (self):
        self.assertEqual (Pause.pause(screen,clock,1,pygame.event.Event(1025, {'pos': (590, 359), 'button': 1, 'touch': False,
                                                                                'window': None})), "pause")

    def test_pause_quit (self):
        self.assertEqual (Pause.pause(screen,clock,1,pygame.event.Event(1025, {'pos': (581, 559), 'button': 1, 'touch': False,
                                                                                'window': None})), "exit")
    
    def test_pre_quit(self):
        self.assertEqual (Pause.pre_quit(0), 0 )