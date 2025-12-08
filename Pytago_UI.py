from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

#.size() -> Tuple (largeur, hauteur)

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        layout_plateau = FloatLayout()
        layout_menu = FloatLayout()

        reset_game = Button(text="Recommencer une partie", pos =[30, 500], size_hint = [.5, .1])
        mode_solo = Button(text="Jouer en solo", pos = [30, 425], size_hint = [.5, .1])
        mode_duo = Button(text="Jouer à 2", pos = [30, 350], size_hint = [.5, .1])
        regles = Button(text="Règles", pos = [30, 30], size_hint = [.5, .1])
        plateau1 = Button(pos = [300, 275],size = [225, 225], size_hint=(None, None), background_color = (1, 0, 0, 1))
        plateau2 = Button(pos = [525, 275],size = [225, 225], size_hint=(None, None), background_color = (0, 0, 1, 1))
        plateau3 = Button(pos = [300, 50],size = [225, 225], size_hint=(None, None), background_color = (0, 1, 0, 1))
        plateau4 = Button(pos = [525, 50],size = [225, 225], size_hint=(None, None), background_color = (1, 1, 0, 1))

        layout_menu.add_widget(reset_game)
        layout_menu.add_widget(mode_solo)
        layout_menu.add_widget(mode_duo)
        layout_menu.add_widget(regles)
        layout_plateau.add_widget(plateau1)
        layout_plateau.add_widget(plateau2)
        layout_plateau.add_widget(plateau3)
        layout_plateau.add_widget(plateau4)

        self.add_widget(layout_menu)
        self.add_widget(layout_plateau)        

class MyApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()