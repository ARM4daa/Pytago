from kivy.uix.button import Button
from player import Player

class SubBoard:
    def __init__(self, board_size, pos_x, pos_y, layout, num_board, main_rotate, x_first_case, y_first_case, move):
        """
        Doc
        """
        self.board_size = board_size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.layout_ajout = layout
        self.num_board = num_board
        self.handler_rotate = main_rotate
        self.button1 = None
        self.button2 = None
        self.move = move

        self.board = Button(pos=[self.pos_x, self.pos_y], size=[self.board_size, self.board_size], size_hint=[None, None], disabled = True, background_normal = "board_wood.PNG")
        self.board.bind(on_press = lambda x: self.print_button_rotate(x))
        
        self.case = []
        
        for i in range(3):            
            for j in range(3):    
                self.case.append(Case([x_first_case + i*75, y_first_case - j*75]))
        

        #Print board then boxe
        layout.add_widget(self.board)
        self.print_case()


    def print_case(self):
        """ Displays the status of the 9 boxes on the board """
        for i in range(3):            
            for j in range(3):    
                self.layout_ajout.remove_widget(self.case[i*3 + j].case)        
                self.layout_ajout.add_widget(self.case[i*3+ j].case)    


    def disable_board(self):
        """ Disable the board """
        self.board.disabled = True

    def able_board(self):
        """ Able the board """
        self.board.disabled = False


    def disable_case(self):
        """ Disable 9 boxes of the board """
        for i in range(3):
            for j in range(3):
                self.case[i*3 + j].case.disabled = True
    
    def able_case(self):
        """ Able 9 boxes of the board """
        for i in range(3):
            for j in range(3):
                self.case[i*3 + j].case.disabled = False


    def print_button_rotate(self, btn):
        if self.button1 is not None:
            self.layout_ajout.remove_widget(self.button1)
            self.layout_ajout.remove_widget(self.button2)

        button1 = Button(text="Gauche", size_hint=(None, None), size=(50, 50))
        button2 = Button(text="Droite", size_hint=(None, None), size=(50, 50))

        if self.num_board == 0:
            button1.pos = (self.pos_x - 50, self.pos_y + 200)
            button2.pos = (self.pos_x, self.pos_y + 250)
        elif self.num_board == 1:
            button1.pos = (self.pos_x + self.board_size - 50, self.pos_y + 250)
            button2.pos = (self.pos_x + self.board_size, self.pos_y + 200)
        elif self.num_board == 2:
            button1.pos = (self.pos_x - 50, self.pos_y)
            button2.pos = (self.pos_x, self.pos_y -50)
        else:
            button1.pos = (self.pos_x + self.board_size - 50, self.pos_y - 50)
            button2.pos = (self.pos_x + self.board_size, self.pos_y)

        button1.bind(on_press = lambda x: self.rotate_left(x))
        button2.bind(on_press = lambda x: self.rotate_right(x))

        self.layout_ajout.add_widget(button1)
        self.layout_ajout.add_widget(button2)
    

    def rotate_right(self, instance):
        print("Droite")
        temp = [self.case[0].player, self.case[0].free, self.case[0].case.background_color]

        self.case[0].player, self.case[0].free, self.case[0].case.background_color = self.case[2].player, self.case[2].free, self.case[2].case.background_color
        self.case[2].player, self.case[2].free, self.case[2].case.background_color = self.case[8].player, self.case[8].free, self.case[8].case.background_color
        self.case[8].player, self.case[8].free, self.case[8].case.background_color = self.case[6].player, self.case[6].free, self.case[6].case.background_color
        self.case[6].player, self.case[6].free, self.case[6].case.background_color = temp

        temp = [self.case[1].player, self.case[1].free, self.case[1].case.background_color]
        
        self.case[1].player, self.case[1].free, self.case[1].case.background_color = self.case[5].player, self.case[5].free, self.case[5].case.background_color
        self.case[5].player, self.case[5].free, self.case[5].case.background_color = self.case[7].player, self.case[7].free, self.case[7].case.background_color
        self.case[7].player, self.case[7].free, self.case[7].case.background_color = self.case[3].player, self.case[3].free, self.case[3].case.background_color
        self.case[3].player, self.case[3].free, self.case[3].case.background_color = temp

        self.print_case()

        Player.joueur = (Player.joueur + 1) % 2
        self.move = (self.num_board, 1)

    def rotate_left(self, instance):
        print("Gauche")
        temp = [self.case[0].player, self.case[0].free, self.case[0].case.background_color]

        self.case[0].player, self.case[0].free, self.case[0].case.background_color = self.case[6].player, self.case[6].free, self.case[6].case.background_color
        self.case[6].player, self.case[6].free, self.case[6].case.background_color = self.case[8].player, self.case[8].free, self.case[8].case.background_color
        self.case[8].player, self.case[8].free, self.case[8].case.background_color = self.case[2].player, self.case[2].free, self.case[2].case.background_color
        self.case[2].player, self.case[2].free, self.case[2].case.background_color = temp

        temp = [self.case[1].player, self.case[1].free, self.case[1].case.background_color]
        
        self.case[1].player, self.case[1].free, self.case[1].case.background_color = self.case[3].player, self.case[3].free, self.case[3].case.background_color
        self.case[3].player, self.case[3].free, self.case[3].case.background_color = self.case[7].player, self.case[7].free, self.case[7].case.background_color
        self.case[7].player, self.case[7].free, self.case[7].case.background_color = self.case[5].player, self.case[5].free, self.case[5].case.background_color
        self.case[5].player, self.case[5].free, self.case[5].case.background_color = temp

        self.print_case()

        Player.joueur = (Player.joueur + 1) % 2
        self.move = (self.num_board, 0)


    def clear_board(self):
        self.board.disabled = True
        for i in range(3):
            for j in range(3):
                self.case[i*3 + j].case.background_color = [1, 1, 1, 1]
                self.case[i*3 + j].case.disabled = True

    def win(self):
        "Animation when a player win"
        pass


class Case():
    def __init__(self, pos_xy):
        """
        Doc
        """
        self.player = None
        self.free = True
        self.case = Button(pos = pos_xy, size = [50, 50], size_hint = (None, None), background_color = (1, 1, 1, 1), disabled = True)
        self.case.bind(on_press = lambda x: self.play(x))
    
    def play(self, instance):
        """
        Doc
        """
        #If a ball isn't in the boxe
        if self.free:
            self.free = False
            self.player = Player.joueur

            #Player 1
            if self.player:
                self.case.background_color = (1, 0, 0, 1)

            #PLayer 2
            else:
                self.case.background_color = (0, 1, 0, 1)
        #return