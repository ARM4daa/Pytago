from kivy.uix.button import Button
from player import Player
from box import Box

class SubBoard:
    def __init__(self, board_size, pos_x, pos_y, layout, id_board, main_rotate, x_first_box, y_first_box, move, disable_boxes, able_boxes, disable_board, able_board, disable_rotate_button, able_rotate_button, main_button1, main_button2):
        """
        Doc
        """
        self.board_size = board_size
        self.pos_x = pos_x                              #Position x of the board on the layout
        self.pos_y = pos_y                              #Position y of the board on the layout
        self.layout_ajout = layout                      #Layout where elements are added

        self.board = Button(pos=[self.pos_x, self.pos_y], size=[self.board_size, self.board_size], size_hint=[None, None], disabled = True, background_normal = "board_wood.PNG", background_disabled_normal = "board_wood.PNG")
        self.board.bind(on_press = lambda x: self.print_button_rotate(x))           

        self.id_board = id_board                        #Id of the board object
        self.handler_rotate = main_rotate               #Rotate function for bitboard
        self.button1 = main_button1                     #First rotation button (left)
        self.button2 = main_button2                     #Second rotation button (right)
        self.move = move                                #Tuple containing the information transmitted to the bitboard  
        self.disable_all_boxes = disable_boxes            #Function associate to any buttons making turn
        self.able_all_boxes = able_boxes                  #Function associate to rotation
        self.disable_all_boards= disable_board          #Function associate to any buttons making turn
        self.able_all_boards = able_board               #Function associate to rotation
        self.disable_rotate_button = disable_rotate_button
        self.able_rotate_button = able_rotate_button
        
        #Create all the boxes's board
        self.box = []
        for i in range(3):            
            for j in range(3):    
                self.box.append(Box([x_first_box + j*75, y_first_box - i*75], self.disable_all_boxes, self.able_all_boards, self.id_board, i*3 + j, move))
        

        #Print board then boxe
        layout.add_widget(self.board)
        self.print_box()


    def print_box(self):
        """ Displays the status of the 9 boxes on the board """
        for i in range(3):            
            for j in range(3):    
                self.layout_ajout.remove_widget(self.box[i*3 + j].box)        
                self.layout_ajout.add_widget(self.box[i*3+ j].box)


    def disable_board(self):
        """ Disable the board """
        self.board.disabled = True

    def able_board(self):
        """ Able the board """
        self.board.disabled = False


    def disable_boxes(self):
        """ Disable 9 boxes of the board """
        for i in range(3):
            for j in range(3):
                self.box[i*3 + j].box.disabled = True
    
    def able_boxes(self):
        """ Able 9 boxes of the board """
        for i in range(3):
            for j in range(3):
                if self.box[i*3 + j].free: 
                    self.box[i*3 + j].box.disabled = False


    def print_button_rotate(self, btn):
        """
        Print the button to rotate a board
        """
        if self.button1 is not None:
            self.layout_ajout.remove_widget(self.button1)
            self.layout_ajout.remove_widget(self.button2)

        self.button1 = Button(text="Gauche", size_hint=(None, None), size=(50, 50))
        self.button2 = Button(text="Droite", size_hint=(None, None), size=(50, 50))

        if self.id_board == 0:
            self.button1.pos = (self.pos_x - 50, self.pos_y + 200)
            self.button2.pos = (self.pos_x, self.pos_y + 250)
        elif self.id_board == 1:
            self.button1.pos = (self.pos_x + self.board_size - 50, self.pos_y + 250)
            self.button2.pos = (self.pos_x + self.board_size, self.pos_y + 200)
        elif self.id_board == 2:
            self.button1.pos = (self.pos_x - 50, self.pos_y)
            self.button2.pos = (self.pos_x, self.pos_y -50)
        else:
            self.button1.pos = (self.pos_x + self.board_size - 50, self.pos_y - 50)
            self.button2.pos = (self.pos_x + self.board_size, self.pos_y)

        self.able_rotate_button()

        self.button1.bind(on_press = lambda x: self.rotate_left(x))
        self.button2.bind(on_press = lambda x: self.rotate_right(x))

        self.layout_ajout.add_widget(self.button1)
        self.layout_ajout.add_widget(self.button2)
    

    def rotate_left(self, instance):
        """
        Doc
        """
        #Permutation of the values of the corners of the board 
        temp = [self.box[0].free, self.box[0].box.background_normal,self.box[0].box.background_disabled_normal]

        self.box[0].free, self.box[0].box.background_normal,self.box[0].box.background_disabled_normal = self.box[2].free, self.box[2].box.background_normal,self.box[2].box.background_disabled_normal
        self.box[2].free, self.box[2].box.background_normal,self.box[2].box.background_disabled_normal = self.box[8].free, self.box[8].box.background_normal,self.box[8].box.background_disabled_normal
        self.box[8].free, self.box[8].box.background_normal,self.box[8].box.background_disabled_normal = self.box[6].free, self.box[6].box.background_normal,self.box[6].box.background_disabled_normal
        self.box[6].free, self.box[6].box.background_normal,self.box[6].box.background_disabled_normal = temp

        #Permutation of the values of the sides of the board 
        temp = [self.box[1].free, self.box[1].box.background_normal,self.box[1].box.background_disabled_normal]
        
        self.box[1].free, self.box[1].box.background_normal,self.box[1].box.background_disabled_normal = self.box[5].free, self.box[5].box.background_normal,self.box[5].box.background_disabled_normal
        self.box[5].free, self.box[5].box.background_normal,self.box[5].box.background_disabled_normal = self.box[7].free, self.box[7].box.background_normal,self.box[7].box.background_disabled_normal
        self.box[7].free, self.box[7].box.background_normal,self.box[7].box.background_disabled_normal = self.box[3].free, self.box[3].box.background_normal,self.box[3].box.background_disabled_normal
        self.box[3].free, self.box[3].box.background_normal,self.box[3].box.background_disabled_normal = temp

        #Displays the updated board  
        self.print_box()

        #Used to turn management
        Player.player = (Player.player + 1) % 2                 #Move to the oser player
        self.move = (self.id_board, 1)                          #Modify value for the bitboard
        self.disable_all_boards()                               #Deactivates the boards
        self.able_all_boxes()                                   #Activates the squares 
        self.disable_rotate_button()

    def rotate_right(self, instance):
        """
        Doc
        """
        #Permutation of the values of the corners of the board 
        temp = [self.box[0].free, self.box[0].box.background_normal,self.box[0].box.background_disabled_normal]

        self.box[0].free, self.box[0].box.background_normal,self.box[0].box.background_disabled_normal = self.box[6].free, self.box[6].box.background_normal,self.box[6].box.background_disabled_normal
        self.box[6].free, self.box[6].box.background_normal,self.box[6].box.background_disabled_normal = self.box[8].free, self.box[8].box.background_normal,self.box[8].box.background_disabled_normal
        self.box[8].free, self.box[8].box.background_normal,self.box[8].box.background_disabled_normal = self.box[2].free, self.box[2].box.background_normal,self.box[2].box.background_disabled_normal
        self.box[2].free, self.box[2].box.background_normal,self.box[2].box.background_disabled_normal = temp

        #Permutation of the values of the sides of the board
        temp = [self.box[1].free, self.box[1].box.background_normal,self.box[1].box.background_disabled_normal]
        
        self.box[1].free, self.box[1].box.background_normal,self.box[1].box.background_disabled_normal = self.box[3].free, self.box[3].box.background_normal,self.box[3].box.background_disabled_normal
        self.box[3].free, self.box[3].box.background_normal,self.box[3].box.background_disabled_normal = self.box[7].free, self.box[7].box.background_normal,self.box[7].box.background_disabled_normal
        self.box[7].free, self.box[7].box.background_normal,self.box[7].box.background_disabled_normal = self.box[5].free, self.box[5].box.background_normal,self.box[5].box.background_disabled_normal
        self.box[5].free, self.box[5].box.background_normal,self.box[5].box.background_disabled_normal = temp

        #Displays the updated board 
        self.print_box()

        #Used to turn management
        Player.player = (Player.player + 1) % 2                 #Move to the oser player
        self.move = (self.id_board, 0)                          #Modify value for the bitboard
        self.disable_all_boards()                               #Deactivates the boards
        self.able_all_boxes()                                   #Activates the squares 
        self.disable_rotate_button()

    def clear_board(self):
        """ Clear the board """
        for i in range(3):
            for j in range(3):
                self.box[i*3 + j].disabled = True
                self.box[i*3 + j].free = True
                self.box[i*3 + j].box.background_normal = "contour2.PNG"
                self.box[i*3 + j].box.background_disabled_normal = "contour2.PNG"