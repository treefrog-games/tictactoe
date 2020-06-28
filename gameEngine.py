from kivy.uix.gridlayout import GridLayout
from customWidget import *
'''
Игровой движок

'''
class GameEngine:
    '''
    Главный класс с логикой противника и реализацией правил игры

    '''
    def __init__(self, dimension, screen):
        self.screen = screen        
        self.state = True
        self.dimension = dimension
        self.move_count = 0
        self.field = GridLayout(cols=dimension)
        for i in range(dimension * dimension):
            row_pos = dimension - (i // dimension) - 1
            column_pos = dimension - (i % dimension) - 1
            self.field.add_widget(Cell(self, i, row_pos, column_pos))

    def get_optimal_cell_after(self, cell):
        my_row = cell.row_pos
        my_column = cell.column_pos
        result = None
        has_enemy_in_line = False
        potential_position = None
        for i in range(self.dimension):
            current_cell = self.get_cell(i, my_column)
            if current_cell.is_enemy:
                has_enemy_in_line = True
            elif not current_cell.is_my:
                potential_position = i
        if potential_position is not None and not has_enemy_in_line:
            result = self.get_cell(potential_position, my_column)
            print('row potential', result.row_pos)
        else:
            for i in range(self.dimension):
                current_cell = self.get_cell(my_row, i)
                if current_cell.is_enemy:
                    has_enemy_in_line = True
                elif not current_cell.is_my:
                    potential_position = i
            if potential_position is not None and not has_enemy_in_line:
                result = self.get_cell(potential_position, my_column)
                print('column potential', result.column_pos)
        return result

    def get_cell(self, x, y):
        revers_array = self.field.children[::-1]
        index = x * (self.dimension - 1) + y + x
        return revers_array[index]

    def stop_game(self):
        self.state = 1
    
    def enemy_move(self, my_cell):
        '''
            Действия противника
        '''
        potential_move = self.get_optimal_cell_after(my_cell)
        if potential_move is None:
            for cell in self.field.children:
                if cell.text == '':
                    potential_move = cell
                    break

        potential_move.text = 'o'
        potential_move.is_enemy = True
        self.move_count += 1
        self.check_state()

    def my_move(self, cell):
        self.move_count += 1
        if self.check_state():
            self.enemy_move(cell)

    def check_state(self):
        '''
        Проверка текущего состояния игры

        '''
        result = self.state

        # Проход по строкам
        for row in range(self.dimension):
            my_count = 0
            enemy_count = 0
            for column in range(self.dimension):
                if self.get_cell(row, column).is_my:
                    my_count += 1
                if self.get_cell(row, column).is_enemy:
                    enemy_count += 1 
            if my_count == self.dimension:
                self.win()
                result = False
            if enemy_count == self.dimension:
                self.lose()
                result = False

        # Проход по столбцам
        for column in range(self.dimension):
            my_count = 0
            enemy_count = 0
            for row in range(self.dimension):
                if self.get_cell(row, column).is_my:
                    my_count += 1
                if self.get_cell(row, column).is_enemy:
                    enemy_count += 1 
            if my_count == self.dimension:
                self.win()
                result = False
            if enemy_count == self.dimension:
                self.lose()
                result = False
            
        # Проход по главная диагональ
        my_count = 0
        enemy_count = 0
        for i in range(self.dimension):            
            if self.get_cell(i, i).is_my:
                my_count += 1
            if self.get_cell(i, i).is_enemy:
                enemy_count += 1 
            if my_count == self.dimension:
                self.win()
                result = False
            if enemy_count == self.dimension:
                self.lose()
                result = False

        # Проход по побочной диагональ
        my_count = 0
        enemy_count = 0
        for row in range(self.dimension):
            if self.get_cell(row, self.dimension - row - 1).is_my:
                my_count += 1
            if self.get_cell(row, self.dimension - row - 1).is_enemy:
                enemy_count += 1 
            if my_count == self.dimension:
                self.win()
                result = False
            if enemy_count == self.dimension:
                self.lose()
                result = False
        
        # Ничья 
        if self.move_count >= 9:
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
        self.move_count = 0
        restart = RestartButton(self, text=_text)
        self.screen.add_widget(restart)
    
    def restar_game(self):
        if not self.state:
            for cell in self.field.children:
                cell.is_my, cell.is_enemy, cell.text = False, False, ''
            self.state = True
