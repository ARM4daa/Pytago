from player import Player
from kivy.uix.button import Button

class Box():
    def __init__(self, pos_xy, disable_all_boxes, able_all_boards, id_board, id_box):
        """
        Doc
        """
        self.free = True                            #Used to determine whether the square is playable
        
        #Create the representation of the box in the game
        self.box = Button(
            pos = pos_xy, 
            size = [50, 50],
            size_hint = (None, None), 
            background_color = (1, 1, 1, 0), 
            disabled = True
        )
        self.box.bind(on_press = lambda x: self.play(x))

        #Used to turn management; They are functions of Board class
        self.disable_all_boxes = disable_all_boxes              
        self.able_all_boards = able_all_boards  

        self.id_box = (id_board, id_box)            #Identity of the box on the main board   
    
    def play(self, instance):
        """
        Doc
        """
        #If a ball isn't in the boxe
        if self.free:
            self.free = False

            #Player 1
            if Player.player:
                self.box.background_color = (1, 0, 0, 1)

            #Player 2
            else:
                self.box.background_color = (0, 1, 0, 1)
        
            #Gestion of the rest of the turn
            self.disable_all_boxes()
            self.able_all_boards()

            #Return value to modify bitboard
            return self.id_box