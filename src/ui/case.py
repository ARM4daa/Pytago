from kivy.uix.button import Button
from player import Player

class Case():
    def __init__(self, pos_xy):
        self.player = None
        self.free = True
        self.case = Button(pos = pos_xy, size = [50, 50], size_hint = (None, None), background_color = (1, 1, 1, 1), disabled = True)
        self.case.bind(on_press = lambda x: self.play(x))
    
    def play(self, instance):
        if self.free:
            self.free = False
            self.player = Player.joueur
            if self.player:
                self.case.background_color = (1, 0, 0, 1)
            else:
                self.case.background_color = (0, 1, 0, 1)