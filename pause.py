import pygame
from settings import *
from button import *
import json
import sys


class Pause:

    def pre_quit(last_passed_level):
        with open('game_data.txt','w') as file:
            json.dump(last_passed_level,file)
        with open('game_data.txt') as file:
            return json.load(file)    
            
    def pause (screen,clock,last_passed_level,dop_event = None):
        
        screen.fill((0, 0, 139))

        font = pygame.font.SysFont(None, 50)
        text = font.render("Пауза", True, (255, 255, 255))
        text_rect = text.get_rect(center=pygame.Rect(590, 150, 5, 5).center)
        screen.blit(text, text_rect)

        continue_button = Button(550, 350, 100, 30, (20, 0, 0), "Продолжить")
        continue_button.draw(screen)
        
        exit_button = Button(550, 550, 100, 30, (0, 0, 0), "Выход")
        exit_button.draw(screen)          
        
        paused = True
        
        while paused :
            if dop_event:
                test_event = dop_event     
                pygame.event.post(test_event)
            for event in pygame.event.get():     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.__dict__['pos']
                    if continue_button.rect.collidepoint(mouse_pos):
                        paused = False
                        if dop_event:
                            return "pause" 
                    elif exit_button.rect.collidepoint(mouse_pos):
                        Pause.pre_quit(last_passed_level)
                        pygame.quit()
                        if dop_event:
                            return "exit"
                        sys.exit()
            pygame.display.update()
            clock.tick(60)  
        

        
