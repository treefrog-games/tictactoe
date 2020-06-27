from kivy.uix.gridlayout import GridLayout
from customWidget import *
'''
Игровой движок

'''
class GameEngine:
    '''
    Главный класс с логикой противника и реализацией правил игры

    '''
    def __init__(self, demention, screen):
        self.screen = screen        
        self.state = True
        self.demention = demention
        self.field = GridLayout(cols=demention)
        for i in range(demention * demention):
            self.field.add_widget(Cell(self, i))

    def get_cell(self, x, y):
        revers_array = self.field.children[::-1].copy()
        index = x * (self.demention - 1) + y + x
        return revers_array[index]

    def stop_game(self):
        self.state = 1
    
    def enemy_move(self):
        '''
            Действия противника
        '''
        for cell in self.field.children:
            if cell.text == '':
                cell.text = 'o'
                cell.is_enemy = True
                break
        self.check_state()

    def my_move(self):
        if self.check_state():
            self.enemy_move()

    def check_state(self):
        '''
        Проверка текущего состояния игры

        '''
        result = self.state

        # Проход по строкам
        for row in range(self.demention):
            my_count = 0
            enemy_count = 0
            for column in range(self.demention):
                if self.get_cell(row, column).is_my:
                    my_count += 1
                if self.get_cell(row, column).is_enemy:
                    enemy_count += 1 
            if my_count == self.demention:
                self.win()
                result = False
            if enemy_count == self.demention:
                self.lose()
                result = False

        # Проход по столбцам
        for column in range(self.demention):
            my_count = 0
            enemy_count = 0
            for row in range(self.demention):
                if self.get_cell(row, column).is_my:
                    my_count += 1
                if self.get_cell(row, column).is_enemy:
                    enemy_count += 1 
            if my_count == self.demention:
                self.win()
                result = False
            if enemy_count == self.demention:
                self.lose()
                result = False
            
        # Проход по главная диагональ
        my_count = 0
        enemy_count = 0
        for i in range(self.demention):            
            if self.get_cell(i, i).is_my:
                my_count += 1
            if self.get_cell(i, i).is_enemy:
                enemy_count += 1 
            if my_count == self.demention:
                self.win()
                result = False
            if enemy_count == self.demention:
                self.lose()
                result = False

        # Проход по побочной диагональ
        my_count = 0
        enemy_count = 0
        for row in range(self.demention):
            if self.get_cell(row, self.demention - row - 1).is_my:
                my_count += 1
            if self.get_cell(row, self.demention - row - 1).is_enemy:
                enemy_count += 1 
            if my_count == self.demention:
                self.win()
                result = False
            if enemy_count == self.demention:
                self.lose()
                result = False
        
        # Ничья 
        my_count = 0
        for cell in self.field.children:
            if cell.is_my or cell.is_enemy:
                my_count += 1
            if my_count >= 9:
                self.standoff()
                result =False

        self.state = result
        return result

    def lose(self):
        self.end_game('Game over :-(')

    def win(self):
        self.end_game("Win!!!")
    
    def standoff(self):
        self.end_game('Standoff')
        
    
    def end_game(self, _text):
        restart = RestartButton(self, text=_text)
        self.screen.add_widget(restart)
    
    def restar_game(self):
        if not self.state:
            for cell in self.field.children:
                cell.is_my, cell.is_enemy, cell.text = False, False, ''
            self.state = True
