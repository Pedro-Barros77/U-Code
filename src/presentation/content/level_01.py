from domain.models.level import Level
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class Level01(Level):
    def __init__(self, game: 'Game', lvl_number, **kwargs):
        super().__init__(game, lvl_number, **kwargs)
        
        self.title = "Atribuição de Valor"
        self.description = 'Seja Bem-Vindo ao U-Code, um jogo simples onde você é o desenvolvedor!\n'+\
                           'Seu objetivo neste nível é atribuir o valor 10 à variável x. Não há regras!'
                        
        x = 0

        var_names = ['x']
        self.variables_dict = dict([(k, locals().get(k, None)) for k in var_names])              
        self.prefix_code = f'# Código Prefixo\n'+\
                            'x = 0'+\
                            '\n\n\n\n'+\
                           f'#{"="*15}\n'+\
                           f'# Seu Código aqui <-\n'+\
                           f'#{"="*15}\n\n'
        self.answer_var_name = 'x'
        self.expected_answer = 10
        self.sufix_code = f'\n# Código Sufixo\ncheck(x == {self.expected_answer})'