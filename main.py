from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen


class GameEngine:
    state = 0

    def __init__(self, *arg):
        self.map = [[0  for i in range(arg[0])] for j in range(arg[0])]
        self.field = GridLayout(cols=arg[0])
        for i in range(arg[0]*arg[0]):
            self.field.add_widget(Cell(self, i))

    def stop_game(self):
        self.state = 1
    
    def enemy_move(self):
        for cell in self.field.children:
            if cell.text == '':
                cell.text = 'o'
                break


class Cell(Button):
    def __init__(self, game, mid, **kwargs):
        self.width = 10
        self.height = 10
        self.cellid = mid
        self.font_size = '100dp'
        self.text = ''
        self.game = game
        super().__init__(**kwargs)
    
    def on_press(self):
        self.text = 'x'
        print('press ' + str(self.cellid))
        self.game.enemy_move()


class MainApp(App):
    def build(self):
        game = GameEngine(3)
        screen = Screen()
        screen.add_widget(game.field)
        return screen
    

MainApp().run()
