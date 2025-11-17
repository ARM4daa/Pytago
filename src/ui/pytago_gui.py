from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from main_board import Board


class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        rules = Button(text="Règles", pos = [30, 30], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        
        self.board = Board([275, 50], 250, rotate, self)

        mode_solo.bind(on_press = lambda x: self.lancer(x))
        reset_game.bind(on_press = lambda x: self.reset(x))

        self.add_widget(reset_game)
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(rules)   
    
    def lancer(self, instance):
        win = False
        self.board.able_board()
        self.board.able_case()

    def reset(self, instance):
        self.board.reset_board()
    
def rotate(self):
    print("test")

class MyApp(App):
    def build(self):
        return LoginScreen()

MyApp().run()