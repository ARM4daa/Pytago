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
        rules = Button(text="Règles", pos = [30, 25], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        button_test_win = Button(text="Fausse victoire", pos = [30, 100], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        
        self.board = Board([275, 50], 250, rotate, self)

        mode_solo.bind(on_press = lambda x: self.run_party(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        button_test_win.bind(on_press = lambda x: self.win(x))
        self.win_p = True

        self.add_widget(reset_game)
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(rules)
        self.add_widget(button_test_win)   
    
    def run_party(self, instance):
        self.win_p = True
        self.board.able_board()
        self.board.able_box()

    
    def win(self, instance):
        """ Function to test winning animation """
        if self.win_p:
            self.board.win_party()

    def reset(self, instance):
        """ Reset the game """
        self.board.reset_board()
    
def rotate(self):
    """ Rotate function for bitboard """
    print("test")

class MyApp(App):
    def build(self):
        return LoginScreen()

MyApp().run()