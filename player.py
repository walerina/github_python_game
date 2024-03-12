import pygame
import threading
import keyboard

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.w = 32
        self.h = 128
        self.mh = self.h / 2
        self.color = 'red'
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.is_down = False
        self.is_jump = False
        self.speed = 7
        self.jump_speed = -11
        self.gravity_speed = 7
        self.jump = self.gravity_speed
        self.healf = 11
        self.is_unbending = False
        self.is_pressed = False
        self.action_number = 0
        self.action_timer = threading.Timer(0, self.empty)

    def empty(self):
            pass

    def jumpToDown(self):
        self.jump = self.gravity_speed

    def apply_gravity(self):
        self.direction.y += self.jump
        self.rect.y += self.direction.y

    def increase_action_number(self):
        self.action_number += 1

    def get_input(self, level_events = [], inc_time = 1):
        if level_events == []:
            keys = pygame.key.get_pressed()
        elif isinstance(level_events, dict):
            keys = level_events
        else:
            if self.action_number == len(level_events):
                keys = {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}
            else:
                keys = level_events[self.action_number][0]
                action_time = level_events[self.action_number][1]
                if not self.action_timer.is_alive():
                    self.action_timer = threading.Timer(action_time, self.increase_action_number)
                    self.action_timer.start()

        self.direction.x, self.direction.y = 0, 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_DOWN]:
            if not self.is_jump:
                self.image = pygame.Surface((self.w, self.mh))
                self.image.fill(self.color)
                if not self.is_down:
                    self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y + self.mh))
                self.is_down = True
        elif keys[pygame.K_UP]:
            if not self.is_jump:
                if not self.is_down and not self.is_unbending:
                    self.jump = self.jump_speed
                    self.is_jump = True
                    timer_thread = threading.Timer(0.25 / inc_time, self.jumpToDown)
                    timer_thread.start()
                elif self.is_down and not self.is_pressed:
                    self.image = pygame.Surface((self.w, self.h))
                    self.image.fill(self.color)
                    self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y - self.mh))
                    self.is_down = False
                    self.is_unbending = True
        if not keys[pygame.K_UP]:
            self.is_unbending = False

    def update(self, level_events = [], inc_time = 1):
        self.get_input(level_events, inc_time)
        self.rect.x += self.direction.x * self.speed
