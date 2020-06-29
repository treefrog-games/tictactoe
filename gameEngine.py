from kivy.uix.gridlayout import GridLayout
from customWidget import *
from itertools import repeat
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
            row_pos = (i // dimension)
            column_pos = i % dimension
            print('create: ', i, row_pos, column_pos)
            self.field.add_widget(Cell(self, i, row_pos, column_pos))
        

    def set_weight(self):
        for cell in self.field.children:
            if not cell.is_my and not cell.is_enemy:
                neighbors = self.get_neighbours_cells(cell)
                for neighbor in neighbors:
                    if not neighbor.is_my and not neighbor.is_enemy:
                        cell.weight += 1
                    if neighbor.is_my:
                        cell.weight += 2
                    if neighbor.is_enemy:
                        cell.weight += 3
            print

    def get_optimal_cell_after(self, cell):
        my_row = cell.row_pos
        my_column = cell.column_pos
        print('my: ', my_row, my_column)
        result = None
        row_result = None
        column_result = None
        has_enemy_in_line = False
        me_in_row = 0
        me_in_column = 0
        me_in_main_diag = 0
        me_in_reverse_diag = 0
        potential_position = None
        for i in range(self.dimension):
            current_cell = self.get_cell(i, my_column)
            if current_cell.is_enemy:
                has_enemy_in_line = True
            elif current_cell.is_my:
                me_in_row += 1
            else:
                potential_position = i
        if (potential_position is not None) and (not has_enemy_in_line):
            row_result = self.get_cell(potential_position, my_column)
            print('row potential', row_result.row_pos, row_result.column_pos)

        has_enemy_in_line = False
        potential_col_position = None
        for i in range(self.dimension):
            current_cell = self.get_cell(my_row, i)
            if current_cell.is_enemy:
                has_enemy_in_line = True
            elif current_cell.is_my:
                me_in_column += 1
            else:
                potential_col_position = i
        if potential_col_position is not None and not has_enemy_in_line:
            column_result = self.get_cell(my_row, potential_col_position)
            print('column potential', column_result.row_pos, column_result.column_pos)

        has_enemy_in_line = False
        potential_main_diag_position = None
        for i in range(self.dimension):
            current_cell = self.get_cell(i, i)
            if current_cell.is_enemy:
                has_enemy_in_line = True
            elif current_cell.is_my:
                me_in_main_diag += 1
            else:
                potential_main_diag_position = i
        print ('me_in_main_diag', me_in_main_diag)
        if (potential_main_diag_position is not None) and (not has_enemy_in_line) and me_in_main_diag > 1:
            result = self.get_cell(potential_main_diag_position, potential_main_diag_position)
            print('main potential', result.row_pos, result.column_pos)

        has_enemy_in_line = False
        potential_reverse_diag_position = None
        for i in range(self.dimension):
            current_cell = self.get_cell(i, self.dimension - i -1)
            if current_cell.is_enemy:
                has_enemy_in_line = True
            elif current_cell.is_my:
                me_in_reverse_diag += 1
            else:
                potential_reverse_diag_position = i
        print('me_in_reverse_diag', me_in_main_diag)
        if (potential_reverse_diag_position is not None) and (not has_enemy_in_line) and me_in_reverse_diag > 1:
            result = self.get_cell(potential_reverse_diag_position, self.dimension - potential_reverse_diag_position - 1)
            print('reverse potential', result.row_pos, result.column_pos)

        if result is None:
            if me_in_row >= my_column:
                result = row_result
            else:
                result = column_result
        return result

    def get_cell(self, x, y):
        result = None
        for cell in self.field.children:
            if cell.row_pos == x and cell.column_pos == y:
                result = cell
        return result
    
    def get_neighbours_cells(self, cell):
        x = cell.row_pos
        y = cell.column_pos
        list_neighbors = set()
        for hei in map(self.get_cell, range(x-1, x+1, 1), repeat(y)):
            list_neighbors.add(hei)
        for hei in map(self.get_cell, range(x-1, x+1, 1), repeat(y-1)):
            list_neighbors.add(hei)
        for hei in  map(self.get_cell, range(x-1, x+1, 1), repeat(y+1)):
            list_neighbors.add(hei)
        list_neighbors.remove(self.get_cell(x, y))
        list_neighbors.discard(None)
        return list_neighbors

    def stop_game(self):
        self.state = 1
    
    def enemy_move(self, my_cell):
        '''
            Действия противника
        '''
        min_weight = 10000
        for cell in self.field.children:
            if cell.weight < min_weight:
                min_weight = cell.weight

        for cell in self.field.children:
            if cell.weight == min_weight:
                cell.text = 'o'
                cell.is_enemy = True
                break
        # potential_move = self.get_optimal_cell_after(my_cell)
        # if potential_move is None:
        #     for cell in self.field.children:
        #         if cell.text == '':
        #             potential_move = cell
        #             break

        # potential_move.text = 'o'
        # potential_move.is_enemy = True
        self.move_count += 1
        self.check_state()

    def my_move(self, cell):
        self.move_count += 1
        self.set_weight()
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


if __name__ == "__main__":
    game = GameEngine(3, screen=None)
    game.set_weight()
    print(game)
