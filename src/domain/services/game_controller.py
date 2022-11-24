import pygame, pygame_textinput, sys


playing = False

def handle_events(game, events):
    """Iterates through each event and call it's appropriate function.
    Args:
        game (Game): The currently running game.
    """
    for event in events:
        if event.type == pygame.QUIT:
            quit_app()
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event.key, game)
        elif event.type == pygame.KEYUP:
            handle_keyup(event.key, game)
                
                
def handle_keydown(key, game):
    """Decides what to do with the key pressed by the user.
    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key not in game.pressed_keys:
        game.pressed_keys.append(key)
        
    if key == pygame.K_F5:
        quit_app()
    

def handle_keyup(key, game):
    """Decides what to do with the key released by the user.
    Args:
        key (int): The pygame keycode of the key.
        game (Game): The currently running game.
    """
    if key in game.pressed_keys:
        game.pressed_keys.remove(key)

def quit_app():
    """Stops the game and closes application.
    """
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
def setup():
    """Sets some configurations for the game.
    """
    pygame.key.set_repeat(200, 25)
    
    
#command keys
cmd_keys = [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
def validate_input(txt: pygame_textinput.TextInputVisualizer, key):

    if txt.size != (0,0) and txt.get_line_width(txt.manager.y_cursor) + txt.padding[0] + txt.border_width > txt.size[0] and key not in cmd_keys:
        return False
    
    if (key == pygame.K_KP_ENTER or key == pygame.K_RETURN) and txt.surface.get_height() + txt.font_object.get_height() > txt.size[1] - (txt.border_width*2):
        return False
    
    return True




# x = 10
# y = 0

# var_names = ['x', 'y']
# var_dict = dict([(k, locals().get(k, None)) for k in var_names])

# cmd = '''
# y = x*2
# '''
# exec(cmd)
# print(y)
