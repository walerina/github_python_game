import pygame
from settings import *
from menu import Menu 


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
menu = Menu()


while True:
    menu.run(screen, clock)
