import pygame, pygame_textinput
from datetime import datetime

from presentation.content import level_01
from domain.services import game_controller, drawer
from domain.utils import colors, math_utillity as math
from domain.utils.math_utillity import sum_tuple_infix as t, clamp_infix as clamp

class Game:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.drawer: drawer.Drawer = None
        self.pressed_keys = []
        self.start_time = None
        self.monitor_size = (0,0)
        self.level = None
    
    
    def start(self):
        pygame.init()
        
        game_controller.setup()
        
        if self.monitor_size == (0,0):
            self.monitor_size = (pygame.display.Info().current_w-50, pygame.display.Info().current_h - 80)

        self.screen = pygame.display.set_mode(self.monitor_size)
        
        self.start_time = datetime.now()

        self.clock = pygame.time.Clock()
        self.drawer = drawer.Drawer()
        self.level = level_01.Level01(self, 1)
        game_controller.playing = True
        self.game_loop()


    def game_loop(self):
        self.screen.fill(colors.BLUE_VOID)
        while game_controller.playing:
            
            _events = pygame.event.get()
            game_controller.handle_events(self, _events)

            
            self.level.update(_events)
            self.level.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)
        
