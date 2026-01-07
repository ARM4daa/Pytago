"""
@file main.py

@brief Create the link between GUI and bitboards.

@section author_sensors Author(s)
- Created by Baptiste Farcy

"""


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from board import Board
from kivy.clock import Clock
from kivy.uix.label import Label
from player import Player
"import pytago_core as core"
"import pytago_ai as ai"

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        button_test_win = Button(text="Fausse victoire", pos = [30, 100], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        
        self.board = Board([275, 50], 250, self.play, self)

        mode_duo.bind(on_press = lambda x: self.run_game(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        button_test_win.bind(on_press = lambda x: self.win(x))

        self.add_widget(Label(text="--------------- Règles ----------------\nUn tour est décomposé en \ndeux parties : \n- Placer une bille sur une \ncase libre\n- Tourner le plateau de son \nchoix\nAlignez 5 billes de la même \ncouleur pour remporter la \nvictoire !", pos=[-265, -50]))
        self.add_widget(reset_game) 
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(button_test_win)

        self.bitboard_me = 0
        self.bitboard_opp = 0
        self.single_player = False
        self.ai_to_play = False
        self.level = 1
    
    def run_game(self, instance):

        """
        @brief run_game.

        Initialize boards to start the game.

        @param self: object of LoginScreen
        @param instance: button object
        @return None
        """
        self.reset(instance)
        Player.player = 0
        self.board.able_boxes()

    def win(self, instance):
        """Try victory animation"""
        self.index = 0
        self.ordre = [6, 3, 0, 1, 2, 5, 8, 7, 4]
        self.event_victory = Clock.schedule_interval(self.test_win, 0.3)

    def test_win(self, dt):
        for i in range(4):
            self.board.boards[i].box[self.ordre[self.index]].box.background_disabled_normal = "billeNoire.PNG"
            self.board.boards[i].box[self.ordre[self.index]].box.background_normal = "billeNoire.PNG"
        
        if self.index >= 8:
            Clock.unschedule(self.event_victory)
        else:
            self.index += 1

    def reset(self, instance):
        """
        @brief reset.

        Reset the board to the initial state to start a new game.

        @param self: object of LoginScreen
        @param instance: button object
        @return None
        """

        self.board.reset_board()
        self.bitboard_me = 0
        self.bitboard_opp = 0

    def apply_move(self, move):
        """
        @brief apply_move.

        apply a move from the GUI to the bitboard associated to a specific player

        @param self: object of LoginScreen
        @param move: button object
        @return None
        """

        self.bitboard_me = core.place_marble(self.bitboard_me, move[0])
        if core.is_won(self.bitboard_me):
            self.board.win_game()
        else:
            if self.board.move[2]:
                core.rotate_board_clockwise(self.bitboard_me, move[1])
                core.rotate_board_clockwise(self.bitboard_opp, move[1])
            else:
                core.rotate_board_aclockwise(self.bitboard_me, move[1])
                core.rotate_board_aclockwise(self.bitboard_opp, move[1])
            self.bitboard_me, self.bitboard_opp = self.bitboard_opp, self.bitboard_me
        
    def play(self):
        """
        @brief play.

        The function will control the game and choose the player to play.
        
        If you will play in solo mode, the ai is call else you can play with you friend

        @param self: object of LoginScreen
        @return None
        """
        if self.single_player:
            if self.ai_to_play:
                best = ai.get_best_move(self.bitboard_me, self.bitboard_opp, self.level)
                self.apply_move(best)
            else:
                self.apply_move(self.board.move)
            self.ai_to_play = not self.ai_to_play
        else:
            self.apply_move(self.board.move)

class MyApp(App):
    def build(self):
        return LoginScreen()

MyApp().run()