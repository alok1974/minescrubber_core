import abc


class UI(abc.ABC):
    @abc.abstractmethod
    def init_board(self, board):
        ...

    @abc.abstractmethod
    def refresh(self, board):
        ...

    @abc.abstractmethod
    def game_over(self, board):
        ...

    @abc.abstractmethod
    def game_solved(self, board):
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
    def run(self, ui_class, pre_args=None, pre_kwargs=None, ui_args=None,
            ui_kwargs=None, post_args=None, post_kwargs=None):

        from . import gamer

        # Call pre callback
        pre_args = pre_args or []
        pre_kwargs = pre_kwargs or {}
        self.pre_callback(*pre_args, **pre_kwargs)

        # Create and run game
        ui_args = post_args or []
        ui_kwargs = post_kwargs or {}
        ui = ui_class(*ui_args, **ui_kwargs)
        gc = gamer.GameController(ui=ui)
        gc.run()

        # Call post callback
        post_args = post_args or []
        post_kwargs = post_kwargs or {}
        self.post_callback(*post_args, **post_kwargs)

    @abc.abstractmethod
    def pre_callback(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def post_callback(self, *args, **kwargs):
        ...
