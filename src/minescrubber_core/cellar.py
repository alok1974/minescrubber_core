import enum


@enum.unique
class CELL_DATA(enum.Enum):
    state = 'state'
    value = 'value'


@enum.unique
class CELL_STATE(enum.Enum):
    covered = 0
    uncovered = 1
    flagged = 2


MINE_INT = -1


class Cell:
    __slots__ = ('_x', '_y', '_state', '_value')

    def __init__(self, x, y, state=CELL_STATE.covered, value=0):
        self._x = x
        self._y = y
        self._state = state
        self._value = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def hint(self):
        if self.has_mine:
            return None
        return self._value

    @property
    def state(self):
        return self._state

    @hint.setter
    def hint(self, val):
        if self.has_mine:
            error_msg = (
                'The cell has mine, cannot add hint!'
            )
            raise ValueError(error_msg)
        self._value = val

    @property
    def slot(self):
        return (self._x, self._y)

    @property
    def is_uncovered(self):
        return self._state == CELL_STATE.uncovered

    @property
    def is_covered(self):
        return self._state == CELL_STATE.covered

    @property
    def is_flagged(self):
        return self._state == CELL_STATE.flagged

    @property
    def is_unflagged(self):
        return self._state != CELL_STATE.flagged

    @property
    def has_mine(self):
        return self._value == MINE_INT

    def set_mine(self):
        self._value = MINE_INT

    def flag(self):
        self._state = CELL_STATE.flagged

    def unflag(self):
        self._state = CELL_STATE.covered

    def cover(self):
        self._state = CELL_STATE.covered

    def uncover(self):
        self._state = CELL_STATE.uncovered

    def __repr__(self):
        return f'Cell<{self.x}, {self.y}>'
