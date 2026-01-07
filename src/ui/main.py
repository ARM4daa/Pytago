"""
@file main.py

@brief Create the link between GUI and bitboards.

"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from board import Board
from kivy.clock import Clock
import pytago_core as core
import pytago_ai as ai
from time import sleep
from player import Player

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        rules = Button(text="Règles", pos = [30, 25], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        button_test_win = Button(text="Fausse victoire", pos = [30, 100], size_hint = [None, None], size = [200, 50], background_normal = "fond_test.PNG")
        
        self.board = Board([275, 50], 250, self.play, self)

        mode_solo.bind(on_press = lambda x: self.solo_mode_game(x))
        mode_duo.bind(on_press = lambda x: self.duo_mode_game(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        button_test_win.bind(on_press = lambda x: self.win_game(x))

        self.add_widget(reset_game)
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(rules)
        self.add_widget(button_test_win)

        self.bitboard_me = 0
        self.bitboard_opp = 0
        self.single_player = False
        self.ai_to_play = False
        self.level = 7
        self.recursion = False
    
    def solo_mode_game(self, instance):
        """
        @brief solo_mode_game.

        This function is launching when the player want to play solo againdt an ia.
        It define the variable "single_player" to true.      

        @param self: object of LoginScreen
        @param instance: A REMPLIR
        @return None
        """

        self.single_player = True
        self.run_game(instance)

    def duo_mode_game(self, instance):
        """
        @brief duo_mode_game.

        This function is launching when two player want to play together.
        It define the variable "single_player" to false. 

        @param self: object of LoginScreen
        @param instance: A REMPLIR
        @return None
        """

        self.single_player = False
        self.run_game(instance)
        
    def run_game(self, instance):
        """
        @brief run_game.

        Initialize boards to start the game.

        @param self: object of LoginScreen
        @param instance: button object
        @return None
        """

        self.reset(instance)
        self.board.able_box()

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

        "print(bin(self.bitboard_me)[2:].zfill(36))"
        self.bitboard_me = core.place_marble(self.bitboard_me, move[0])
        print(move)
        if move[2]:
            self.bitboard_me = core.rotate_board_clockwise(self.bitboard_me, move[1])
            self.bitboard_opp = core.rotate_board_clockwise(self.bitboard_opp, move[1])
        else:
            self.bitboard_me = core.rotate_board_aclockwise(self.bitboard_me, move[1])
            self.bitboard_opp = core.rotate_board_aclockwise(self.bitboard_opp, move[1])
        """
        print("me : ", end="")
        print(bin(self.bitboard_me)[2:].zfill(36), end=": ")
        print(core.is_won(self.bitboard_me))
        print("opp: ", end="")
        print(bin(self.bitboard_opp)[2:].zfill(36), end=": ")
        print(core.is_won(self.bitboard_opp))
        print()
        """
        if core.is_won(self.bitboard_me):
            print("winnnn") #A SUPPRIMER
            sleep(1)
            self.board.win_game()
            return 1
        if core.is_won(self.bitboard_opp):
            sleep(1)
            Player.player = 0 if Player.player else 1
            self.board.win_game()
            return 1
        self.bitboard_me, self.bitboard_opp = self.bitboard_opp, self.bitboard_me
        
    def play(self):
        """
        @brief play.

        The function will control the game and choose the player to play.
        
        If you will play in solo mode, the ai is call else you can play with you friend

        @param self: object of LoginScreen
        @return None
        """

        if self.recursion :
            return None
        if self.single_player:
            if self.ai_to_play:
                print(self.level)
                print(bin(self.bitboard_me)[2:].zfill(36))
                print(bin(self.bitboard_opp)[2:].zfill(36))
                best = ai.get_best_move(self.bitboard_me, self.bitboard_opp, self.level)
                self.apply_move(best)
                self.recursion = True
                self.board.apply_move(best)
                self.recursion = False
                self.ai_to_play = False
            else:
                won = self.apply_move(self.board.move)
                if not won:
                    self.ai_to_play = True
                    self.play()
        else:
            self.apply_move(self.board.move)

class MyApp(App):
    def build(self):
        return LoginScreen()

print(core.is_won(0b000000001010100001010000001000000000)) #A SUPPRIMER
MyApp().run()