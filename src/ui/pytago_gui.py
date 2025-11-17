from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from board import Board


class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        rules = Button(text="Règles", pos = [30, 30], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")

        self.plateau1 = Board(250, 275, 300, self, 0, [1, 0, 0, 1], rotate, 300, 475)
        self.plateau2 = Board(250, 525, 300, self, 1, [0, 0, 1, 1], rotate, 550, 475)
        self.plateau3 = Board(250, 275, 50, self, 2, [0, 1, 0, 1], rotate, 300, 225)
        self.plateau4 = Board(250, 525, 50, self, 3, [1, 1, 0, 1], rotate, 550, 225)
        mode_solo.bind(on_press = lambda x: self.lancer(x))
        reset_game.bind(on_press = lambda x: self.reset(x))

        self.add_widget(reset_game)
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(rules)   
    
    def lancer(self, instance):
        win = False
        self.plateau1.board.disabled = False
        self.plateau2.board.disabled = False
        self.plateau3.board.disabled = False
        self.plateau4.board.disabled = False
        for i in range(3):
            for j in range(3):
                self.plateau1.case[i*3 + j].case.disabled = False
                self.plateau2.case[i*3 + j].case.disabled = False
                self.plateau3.case[i*3 + j].case.disabled = False
                self.plateau4.case[i*3 + j].case.disabled = False

    def reset(self, instance):
        self.plateau1.clear_board()
        self.plateau2.clear_board()
        self.plateau3.clear_board()
        self.plateau4.clear_board()

def rotate(self):
    print("test")

class MyApp(App):
    def build(self):
        return LoginScreen()

MyApp().run()