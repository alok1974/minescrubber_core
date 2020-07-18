class Game:
    def __init__(self, board, ui):
        self.board = board
        self.ui = ui
        self._is_game_over = False

    def select(self, slot):
        if self._is_game_over:
            return

        cell = self.board.get_cell(slot)
        if cell.has_mine:
            self._is_game_over = True
            self.board.stepped_on_mine(cell)
            self.ui.game_over(self.board)
            return

        self.board.sweep(cell)
        self.ui.refresh(self.board)

    def reset(self, args):
        width, height, nb_mines = args
        self.board.init_board(width=width, height=height, nb_mines=nb_mines)
        self._is_game_over = False
        self.ui.refresh(self.board)
