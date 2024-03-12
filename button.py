import pygame

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.clicked = False
        self.rect.topleft = (x, y)

    def draw(self,screen, pos = (0,0), pres = 3):
        action = False
        if pos == (0,0):
            pos = pygame.mouse.get_pos()


        if self.rect.collidepoint(pos):
            if pres == 3:
                pres =  pygame.mouse.get_pressed()[0]            
            if pres == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pres == 3:
                pres =  pygame.mouse.get_pressed()[0]
        if pres == 0:
            self.clicked = False

        font = pygame.font.SysFont(None, 30)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        return action
    
