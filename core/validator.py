class SudokuValidator:
    @staticmethod
    def check_cell(board, row, col, value):
        """检查单个格子的值是否合法"""
        # 查行
        for j in range(9):
            if j != col and board[row][j] == value:
                return False
                
        # 检查列
        for i in range(9):
            if i != row and board[i][col] == value:
                return False
                
        # 检查3x3方格
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and board[i][j] == value:
                    return False
                    
        return True

    @staticmethod
    def check_win(board):
        """检查是否完成游戏"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False
        return True 