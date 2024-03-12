import pygame
from settings import *
from button import *


class Mess_window:

    def __init__(self):
        self.first_time = True

    def win(self, last_passed_level, screen, dop_event = None, test=0):
        screen.fill((0, 0, 139))
        font = pygame.font.SysFont(None, 100)
        all_pobeda = "ПОБЕДА"
        text = font.render(all_pobeda, True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 100, 5, 5).center)
        screen.blit(text, text_rect)
        if self.first_time:
            self.first_time = False
            last_passed_level[0] += 1
            if test == 1:
                return last_passed_level[0]
            if last_passed_level[0] == len(level_maps):
                last_passed_level[0] = 0
                if test == 2:
                    return last_passed_level[0]
            if test == 2:
                    return last_passed_level[0]
        if last_passed_level[0] == 0:
            font = pygame.font.SysFont(None, 50)
            all_pobeda = "Ты всё прошел! Можешь начать сначала"
            text = font.render(all_pobeda, True, (255, 255, 255))
            text_rect = text.get_rect(center=pygame.Rect(590, 200, 5, 5).center)
            screen.blit(text, text_rect)
            if test == 3:
                 return "all"
        if test == 3:
            return "Not all"
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        for event in pygame.event.get():
                if dop_event:
                     event = dop_event         
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.__dict__['pos']
                    if continue_button.rect.collidepoint(mouse_pos):
                        self.first_time = True
                        return ("continue")
        return("waiting")

    def loose(self, screen, dop_event=None):
        screen.fill((0, 0, 139))
        font = pygame.font.SysFont(None, 100)
        all_loose = "ПРОИГРЫШ"
        text = font.render(all_loose, True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 100, 5, 5).center)
        screen.blit(text, text_rect)
        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        for event in pygame.event.get():
                if dop_event:
                     event = dop_event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.__dict__['pos']
                    if continue_button.rect.collidepoint(mouse_pos):
                        self.first_time = True
                        return ("continue")
        return("waiting")

