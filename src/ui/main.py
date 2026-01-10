"""
@file main.py

@brief Create the link between GUI and bitboards.

"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from board import Board
from kivy.uix.label import Label
from kivy.config import Config
Config.set('graphics', 'width', '900') 
Config.set('graphics', 'height', '600')
from time import sleep
from player import Player

"import pytago_core as core"
"import pytago_ai as ai"

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        reset_game = Button(text="Recommencer une partie", pos = [30, 500], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        mode_duo = Button(text="Jouer à 2", pos = [30, 275], size_hint = [None, None], size = [200, 50], background_normal = "Image/buttonBackground.PNG")
        level_ai_more = Button(text='+', pos = [140,350], size_hint = [None, None], size = [50, 50], background_normal = "Image/buttonBackground.PNG")
        level_ai_less = Button(text='-', pos = [70,350], size_hint = [None, None], size = [50, 50], background_normal = "Image/buttonBackground.PNG")
        self.board = Board([300, 50], 250, self.play, self)

        mode_solo.bind(on_press = lambda x: self.solo_mode_game(x))
        mode_duo.bind(on_press = lambda x: self.duo_mode_game(x))
        reset_game.bind(on_press = lambda x: self.reset(x))
        level_ai_less.bind(on_press = lambda x: self.level_ia_sub(x))
        level_ai_more.bind(on_press = lambda x: self.level_ia_add(x))

        self.bitboard_me = 0
        self.bitboard_opp = 0
        self.single_player = False
        self.ai_to_play = False
        self.level = 3
        self.recursion = False
        self.level_ai_label = Label(text =f"{self.level}", pos =[-320, 75])

        self.add_widget(Label(text="--------------- Règles ----------------\nUn tour est décomposé en \ndeux parties : \n- Placer une bille sur une \ncase libre\n- Selectionner un plateau \n- Tourner le plateau de son \nchoix\nAlignez 5 billes de la même \ncouleur pour remporter la \nvictoire !", pos=[-315, -125]))
        self.add_widget(reset_game) 
        self.add_widget(mode_solo)
        self.add_widget(mode_duo)
        self.add_widget(level_ai_more)
        self.add_widget(level_ai_less)
        self.add_widget(Label(text="Niveau de l'IA (1 à 6)", pos = [-315, 110]))
        self.add_widget(self.level_ai_label)

    def level_ia_add(self, instance):
        if self.level < 6:
            self.level += 1
            self.level_ai_label.text = str(self.level)
            
    
    def level_ia_sub(self, instance):
        if self.level > 1:
            self.level -= 1
            self.level_ai_label.text = str(self.level)
    
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
                #self.apply_move(best)
                self.recursion = True
                self.board.apply_move(best)
                self.recursion = False
                self.ai_to_play = False
            else:
                #won = self.apply_move(self.board.move)
                if not won:
                    self.ai_to_play = True
                    #self.play()
        else:
            pass
            #self.apply_move(self.board.move)

class Pytago(App):
    def build(self):
        return LoginScreen()

Pytago().run()