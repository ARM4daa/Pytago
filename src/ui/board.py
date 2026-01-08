from subboard import SubBoard
from kivy.uix.button import Button
from player import Player
from kivy.clock import Clock
 
class Board:
    def __init__(self, pos, size, apply_move, layout):
        """
        @brief __init__

        Constructor of Board 

        @param self: Board object
        @param pos: position of Board
        @param size: size of a subboard
        @param apply_move: function to apply a move to the bitboard
        @param layout: LoginScreen object
        @return None
        """
        self.move = [0, 0, 0]
        self.button1 = Button(pos=[25, 150], size_hint = [None, None], size = [75, 75])
        self.button2 = Button(pos=[125, 150], size_hint = [None, None], size = [75, 75])
        self.boards = (
            SubBoard(size, pos[0],          pos[1] + size, layout, 0, apply_move, 290, 465, self.move, self.disable_boxes, self.able_boxes, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2), 
            SubBoard(size, pos[0] * 2 - 25, pos[1] + size, layout, 1, apply_move, 540, 465, self.move, self.disable_boxes, self.able_boxes, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0],          pos[1],        layout, 2, apply_move, 290, 215, self.move, self.disable_boxes, self.able_boxes, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2),
            SubBoard(size, pos[0] * 2 - 25, pos[1],        layout, 3, apply_move, 540, 215, self.move, self.disable_boxes, self.able_boxes, self.disable_board, self.able_board, self.disable_rotate_button, self.able_rotate_button, self.button1, self.button2)
        )
        self.layout = layout

        #Si on veut faire des rotations via deux boutons seuls :
        #layout.add_widget(self.button1)
        #layout.add_widget(self.button2)

    def able_board(self):
        """
        @brief able_board

        The board become clickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.able_board()
    
    def disable_board(self):
        """
        @brief disable_board

        The board become unclickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.disable_board()
    
    def disable_boxes(self):
        """
        @brief able_board

        The boxes become unclickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.disable_boxes()
    
    def able_boxes(self):
        """
        @brief able_boxes

        The boxes become clickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.able_boxes()

    def reset_board(self):
        """
        @brief reset_board

        The board become blank

        @param self: Board object
        @return None
        """
        for i in range(4):
            self.boards[i].disable_board()
            self.boards[i].disable_boxes()
            self.boards[i].clear_board()
            
    def disable_rotate_button(self):
        """
        @brief disable_rotate_button

        The rotate buttons become unclickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.button1.disabled = True
            elt.button2.disabled = True
    
    def able_rotate_button(self):
        """
        @brief able_rotate_button

        The rotate buttons become clickable

        @param self: Board object
        @return None
        """
        for elt in self.boards:
            elt.button1.disabled = False
            elt.button2.disabled = False

    def print_rotate_button(self, btn):
        """
        @brief print_rotate_button

        The rotate buttons become usable

        @param self: Board object
        @param btn: Button object
        @return None
        """
        button1 = Button(text="Gauche", size_hint=(None, None), size=(50, 50), pos = (0, 0))
        button2 = Button(text="Droite", size_hint=(None, None), size=(50, 50), pos = (0, 0))

        button1.bind(on_press = lambda x: SubBoard.rotate_left(x))
        button2.bind(on_press = lambda x: SubBoard.rotate_right(x))

        self.layout.add_widget(button1)
        self.layout.add_widget(button2)
    
    def win_game(self):
        """
        @brief win_game

        Displays the victory animation

        @param self: Board object
        @return None
        """
        self.index = 0
        self.ordre = [6, 3, 0, 1, 2, 5, 8, 7, 4]
        self.event_victory = Clock.schedule_interval(self.animation_win, 0.3)
        self.disable_board()
        self.disable_boxes()

    def animation_win(self, dt):
        """
        @brief win_game

        Displays the victory animation

        @param self: Board object
        @param dt: time (sec)
        @return None
        """
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