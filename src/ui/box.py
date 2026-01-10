"""
@file box.py

@brief Representation of the Box

@section author_sensors Author(s)
- Created by Léo Ethoré
"""

from player import Player
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from time import sleep

class Box(ButtonBehavior):
    def __init__(self, pos_xy, disable_all_boxes, able_all_boards, id_board, id_box, move):
        """
        @brief __init__

        Constructor of Box

        @param self: Box object
        @param pos_xy: list with positoin x and y of the Box
        @param disable_all_boxes: function to disable all boxes on the board 
        @param able_all_boards: function to able all boxes on the board 
        @param id_board: specific id of the subboard
        @param id_box: specific id of the box
        @param move: list containing the information transmitted to the bitboard
        @return None
        """
        self.free = True                            #Used to determine whether the square is playable
        
        #Create the representation of the box in the game
        self.box = Button(
            pos = pos_xy, 
            size = [70, 70],
            size_hint = (None, None), 
            background_normal = "Image/border.PNG",
            background_disabled_normal = "Image/border.PNG",
            disabled = True,
            border = [0, 0, 0, 0]
        )
        self.box.bind(on_press = lambda x: self.play(x))

        #Used to turn management; They are functions of Board class
        self.disable_all_boxes = disable_all_boxes              
        self.able_all_boards = able_all_boards  

    
        #The next part is used to transform a case from a board to a power of 2 sends to the bitboard
        
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
        @brief play

        Place a marble on a box

        @param self: Box object
        @param instance: Button object
        @return None
        """
        #If a marble isn't in the box
        if self.free:
            self.free = False

            #Player 2
            if Player.player:
                self.box.background_normal = "Image/blackMarble.PNG"
                self.box.background_disabled_normal = "Image/blackMarble.PNG"

            #Player 1
            else:
                self.box.background_normal = "Image/whiteMarble.PNG"
                self.box.background_disabled_normal = "Image/whiteMarble.PNG"
        
            #Gestion of the rest of the turn
            self.disable_all_boxes()
            self.able_all_boards()

            #Return value to modify bitboard
            self.move[0] = self.value