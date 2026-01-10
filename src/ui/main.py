"""
@file main.py

@brief Create the link between GUI and bitboards.

@section author_sensors Author(s)
- Created by Baptiste Farcy
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from ui.board import Board
from kivy.uix.label import Label
from kivy.config import Config
from time import sleep
from ui.player import Player
import wrappers.pytago_core as core
import wrappers.pytago_ai as ai

#Window config
Config.set('graphics', 'width', '900') 
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 275], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        self.level_ai_more = Button(text='+', pos = [140,340], size_hint = [None, None], size = [50, 50], background_normal = "Image/buttonBackground.PNG")
        self.level_ai_less = Button(text='-', pos = [70,340], size_hint = [None, None], size = [50, 50], background_normal = "Image/buttonBackground.PNG")
        self.board = Board([300, 50], 250, self.play, self)

        mode_solo.bind(on_press = lambda x: self.solo_mode_game(x))
        mode_duo.bind(on_press = lambda x: self.duo_mode_game(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        self.level_ai_less.bind(on_press = lambda x: self.level_ia_sub(x))
        self.level_ai_more.bind(on_press = lambda x: self.level_ia_add(x))

        self.bitboard_me = 0
        self.bitboard_opp = 0
        self.single_player = False
        self.ai_to_play = False
        self.level = 6
        self.recursion = False
        self.level_ai_label = Label(text =f"{self.level}", pos =[-320, 65])

        self.add_widget(Label(text="--------------- Règles ----------------\nEn mode solo : \nSelectionnez le niveau de l'IA avant\nde débuter la partie.\nEn mode duo : Amusez-vous contre\nvos amis\n\nLe jeu : \n- Placer une bille sur une case libre\n- Selectionner un plateau et tournez le\n Le but ? Alignez 5 billes de la même \ncouleur pour remporter la partie !", pos=[-315, -150]))
        self.add_widget(reset_game) 
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(self.level_ai_more)
        self.add_widget(self.level_ai_less)
        self.add_widget(Label(text="Niveau de l'IA (1 à 6) :", pos = [-315, 105]))
        self.add_widget(self.level_ai_label)

    def level_ia_add(self, instance):
        """
        @brief level_ia_add.

        Increase the level of AI.

        @param self: object of LoginScreen
        @param instance: button object
        @return None
        """
        if self.level < 6:
            self.level += 1
            self.level_ai_label.text = str(self.level)
    
    def level_ia_sub(self, instance):
        """
        @brief level_ia_sub.

        Decrease the level of AI.

        @param self: object of LoginScreen
        @param instance: button object
        @return None
        """

        if self.level > 1:
            self.level -= 1
            self.level_ai_label.text = str(self.level)
            print(self.level)

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
        self.level_ai_more.disabled = True
        self.level_ai_less.disabled = True


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
        self.level_ai_more.disabled = False
        self.level_ai_less.disabled = False

    def apply_move(self, move):
        """
        @brief apply_move.

        apply a move from the GUI to the bitboard associated to a specific player

        @param self: object of LoginScreen
        @param move: button object
        @return None
        """

        self.bitboard_me = core.place_marble(self.bitboard_me, move[0])

        if move[2]:
            self.bitboard_me = core.rotate_board_clockwise(self.bitboard_me, move[1])
            self.bitboard_opp = core.rotate_board_clockwise(self.bitboard_opp, move[1])
        else:
            self.bitboard_me = core.rotate_board_aclockwise(self.bitboard_me, move[1])
            self.bitboard_opp = core.rotate_board_aclockwise(self.bitboard_opp, move[1])

        if core.is_won(self.bitboard_me):
            sleep(2)
            self.board.win_game()
            self.level_ai_more = True
            return 1
        
        if core.is_won(self.bitboard_opp):
            sleep(2)
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

class Pytago(App):
    def build(self):
        self.icon = "Image/marbles.png"
        return LoginScreen()

Pytago().run()
