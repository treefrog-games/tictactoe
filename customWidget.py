from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
'''
Пользовотельские виджеты

'''

class Cell(Button):
    def __init__(self, game, mid, **kwargs):
        self.width = 10
        self.height = 10
        self.cell_id = mid
        self.font_size = '100dp'
        self.text = ''
        self.game = game
        self.is_my = False
        self.is_enemy = False
        super().__init__(**kwargs)
    
    def on_press(self):
        if not self.is_my and not self.is_enemy and self.game.state:
            self.is_my = True
            self.text = 'x'
            print('press ' + str(self.cell_id))
            self.game.my_move()

class RestartButton(Button):

    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(**kwargs)

    def on_press(self):
        print('restart')
        self.parent.remove_widget(self.parent.children[0])
        self.game.restar_game()

class StartButton(Button):
    pass

class PlusButton(Button):
    pass

class MinusButton(Button):
    pass

class StartScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dimention = 3
        self.cols = 1

        self.start_button = StartButton(text="Start?")
        self.plus_button = PlusButton(text="+")
        self.minus_button =  MinusButton(text="-")
        self.dimention_label = Label(text=str(self.dimention))

        self.add_widget(self.plus_button)
        self.add_widget(self.minus_button)
        self.add_widget(self.dimention_label)
        self.add_widget(self.start_button)