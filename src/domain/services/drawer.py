import pygame, pygame_textinput

from domain.utils import colors, math_utillity as math
from domain.utils.math_utillity import \
    sum_tuple_infix as t_sum, \
    divide_tuple_infix as t_div

class Drawer:
    def __init__(self):
        pass
    
    def draw_text(self, surface, text, pos, color = colors.WHITE, font = 'Calibri', size = 30):
        text_surface = self.get_text_surface(text, color, font, size)
        surface.blit(text_surface, pos)
    
    def get_text_surface(self, text, color, font, size):
        text = str(text)
        
        r, g, b, *a = color
        color = (r,g,b)
        _font = None
        
        if type(font) == str:
            _font = pygame.font.SysFont(font, size)
        else:
            _font = font
                
        text_surface = _font.render(text, False, color)
        if len(a) > 0:
            text_surface.set_alpha(a[0])
        return text_surface
