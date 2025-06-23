import numpy as np
from collections import defaultdict

class TreasureHunter:
    def __init__(self):
        self.size = 5
        self.grid = np.full((self.size, self.size), '?')  # неизвестные лунки
        self.safe = set()  # безопасные лунки
        self.bombs = set()  # лунки с бочками
        self.possible_bombs = defaultdict(int)  # возможные бомбы
        self.dug = set()  # раскопанные лунки
        self.last_dug = None
        
    def print_grid(self):
        """Выводит текущее состояние поля"""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) in self.dug:
                    row.append(self.grid[i, j])
                elif (i, j) in self.bombs:
                    row.append('X')
                else:
                    row.append('?')
            print(' '.join(row))
        print()
    
    def update_safe(self, pos):
        """Добавляет безопасные лунки после раскопки пустой"""
        i, j = pos
        # горизонталь и вертикаль
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                if (ni, nj) not in self.dug and (ni, nj) not in self.bombs:
                    self.safe.add((ni, nj))
    
    def update_bombs_from_vegetable(self, pos):
        """Обновляет возможные бомбы после раскопки овоща"""
        i, j = pos
        adjacent = []
        # горизонталь и вертикаль
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                if (ni, nj) not in self.dug and (ni, nj) not in self.bombs:
                    adjacent.append((ni, nj))
        
        # В соседних должно быть ровно 1 бомба
        if len(adjacent) > 0:
            for cell in adjacent:
                self.possible_bombs[cell] += 1
    
    def update_bombs_from_iron(self, pos):
        """Обновляет возможные бомбы после раскопки железа"""
        i, j = pos
        adjacent = []
        # горизонталь и вертикаль
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                if (ni, nj) not in self.dug and (ni, nj) not in self.bombs:
                    adjacent.append((ni, nj))
        
        # В соседних должно быть 2 бомбы
        if len(adjacent) >= 2:
            for cell in adjacent:
                self.possible_bombs[cell] += 2
    
    def process_dug_cell(self, pos, item):
        """Обрабатывает раскопанную лунку"""
        i, j = pos
        self.grid[i, j] = item
        self.dug.add(pos)
        self.last_dug = pos
        
        if item == ' ':
            self.update_safe(pos)
        elif item in ['C', 'P']:  # C - капуста, P - картошка
            self.update_bombs_from_vegetable(pos)
        elif item == 'I':  # I - железо
            self.update_bombs_from_iron(pos)
        elif item == 'X':
            print("БОМБА! Игра окончена.")
            return False
        
        # Проверяем возможные бомбы с высокой вероятностью
        for cell, count in list(self.possible_bombs.items()):
            adjacent = self.get_adjacent_hv(cell)
            needed = self.calculate_needed_bombs(cell)
            
            if count >= 3 or (needed > 0 and count >= needed):
                self.bombs.add(cell)
                if cell in self.safe:
                    self.safe.remove(cell)
                del self.possible_bombs[cell]
        
        return True
    
    def get_adjacent_hv(self, pos):
        """Возвращает соседние клетки по горизонтали и вертикали"""
        i, j = pos
        adjacent = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                adjacent.append((ni, nj))
        return adjacent
    
    def calculate_needed_bombs(self, pos):
        """Вычисляет сколько бомб должно быть вокруг клетки"""
        i, j = pos
        for (di, dj), item in np.ndenumerate(self.grid):
            if (di, dj) in self.dug:
                if item in ['C', 'P']:
                    adjacent = self.get_adjacent_hv((di, dj))
                    if pos in adjacent:
                        unknown_adjacent = [c for c in adjacent if c not in self.dug and c not in self.bombs]
                        if len(unknown_adjacent) == 1:
                            return 1  # должна быть 1 бомба
                elif item == 'I':
                    adjacent = self.get_adjacent_hv((di, dj))
                    if pos in adjacent:
                        unknown_adjacent = [c for c in adjacent if c not in self.dug and c not in self.bombs]
                        if len(unknown_adjacent) <= 2:
                            return 2  # должно быть 2 бомбы
        return 0
    
    def suggest_next_dig(self):
        """Предлагает следующую лунку для раскопок"""
        # 1. Проверяем безопасные лунки
        if self.safe:
            return self.safe.pop()
        
        # 2. Проверяем лунки с наименьшей вероятностью бомбы
        safe_candidates = []
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in self.dug and (i, j) not in self.bombs:
                    safe_candidates.append((i, j))
        
        if not safe_candidates:
            return None
        
        # Убираем возможные бомбы
        safe_candidates = [c for c in safe_candidates if c not in self.possible_bombs]
        
        if safe_candidates:
            return safe_candidates[0]
        
        # Если все потенциально опасны, выбираем с наименьшим весом
        min_weight = min(self.possible_bombs.values())
        candidates = [k for k, v in self.possible_bombs.items() if v == min_weight]
        return candidates[0] if candidates else None

def main():
    print("Добро пожаловать в игру 'Поиск сокровищ'!")
    print("Вводите что нашли в лунке (пробел - пусто, C - капуста, P - картошка, I - железо, X - бомба):")
    
    hunter = TreasureHunter()
    
    while True:
        hunter.print_grid()
        next_dig = hunter.suggest_next_dig()
        
        if next_dig is None:
            print("Не могу определить следующую лунку. Возможно, сундук уже найден или игра окончена.")
            break
        
        print(f"Следующая лунка для раскопок: {next_dig}")
        item = input("Что нашли в этой лунке? (введите символ): ").upper()
        
        if item == 'T':
            print("Поздравляем! Вы нашли сундук!")
            break
        
        if not hunter.process_dug_cell(next_dig, item):
            break

if __name__ == "__main__":
    main()
