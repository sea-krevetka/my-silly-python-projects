class BattleFigure:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def get_attack_area(self, rows, cols, walls):
        pass


class Polearm(BattleFigure):
    def get_attack_area(self, rows, cols, walls):
        attacks = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 1 <= nx <= rows and 1 <= ny <= cols:
                if (nx, ny) not in walls:
                    attacks.append((nx, ny))
        
        return attacks


class Sekire(BattleFigure):
    def get_attack_area(self, rows, cols, walls):
        attacks = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 1 <= nx <= rows and 1 <= ny <= cols:
                if (nx, ny) not in walls:
                    attacks.append((nx, ny))
        
        return attacks


class Chilivary(BattleFigure):
    def get_attack_area(self, rows, cols, walls):
        attacks = []
        
        for i in range(self.x - 1, 0, -1):
            if (i, self.y) in walls:
                break
            attacks.append((i, self.y))
        
        for i in range(self.x + 1, rows + 1):
            if (i, self.y) in walls:
                break
            attacks.append((i, self.y))
        
        for j in range(self.y - 1, 0, -1):
            if (self.x, j) in walls:
                reak
            attacks.append((self.x, j))
        
        for j in range(self.y + 1, cols + 1):
            if (self.x, j) in walls:
                break
            attacks.append((self.x, j))
        
        return attacks


class GameSolver:
    def __init__(self, rows, cols, walls, enemies):
        self.rows = rows
        self.cols = cols
        self.walls = walls
        self.enemies = set(enemies)
        self.original_enemies = set(enemies)
        self.solution = []
    
    def create_figure(self, figure_type, x, y):
        if figure_type == 'Polearm':
            return Polearm('Polearm', x, y)
        elif figure_type == 'Sekire':
            return Sekire('Sekire', x, y)
        elif figure_type == 'Chilivary':
            return Chilivary('Chilivary', x, y)
    
    def get_valid_positions(self, current_enemies):
        positions = []
        for x in range(1, self.rows + 1):
            for y in range(1, self.cols + 1):
                if (x, y) not in self.walls and (x, y) not in current_enemies:
                    positions.append((x, y))
        return positions
    
    def simulate_attack(self, figure, current_enemies):
        attacks = set(figure.get_attack_area(self.rows, self.cols, self.walls))
        remaining = current_enemies - attacks
        return remaining
    
    def solve(self, figure_types, figure_index=0, current_enemies=None, placed_figures=None):
        if current_enemies is None:
            current_enemies = self.enemies.copy()
        if placed_figures is None:
            placed_figures = []
        
        if not current_enemies:
            self.solution = placed_figures.copy()
            return True
        
        if figure_index >= len(figure_types):
            return False
        
        figure_type = figure_types[figure_index]
        valid_positions = self.get_valid_positions(current_enemies)
        
        for x, y in valid_positions:
            figure = self.create_figure(figure_type, x, y)
            remaining_enemies = self.simulate_attack(figure, current_enemies)
            
            if len(remaining_enemies) == len(current_enemies):
                continue
            
            placed_figures.append((figure_type, x, y))
            
            if self.solve(figure_types, figure_index + 1, remaining_enemies, placed_figures):
                return True
            
            placed_figures.pop()
        
        return False
    
    def solve_all_combinations(self):
        from itertools import permutations
        
        figure_types = ['Sekire', 'Sekire', 'Polearm', 'Polearm', 'Chilivary']
        unique_permutations = set(permutations(figure_types))
        
        print(f"Перебираем {len(unique_permutations)} уникальных перестановок фигур...")
        
        solutions = []
        for i, perm in enumerate(unique_permutations, 1):
            self.enemies = self.original_enemies.copy()
            self.solution = []
            if self.solve(list(perm)):
                solutions.append((list(perm), self.solution.copy()))
                print(f"Найдено решение для перестановки {i}")
        
        return solutions
    
    def print_solution(self, solution):
        if not solution:
            print("Решение не найдено")
            return
        
        print("\n" + "="*60)
        print("НАЙДЕНО РЕШЕНИЕ:")
        print("="*60)
        
        enemies = self.original_enemies.copy()
        
        for i, (fig_type, x, y) in enumerate(solution, 1):
            figure = self.create_figure(fig_type, x, y)
            attacks = figure.get_attack_area(self.rows, self.cols, self.walls)
            killed = enemies.intersection(attacks)
            enemies = enemies - set(attacks)
            
            print(f"\n{i}. {fig_type} на позиции ({x},{y})")
            print(f"   Атакует: {sorted(attacks)}")
            print(f"   Убивает: {sorted(killed)}")
            print(f"   Осталось врагов: {len(enemies)}")
        
        self.print_map(solution)
    
    def print_map(self, solution):
        display = [[' . ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        for x, y in self.walls:
            if 1 <= x <= self.rows and 1 <= y <= self.cols:
                display[x-1][y-1] = ' X '
        
        for x, y in self.original_enemies:
            if 1 <= x <= self.rows and 1 <= y <= self.cols:
                if display[x-1][y-1] == ' . ':
                    display[x-1][y-1] = ' E '
        
        for fig_type, x, y in solution:
            if 1 <= x <= self.rows and 1 <= y <= self.cols:
                if fig_type == 'Polearm':
                    display[x-1][y-1] = ' P '
                elif fig_type == 'Sekire':
                    display[x-1][y-1] = ' S '
                elif fig_type == 'Chilivary':
                    display[x-1][y-1] = ' C '
        
        print("\nФинальная карта:")
        print("    " + "   ".join(str(i+1) for i in range(self.cols)))
        for i in range(self.rows):
            row_str = f"{i+1:2} " + "".join(display[i])
            print(row_str)


if __name__ == "__main__":
    rows, cols = 6, 5
    
    walls = {(3,1), (4,2), (3,3), (4,4), (3,5)}
    
    enemies = {
        (4,1), (5,2), (4,3), (5,4), (4,5), (5,5), (5,1), (5,3),
        (6,1), (6,2), (6,3), (6,4), (6,5)
    }
    
    print(f"Поле: {rows}x{cols}")
    print(f"Стены: {sorted(walls)}")
    print(f"Враги: {sorted(enemies)}")
    print(f"Всего врагов: {len(enemies)}")
    
    solver = GameSolver(rows, cols, walls, enemies)
    
    solutions = solver.solve_all_combinations()
    
    if solutions:
        print(f"\nНайдено {len(solutions)} решений!")
        solver.print_solution(solutions[0][1])
        
        if len(solutions) > 1:
            print("\n" + "="*60)
            print("ДРУГИЕ РЕШЕНИЯ:")
            for i, (perm, sol) in enumerate(solutions[1:], 2):
                print(f"\nРешение {i}:")
                for fig_type, x, y in sol:
                    print(f"  {fig_type} ({x},{y})")
    else:
        print("\nРешений не найдено!")
