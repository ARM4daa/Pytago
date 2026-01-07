from subboard import SubBoard
from kivy.uix.button import Button
from player import Player
from kivy.clock import Clock

class Board:
    def __init__(self, pos, size, apply_move, selfmain):
        self.move = [0, 0, 0]
        self.button1 = Button(pos=[25, 150], size_hint = [None, None], size = [75, 75])
        self.button2 = Button(pos=[125, 150], size_hint = [None, None], size = [75, 75])
        self.boards = (
            SubBoard(size, pos[0],          pos[1] + size, selfmain, 0, apply_move, 290, 465, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2), 
            SubBoard(size, pos[0] * 2 - 25, pos[1] + size, selfmain, 1, apply_move, 540, 465, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0],          pos[1],        selfmain, 2, apply_move, 290, 215, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0] * 2 - 25, pos[1],        selfmain, 3, apply_move, 540, 215, self.move, self.disable_box, self.able_box, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2)
        )
        self.layout = selfmain

        #Si on veut faire des rotations via deux boutons seuls :
        #selfmain.add_widget(self.button1)
        #selfmain.add_widget(self.button2)

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
        self.index = 0
        self.ordre = [6, 3, 0, 1, 2, 5, 8, 7, 4]
        self.event_victory = Clock.schedule_interval(self.test_win, 0.3)
        self.disable_board()
        self.disable_box()

    def test_win(self, dt):
        if Player.player == 0:
            img = "billeBlanche.PNG"
        else:
            img = "billeNoire.PNG"
        for i in range(4):
            self.boards[i].box[self.ordre[self.index]].box.background_disabled_normal = img
            self.boards[i].box[self.ordre[self.index]].box.background_normal = img
        
        if self.index >= 8:
            Clock.unschedule(self.event_victory)
        else:
            self.index += 1