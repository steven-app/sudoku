import random

class SudokuGenerator:
    def __init__(self):
        self.reset_board()
        self.solutions_count = 0
        # 按照指定比例调整难度系数
        self.difficulty_ratios = {
            'easy': 0.60,      # 60% cells filled
            'medium': 0.50,    # 50% cells filled
            'hard': 0.40,      # 40% cells filled
            'expert': 0.30     # 30% cells filled
        }

    def reset_board(self):
        """重置数独板"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def generate_solution(self):
        """生成完整的数独解决方案"""
        self.reset_board()
        
        # 随机填充第一行
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        self.board[0] = numbers
        
        # 解决剩余的数独
        if self._solve_recursive(self.board):
            return [row[:] for row in self.board]
        return None

    def count_solutions(self, board):
        """计算数独谜题的解的数量"""
        self.solutions_count = 0  # 重置计数器
        board_copy = [row[:] for row in board]  # 创建副本以免修改原始数据
        self._count_solutions_recursive(board_copy)
        return self.solutions_count

    def _count_solutions_recursive(self, board):
        """递归计算解的数量"""
        if self.solutions_count > 1:  # 如果已经找到多个解，提前返回
            return
            
        empty = self.find_empty(board)
        if not empty:
            self.solutions_count += 1
            return
            
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(num, (row, col), board):
                board[row][col] = num
                self._count_solutions_recursive(board)
                board[row][col] = 0

    def _solve_recursive(self, board):
        """递归解数独"""
        empty = self.find_empty(board)
        if not empty:
            return True
            
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # 随机尝试数字，增加随机性
        
        for num in numbers:
            if self.is_valid(num, (row, col), board):
                board[row][col] = num
                
                if self._solve_recursive(board):
                    return True
                    
                board[row][col] = 0
        
        return False

    def find_empty(self, board):
        """找到一个空格子"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos, board):
        """检查在指定位置放置数字是否合法"""
        # 检查行
        for x in range(9):
            if board[pos[0]][x] == num and pos[1] != x:
                return False
                
        # 检查列
        for x in range(9):
            if board[x][pos[1]] == num and pos[0] != x:
                return False
        
        # 检查3x3方格
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        
        return True

    def generate_puzzle(self, difficulty):
        """Generate a puzzle with the specified difficulty"""
        # First generate a complete solution
        solution = self.generate_solution()
        if not solution:
            return None, None
            
        # Get the ratio based on difficulty
        remain_ratio = self.difficulty_ratios.get(difficulty, 0.5)
        
        # Generate and return the puzzle
        puzzle = self.generate_puzzle_from_solution(solution, remain_ratio)
        return puzzle, solution

    def generate_puzzle_from_solution(self, solution, remain_ratio):
        """Generate puzzle from solution with the specified ratio of remaining numbers"""
        while True:
            puzzle = [row[:] for row in solution]
            cells_to_remove = int(81 * (1 - remain_ratio))
            
            # Get all non-empty positions
            positions = [(i, j) for i in range(9) for j in range(9)]
            random.shuffle(positions)
            
            # Try removing numbers one by one
            removed = 0
            for i, j in positions:
                temp = puzzle[i][j]
                puzzle[i][j] = 0
                
                # Copy current puzzle for testing
                test_puzzle = [row[:] for row in puzzle]
                
                # Check number of solutions
                if self.count_solutions(test_puzzle) == 1:
                    removed += 1
                    if removed == cells_to_remove:
                        return puzzle
                else:
                    # If not unique solution, restore the number
                    puzzle[i][j] = temp
            
            # If can't reach target removal count, start over
            if removed < cells_to_remove:
                continue
            
            return puzzle 