from player import Player
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior

class Box(ButtonBehavior):
    def __init__(self, pos_xy, disable_all_boxes, able_all_boards, id_board, id_box, move):
        """
        Doc
        """
        self.free = True                            #Used to determine whether the square is playable
        
        #Create the representation of the box in the game
        self.box = Button(
            pos = pos_xy, 
            size = [50, 50],
            size_hint = (None, None), 
            background_normal = "test_placement.jpeg",
            background_disabled_normal = "test_placement.jpeg",
            disabled = True,
            border = [0, 0, 0, 0]
        )
        self.box.bind(on_press = lambda x: self.play(x))

        #Used to turn management; They are functions of Board class
        self.disable_all_boxes = disable_all_boxes              
        self.able_all_boards = able_all_boards  

        self.move = move

        values = {0: 8,
         1: 4,
         2: 7,
         3: 1,
         4: 0,
         5: 3,
         6: 5,
         7: 2,
         8: 6}

        self.value = 2 ** (values[id_box] + (3 - id_board)*9)

    
    def play(self, instance):
        """
        Doc
        """
        #If a ball isn't in the boxe
        if self.free:
            self.free = False

            #Player 1
            if Player.player:
                self.box.background_normal = "billeNoire.PNG"
                self.box.background_disabled_normal = "billeNoire.PNG"

            #Player 2
            else:
                self.box.background_normal = "billeBlanche.PNG"
                self.box.background_disabled_normal = "billeBlanche.PNG"
        
            #Gestion of the rest of the turn
            self.disable_all_boxes()
            self.able_all_boards()

            #Return value to modify bitboard
            self.move[0] = self.value