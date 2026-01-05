from subboard import SubBoard
from kivy.uix.button import Button
from kivy.uix.label import Label
from player import Player
import math

class Board:
    def __init__(self, pos, size, apply_move, selfmain):
        self.move = [0, 0, 0]
        self.button1 = Button(pos=[25, 150], size_hint = [None, None], size = [75, 75])
        self.button2 = Button(pos=[125, 150], size_hint = [None, None], size = [75, 75])
        self.boards = (
            SubBoard(size, pos[0],          pos[1] + size, selfmain, 0, apply_move, 300, 475, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2), 
            SubBoard(size, pos[0] * 2 - 25, pos[1] + size, selfmain, 1, apply_move, 550, 475, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0],          pos[1],        selfmain, 2, apply_move, 300, 225, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0] * 2 - 25, pos[1],        selfmain, 3, apply_move, 550, 225, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2)
        )
        self.layout = selfmain
                
        self.values_reverse = {8: 0,
         4: 1,
         7: 2,
         1: 3,
         0: 4,
         3: 5,
         5: 6,
         2: 7,
         6: 8}

        #Si on veut faire des rotations via deux boutons seuls :
        #selfmain.add_widget(self.button1)
        #selfmain.add_widget(self.button2)

    def apply_move(self,move) :
        
        """
        @brief apply_move.

        calculate the case with the power of 2 associate and place the ball

        @param self: object of Board
        @param move: the move gives by the AI to apply on the board
        @return None
        """

        values = (int(3-math.log2(move[0])//9), self.values_reverse[math.log2(move[0])%9])
        self.boards[values[0]].box[values[1]].play(None)
        if move[2] :
            self.boards[move[1]].rotate_right(None)
        else :
            self.boards[move[1]].rotate_left(None)

    def able_board(self):
        for elt in self.boards:
            elt.able_board()
    
    def disable_board(self):
        for elt in self.boards:
            elt.disable_board()
    
    
    def disable_box(self):
        for elt in self.boards:
            elt.disable_box()
    
    def able_box(self):
        for elt in self.boards:
            elt.able_box()

    def reset_board(self):
        for i in range(4):
            self.boards[i].disable_board()
            self.boards[i].disable_box()
            self.boards[i].clear_board()
            
    def disable_rotate_button(self):
        for elt in self.boards:
            elt.button1.disabled = True
            elt.button2.disabled = True
    
    def able_rotate_button(self):
        for elt in self.boards:
            elt.button1.disabled = False
            elt.button2.disabled = False

    def print_button_rotate(self, btn):
        button1 = Button(text="Gauche", size_hint=(None, None), size=(50, 50), pos = (0, 0))
        button2 = Button(text="Droite", size_hint=(None, None), size=(50, 50), pos = (0, 0))

        button1.bind(on_press = lambda x: SubBoard.rotate_left(x))
        button2.bind(on_press = lambda x: SubBoard.rotate_right(x))

        self.layout.add_widget(button1)
        self.layout.add_widget(button2)
    
    def win_game(self):
        self.layout.add_widget(Label(text = f"Player {Player.player} wiiiiiiiiiiiiiiiin ! "))