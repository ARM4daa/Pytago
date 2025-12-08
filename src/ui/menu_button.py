from kivy.uix.button import Button

class MenuButton:
    def __init__(self, text_mb, pos_mb, size_mb, background_mb):
        self.menu_button = Button(text = text_mb, pos = pos_mb, size_hint = [None, None], size = size_mb, background_normal = background_mb)
    
    def print_rules(self):
        pass

    def play_with_two_player(self):
        pass
    
    def play_with_one_player(self):
        pass

    def restart(self):
        pass
