import pygame, pygame_textinput
from typing import TYPE_CHECKING
import datetime

from domain.utils import colors, math_utillity as math
from domain.utils.math_utillity import divide_tuple_infix as t_div, sum_tuple_infix as t_sum
from domain.services import game_controller
from domain.models.button import Button
from domain.utils.math_utillity import multiply_tuple_infix as t_mul
if TYPE_CHECKING:
    from game import Game
    
class Level:
    def __init__(self, game: 'Game', lvl_number, **kwargs):
        self.game = game
        self.txt_input = None
        _font_obj = kwargs.pop('font_obj', pygame.font.SysFont('calibri', 30,True))
        _background_color = kwargs.pop('background_color', colors.CODE_BG)
        _border_color = kwargs.pop('border_color', colors.CODE_BORDER)
        _border_width = kwargs.pop('border_width', 20)
        _input_size = kwargs.pop('_input_size', self.game.monitor_size |t_mul| (0.6,0.7))
        _cursor_color = kwargs.pop('cursor_color', colors.WHITE)
        _padding = kwargs.pop('padding', (18,18))
        
        self.title = ''
        self.description = ''
        
        self.variables_dict = None
        self.prefix_code = ''
        self.sufix_code = ''
        self.user_code = ''
        self.expected_answer = None
        self.answer_var_name = ''
        
        self.rendered = []
        self.popup_box = None
        self.popup_endtime = None
        
        _screen_rect = game.screen.get_rect()
        _btn_rect = pygame.Rect((0,0), (150,70))
        _btn_rect.right = _screen_rect.width - (_screen_rect.height * 0.05)
        _btn_rect.bottom = _screen_rect.height - (_screen_rect.height * 0.05)
        self.btn_run = Button((150,70),_btn_rect.topleft,lambda btn: self.run(), text="Executar")
        
        _txt_manager = pygame_textinput.TextInputManager(validator=game_controller.validate_input)
        self.txt_input = pygame_textinput.TextInputVisualizer(
            manager = _txt_manager, 
            font_object = _font_obj,
            background_color = _background_color,
            border_color = _border_color,
            border_width = _border_width,
            size = _input_size,
            cursor_color = _cursor_color,
            padding = _padding)
        
        self.prefix_txt = pygame_textinput.TextInputVisualizer(
            readonly=True,
            font_object = _font_obj,
            background_color = _background_color,
            border_color = _border_color,
            border_width = _border_width,
            size = _input_size,
            cursor_color = _cursor_color,
            padding = _padding)

        pygame.display.set_caption(f'U-Code (Level {lvl_number})')
        
    def print_btn(self, btn: Button):
        print("Clicked!")
    
    def update(self, events):
        self.txt_input.update(events)
        if 'pref_txt' not in self.rendered:
            self.rendered.append('pref_txt')
            self.prefix_txt.manager.set_buffer(self.prefix_code.split('\n') + self.sufix_code.split('\n'))
            self.prefix_txt.update(events)
        self.btn_run.update(events)
    
    def draw(self, screen: pygame.Surface):
        _txt_rect = self.draw_txt_input(screen)
        
        if 'btn_run' not in self.rendered:
            self.rendered.append('btn_run')  
            _screen_rect = screen.get_rect()
            _txt_spacing = self.txt_input.border_width/2 + self.txt_input.padding[0]/2
            self.btn_run.size = (_screen_rect.width - (_txt_rect.left + _txt_rect.width + _txt_spacing + 20), self.btn_run.size[1])
            self.btn_run.rect.left = _txt_rect.left + _txt_rect.width + _txt_spacing + 10
            self.btn_run.rect.size = self.btn_run.size
            self.btn_run.draw(screen)
        
        if 'title' not in self.rendered:
            self.rendered.append('title')  
            title_sur = self.game.drawer.get_text_surface(self.title, colors.WHITE, 'Calibri', 50)
            screen.blit(title_sur, (screen.get_width()/2 - title_sur.get_width()/2, 10))
        
        if 'description' not in self.rendered:
            self.rendered.append('description')  
            lines = self.description.split('\n')
            top = 0
            for line in lines:
                description_sur = self.game.drawer.get_text_surface(line, colors.WHITE, 'Calibri', 30)
                screen.blit(description_sur, (screen.get_width()/2 - description_sur.get_width()/2, self.txt_input.pos[1] - (description_sur.get_height() * len(lines)) + top))
                top += description_sur.get_height()
        
        if self.popup_box != None:
            self.popup_box()
            if datetime.datetime.now() >= self.popup_endtime:
                self.popup_endtime = None
                self.popup_box = None
            
                
    def run(self) -> bool:
        
        self.user_code = self.txt_input.get_value()
        
        #for user to view
        def check(condition):
            _message = f'A solução está {"CORRETA" if condition else "INCORRETA"}!'
            print(_message)
            self.popup(_message, colors.GREEN if condition else colors.RED, 3)
            return condition
        self.variables_dict['check'] = check
        
        exec(self.prefix_code, self.variables_dict)
        
        try:
            exec(self.user_code, self.variables_dict)
        except Exception as err:
            self.popup(str(err), colors.RED, 5)
            return False
        
        exec(self.sufix_code, self.variables_dict)
        
        return self.variables_dict[self.answer_var_name] == self.expected_answer
    
    def popup(self, message, color, timeout):
        _text_surface = self.game.drawer.get_text_surface(message, color, 'Calibri', 30)
        _screen_rect = self.game.screen.get_rect()
        _txt_rect = pygame.Rect((0,0), _text_surface.get_size())
        _txt_rect.center = _screen_rect.center
        self.popup_box = lambda: self.game.screen.blit(_text_surface, _txt_rect.topleft)
        self.popup_endtime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    
    def draw_txt_input(self, screen: pygame.Surface):
        _size = 0
        if self.txt_input.size == (0,0):
            _size = self.txt_input.surface.get_size()
        else:
            _size = self.txt_input.size
            
        _screen_rect = screen.get_rect()
        _rect = pygame.Rect((0,0), _size)
            
        _rect.bottom = _screen_rect.height - (_screen_rect.height * 0.05)
        _rect.right = _screen_rect.width - (_screen_rect.height * 0.05) - self.btn_run.size[0] - self.btn_run.border_width*2
        
        board = pygame.draw.rect(screen, self.txt_input.background_color, (_rect.topleft, _size |t_sum| self.txt_input.padding))
        border = pygame.draw.rect(screen, self.txt_input.border_color, (_rect.topleft, _size |t_sum| self.txt_input.padding), self.txt_input.border_width)
        screen.blit(self.txt_input.surface, _rect.topleft |t_sum| (self.txt_input.padding |t_div| (2,2)) |t_sum| (self.txt_input.border_width,self.txt_input.border_width) )
        self.txt_input.pos = _rect.topleft
        
        _pref_size = (_screen_rect.size[0] - _size[0] - self.txt_input.padding[0]*2 - self.txt_input.border_width*2 - self.btn_run.size[0] - self.btn_run.border_width*2 - self.btn_run.padding[0], _size[1])
        _pref_rect = pygame.Rect((_screen_rect.height * 0.05, _rect.top), _pref_size)
        pref_board = pygame.draw.rect(screen, self.prefix_txt.background_color, (_pref_rect.topleft, _pref_size |t_sum| self.prefix_txt.padding))
        pref_border = pygame.draw.rect(screen, self.prefix_txt.border_color, (_pref_rect.topleft, _pref_size |t_sum| self.prefix_txt.padding), self.prefix_txt.border_width)
        screen.blit(self.prefix_txt.surface, _pref_rect.topleft |t_sum| (self.prefix_txt.padding |t_div| (2,2)) |t_sum| (self.prefix_txt.border_width,self.prefix_txt.border_width) )
        return _rect