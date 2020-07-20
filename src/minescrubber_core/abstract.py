import abc


class UI(abc.ABC):
    @abc.abstractmethod
    def refresh(self):
        ...

    @abc.abstractmethod
    def game_over(self):
        ...

    @abc.abstractmethod
    def game_solved(self):
        ...

    @abc.abstractmethod
    def run(self):
        ...

    @abc.abstractproperty
    def cell_selected_signal(self):
        ...

    @abc.abstractproperty
    def cell_flagged_signal(self):
        ...

    @abc.abstractproperty
    def new_game_signal(self):
        ...

    @abc.abstractproperty
    def wiring_method_name(self):
        ...


class Controller:
    def run(self, ui_class, pre_args=None, pre_kwargs=None, post_args=None,
            post_kwargs=None):

        from . import boarder, gamer

        pre_args = pre_args or []
        pre_kwargs = pre_kwargs or {}
        self.pre_callback(*pre_args, **pre_kwargs)

        board = boarder.Board()
        ui = ui_class(board=board)
        game = gamer.Game(board=board, ui=ui)

        self._do_wiring(ui, game)
        ui.run()

        post_args = post_args or []
        post_kwargs = post_kwargs or {}
        self.post_callback(*post_args, **post_kwargs)

    @staticmethod
    def _do_wiring(ui, game):
        wiring = {
            ui.cell_selected_signal: game.select,
            ui.cell_flagged_signal: game.flag,
            ui.new_game_signal: game.reset
        }
        for connect_from, connect_to in wiring.items():
            wiring_method = getattr(connect_from, ui.wiring_method_name)
            wiring_method(connect_to)

    @abc.abstractmethod
    def pre_callback(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def post_callback(self, *args, **kwargs):
        ...
