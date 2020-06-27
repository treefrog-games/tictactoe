from kivy.app import App
from customWidget import *
from gameEngine import GameEngine
'''
    Главный модуль игры крестики-нолики.
    @author ms_subbotin
    
'''

class MainApp(App):
    def build(self):
        screen = Screen()
        # start_screen = StartScreen()
        # screen.add_widget(start_screen)        
        game = GameEngine(3, screen)
        screen.add_widget(game.field)
        
        return screen
    

MainApp().run()
