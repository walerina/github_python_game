from levels import Level
from pause import *
from mess_window import Mess_window
import json
import sys

class Menu:
    def __init__(self):
        self.last_passed_level = 0

    def pre_start():
        try:
            with open('game_data.txt') as file:
                return  json.load(file)
        except:
           return 0

    def run(self, screen, clock, dop_event = None, last_passed_level = pre_start(), level_events = [], level_structure = [], return_player = False, inc_time = 1):
        self.last_passed_level = last_passed_level
        new_game_button = Button(550, 150, 100, 30, (0, 100, 0), "Новая игра")
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        exit_button = Button(550, 550, 100, 30, (0, 0, 0), "Выход")
        screen.fill((0, 0, 139))
        new_game_button.draw(screen)
        continue_button.draw(screen)
        exit_button.draw(screen)
        while True:
            if dop_event:
                test_event = dop_event     
                pygame.event.post(test_event)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.__dict__['pos']
                    if new_game_button.rect.collidepoint(mouse_pos):
                        self.last_passed_level = 0
                        if dop_event and level_events == []:
                            return "start"
                        game_result = self.start_the_game(screen, clock, level_events, level_structure, return_player, inc_time)
                        if level_events != []:
                            return game_result
                    elif continue_button.rect.collidepoint(mouse_pos) and self.last_passed_level != 0:
                        if dop_event and level_events == []:
                            return "continue"
                        game_result = self.continue_the_game(screen, clock, level_events, level_structure, return_player, inc_time)
                        if level_events != []:
                            return game_result
                    elif exit_button.rect.collidepoint(mouse_pos):
                        if dop_event and level_events == []:
                            return "exit"
                        Pause.pre_quit(self.last_passed_level)
                        pygame.quit()
                        sys.exit()
                    elif dop_event:
                        return "mouse"
                elif dop_event:
                    return("not_mouse")
            pygame.display.update()


    def start_the_game(self, screen, clock, level_events, level_structure, return_player = False, inc_time = 1, zero_level=0, dop_event = None, test=0, test_result=""):
        if level_structure == []:
            level_structure = level_maps[zero_level]
        level = Level(level_structure, screen)
        result = "running"
        while result == "running":
            screen.fill('grey')
            if dop_event:
                test_event = dop_event     
                pygame.event.post(test_event)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if dop_event:
                            return "pause"
                        Pause.pause(screen,clock,self.last_passed_level)
            result = level.run(screen, level_events, return_player, inc_time)
            if return_player and result != "running":
                return result
            if test !=0:
                result = test_result
            pygame.display.update()
            clock.tick(60 * inc_time)
        if result == "win": #!
                if level_events != []:
                    return result
                mess_window = Mess_window()
                win_result = "waiting"
                while win_result == "waiting":
                    if test ==1:
                        return "waiting"
                    last_passed_level_param = [self.last_passed_level]
                    win_result = mess_window.win(last_passed_level_param, screen)
                    self.last_passed_level = last_passed_level_param[0]
                    if test==3:
                        return self.last_passed_level
                    pygame.display.update()
                    clock.tick(60 * inc_time)
                    if test==2:
                        win_result="continue"
                if win_result == "continue":
                    if test==2:
                        return "continue"
                    self.continue_the_game(screen, clock, level_events, [], return_player, inc_time)

        elif result == "loose":
                if level_events != []:
                    return result
                mess_window = Mess_window()
                loose_result = "waiting"
                while loose_result == "waiting":
                    if test ==1:
                        return "waiting"
                    loose_result = mess_window.loose(screen)
                    if test==3:
                        return self.last_passed_level
                    if test==2:
                        loose_result="continue"
                    pygame.display.update()
                    clock.tick(60 * inc_time)
                if loose_result == "continue":
                    if test==2:
                        return "continue"
                    self.continue_the_game(screen, clock, level_events, [], return_player, inc_time)

    def continue_the_game(self, screen, clock, level_events, level_structure, return_player = False, inc_time = 1, test=False):
        self.start_the_game(screen, clock, level_events, level_structure, return_player, inc_time, zero_level=self.last_passed_level)
