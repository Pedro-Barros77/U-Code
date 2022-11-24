import pygame
from typing import TYPE_CHECKING

from domain.utils import colors
from domain.services.drawer import Drawer
from domain.utils.math_utillity import multiply_tuple_infix as t_mul
# if TYPE_CHECKING:
#     from game import Game
    
class Button:
    def __init__(self, size, pos, callback, **kwargs):
        
        self.size = size
        self.pos = pos
        self.callback = callback
        self.rect = pygame.Rect(pos, size)
        self.drawer = Drawer()
        
        
        self.text = kwargs.pop('text', "Click Me!")
        self.text_color = kwargs.pop('text_color', colors.WHITE)
        self.background_color = kwargs.pop('background_color', colors.PASTEL_GREEN)
        self.border_width = kwargs.pop('border_width', 5)
        self.border_color = kwargs.pop('border_color', colors.PASTEL_DARK_GREEN)
        self.border_radius = kwargs.pop('border_radius', 15)
        self.font_obj = kwargs.pop('font_obj', pygame.font.SysFont('Calibri', 30,True))
        self.padding = kwargs.pop('padding', (18,18))
        self.hover_callback = kwargs.pop('hover_callback', self.default_hover)
        self.hovering = False
        
        self.defaults = {
            'size': self.size,
            'pos': self.pos,
            'rect': self.rect,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'border_width': self.border_width,
            'border_color': self.border_color,
            'font_obj': self.font_obj,
            'padding': self.padding,
            'hover_callback': self.hover_callback,
        }
        
    def mouse_in_bounds(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.left < mouse_pos[0] < self.rect.right and\
            self.rect.top < mouse_pos[1] < self.rect.bottom
    
    def update(self, events):
        
        if self.mouse_in_bounds():
            self.hovering = True
            self.hover_callback(self)
        else:
            self.hovering = False
            self.hover_out()
        
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and self.mouse_in_bounds():
                self.callback(self)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=int(self.border_radius))
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width,self.border_radius)
        
        _txt_surface = self.drawer.get_text_surface(self.text, self.text_color, self.font_obj, 0)
        _txt_rect = _txt_surface.get_rect()
        _txt_rect.center = self.rect.center
        screen.blit(_txt_surface, _txt_rect.topleft)
    
    def default_hover(self, btn: 'Button'):
        btn.background_color = colors.PASTEL_LIGHT_GREEN
        btn.border_color = colors.PASTEL_GREEN
        
    def hover_out(self):
        for prop in self.defaults.items():
            setattr(self, prop[0], prop[1])