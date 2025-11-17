from board import SubBoard
from kivy.uix.button import Button

class Board:
    def __init__(self, pos, size, rotate, selfmain):
        self.update_move = tuple()
        self.boards = (
            SubBoard(size, pos[0],          pos[1] + size, selfmain, 0, rotate, 300, 475, self.update_move), 
            SubBoard(size, pos[0] * 2 - 25, pos[1] + size, selfmain, 1, rotate, 550, 475, self.update_move),
            SubBoard(size, pos[0],          pos[1],        selfmain, 2, rotate, 300, 225, self.update_move),
            SubBoard(size, pos[0] * 2 - 25, pos[1],        selfmain, 3, rotate, 550, 225, self.update_move)
        )
        self.layout = selfmain

    def update_move(self, num_board, index_box, sens):
        self.update_move = (num_board, index_box, sens)

    def able_board(self):
        for elt in self.boards:
            elt.able_board()
    
    def disable_board(self):
        for elt in self.boards:
            elt.disable_board()
    
    def disable_case(self):
        for elt in self.boards:
            elt.disable_case()
    
    def able_case(self):
        for elt in self.boards:
            elt.able_case()

    def reset_board(self):
        for i in range(4):
            self.boards[i].disable_board()
            self.boards[i].disable_case()
            self.boards[i].clear_board()

    def print_button_rotate(self, btn):
        button1 = Button(text="Gauche", size_hint=(None, None), size=(50, 50), pos = (0, 0))
        button2 = Button(text="Droite", size_hint=(None, None), size=(50, 50), pos = (0, 0))

        button1.bind(on_press = lambda x: SubBoard.rotate_left(x))
        button2.bind(on_press = lambda x: SubBoard.rotate_right(x))

        self.layout.add_widget(button1)
        self.layout.add_widget(button2)