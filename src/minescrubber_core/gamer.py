from . import boarder


class GameController:
    def __init__(self, ui):
        self.board = boarder.Board()
        self.ui = ui
        self.ui.init_board(board=self.board)
        self._do_wiring()

        self._is_game_over = False
        self._is_game_solved = False

    def run(self):
        self.ui.run()

    def select(self, slot):
        if self._is_game_over or self._is_game_solved:
            return

        cell = self.board.get_cell(slot)
        if self._is_over(cell):
            self._game_over(cell)
            return

        self.board.sweep(cell)

        if self._is_solved():
            self._game_solved()
            return

        self.ui.refresh(self.board, init_image=False)

    def flag(self, slot):
        if self._is_game_over or self._is_game_solved:
            return

        cell = self.board.get_cell(slot)
        self.board.flag(cell)

        if self._is_solved():
            self._game_solved()
            return

        self.ui.refresh(self.board)

    def reset(self, args):
        width, height, nb_mines = args
        self.board.init_board(width=width, height=height, nb_mines=nb_mines)
        self._is_game_over = False
        self._is_game_solved = False
        self.ui.refresh(self.board)

    def _do_wiring(self):
        wiring = [
            (self.ui.cell_selected_signal, self.select),
            (self.ui.cell_flagged_signal, self.flag),
            (self.ui.new_game_signal, self.reset),
        ]
        for connect_from, connect_to in wiring:
            wiring_method = getattr(connect_from, self.ui.wiring_method_name)
            wiring_method(connect_to)

    def _is_solved(self):
        return self.board.mine_slots == sorted(
            self.board.covered_slots +
            self.board.flagged_slots
        )

    def _game_solved(self):
        self._is_game_solved = True
        self.ui.game_solved(self.board)

    def _is_over(self, cell):
        return cell.has_mine

    def _game_over(self, cell):
        self._is_game_over = True
        self.board.uncover_all()
        self.ui.game_over(self.board)
