from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from main_board import Board
import pytago_core as core

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        rules = Button(text="Règles", pos = [30, 25], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        button_test_win = Button(text="Fausse victoire", pos = [30, 100], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        
        self.board = Board([275, 50], 250, self.apply_move, self)

        mode_solo.bind(on_press = lambda x: self.run_party(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        button_test_win.bind(on_press = lambda x: self.win(x))
        self.win_p = True

        self.add_widget(reset_game)
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(rules)
        self.add_widget(button_test_win)

        self.mainloop()
    
    def run_party(self, instance):
        self.win_p = True
        self.board.able_board()
        self.board.able_box()

    def reset(self, instance):
        """ Reset the game """
        self.board.reset_board()
        self.bitboard_me = 0
        self.bitboard_opp = 0
        
    def apply_move(self):
        """ Rotate function for bitboard """
        self.bitboard_me = core.place_marble(self.bitboard_me, self.board.move[0])
        if core.is_won(self.bitboard_me):
            self.board.win_party()
        else:
            if self.board.move[2]:
                core.rotate_board_clockwise(self.bitboard_me, self.board.move[1])
                core.rotate_board_clockwise(self.bitboard_opp, self.board.move[1])
            else:
                core.rotate_board_aclockwise(self.bitboard_me, self.board.move[1])
                core.rotate_board_aclockwise(self.bitboard_opp, self.board.move[1])
            self.bitboard_me, self.bitboard_opp = self.bitboard_opp, self.bitboard_me

    def mainloop(self):
        self.bitboard_me = 0
        self.bitboard_opp = 0
        self.single_player = False


class MyApp(App):
    def build(self):
        return LoginScreen()

MyApp().run()