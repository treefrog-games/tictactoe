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
        self.set_weight()

    def set_weight(self):
        '''
        Метод разачи весов
        '''
        for cell in self.field.children:
            cell.weight = 0
        for cell in self.field.children:
            cell.weight = 0
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

    def get_cell(self, x, y):
        '''
        Гетер ячейки по координатам
        '''
        result = None
        for cell in self.field.children:
            if cell.row_pos == x and cell.column_pos == y:
                result = cell
        return result
    
    def get_neighbours_cells(self, cell):
        x = cell.row_pos
        y = cell.column_pos
        list_neighbors = set()
        for hei in map(self.get_cell, range(x-1, x+2, 1), repeat(y)):
            list_neighbors.add(hei)
        for hei in map(self.get_cell, range(x-1, x+2, 1), repeat(y-1)):
            list_neighbors.add(hei)
        for hei in  map(self.get_cell, range(x-1, x+2, 1), repeat(y+1)):
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
        max_weight = 0
        for cell in self.field.children:
            if cell.weight > max_weight:
                max_weight = cell.weight

        for cell in self.field.children:
            if cell.weight == max_weight and not cell.is_my and not cell.is_enemy:
                cell.text = 'o'
                cell.is_enemy = True
                break
        self.move_count += 1
        self.check_state()

    def my_move(self, cell):
        cell.text = 'x'
        self.is_my = True
        self.move_count += 1
        self.set_weight()
        if self.check_state():
            self.enemy_move(cell)

    def check_state(self, deep=3):
        '''
        Проверка текущего состояния игры

        '''
        result = self.state
        my_count = 0
        enemy_count = 0

        # проверка по линиям
        for y in range(self.dimension):
            for cell in map(self.get_cell, range(0, deep, 1), repeat(y)):
                if cell.is_my:
                    my_count += 1
                if cell.is_enemy:
                    enemy_count += 1
                if my_count == self.dimension:
                    self.win()
                    result = False
                if enemy_count == self.dimension:
                    self.lose()
                    result = False
            my_count = 0
            enemy_count = 0

        for x in range(self.dimension):
            for cell in map(self.get_cell, repeat(x), range(0, deep,1)):
                if cell.is_my:
                    my_count += 1
                if cell.is_enemy:
                    enemy_count += 1
                if my_count == self.dimension:
                    self.win()
                    result = False
                if enemy_count == self.dimension:
                    self.lose()
                    result = False
            my_count = 0
            enemy_count = 0

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
