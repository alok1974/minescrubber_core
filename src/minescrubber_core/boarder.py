import os
import random


from . import cellar


class Board:
    MIN_CELLS = 5
    MAX_CELLS = 16

    def __init__(self, width=9, height=9, nb_mines=10):
        self._validate_args(
            width=width,
            height=height,
            nb_mines=nb_mines
        )

        self._dev_env = os.environ.get('MINESCRUBBER_DEV')
        self.init_board(width=width, height=height, nb_mines=nb_mines)

    def init_board(self, width, height, nb_mines):
        self._width = width
        self._height = height

        self._min_x = 0
        self._max_x = self._width - 1

        self._min_y = 0
        self._max_y = self._height - 1

        self._nb_slots = self._width * self._height
        self._nb_mines = nb_mines

        self._mine_slots = None
        self._data = self._generate_board_data()

        self._swept_slots = []
        self._flagged_slots = []
        self._last_swept = []

    @property
    def minimum_nb_cells(self):
        return self._minimum_nb_cells

    @property
    def maximum_nb_cells(self):
        return self._maximum_nb_cells

    @property
    def state(self):
        return self.display(show_all=False)

    @property
    def nb_mines(self):
        return self._nb_mines

    @property
    def nb_flagged(self):
        return len(self._flagged_slots)

    @property
    def max_flagged(self):
        return self.nb_mines == self.nb_flagged

    @property
    def data(self):
        return self._data

    @property
    def mine_slots(self):
        return sorted(self._mine_slots)

    @property
    def flagged_slots(self):
        return sorted(self._flagged_slots)

    @property
    def covered_slots(self):
        return sorted([cell.slot for cell in self.cells if cell.is_covered])

    @property
    def cells(self):
        return self.data.values()

    @property
    def slots(self):
        return self.data.keys()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def min_x(self):
        return self._min_x

    @property
    def min_y(self):
        return self._min_y

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    @property
    def nb_slots(self):
        return self._nb_slots

    @property
    def last_swept(self):
        return self._last_swept

    def get_cell(self, slot):
        return self.data[slot]

    def get_slot(self, cell):
        return cell.slot

    def display(self, show_all=True):
        dash = '-' * ((self.width * 6) - 1)
        line = f' {dash} '
        out = []
        for y in range(self.height):
            out.append(line)
            line_data = []
            for x in range(self.width):
                slot = (x, y)
                cell = self.get_cell(slot)
                if cell.has_mine:
                    val = ' * '
                elif cell.hint == 0:
                    val = '   '
                else:
                    val = f' {cell.hint} '
                if show_all:
                    line_data.append(val)
                else:
                    if cell.is_uncovered:
                        line_data.append(val)
                    else:
                        line_data.append(' \u2588 ')

            line_str = ' | '.join(line_data)
            out.append(f'| {line_str} |')
        out.append(line)
        return '\n'.join(out)

    def flag(self, cell):
        if cell.is_uncovered:
            return

        if cell.is_flagged:
            cell.unflag()
            self._flagged_slots.remove(cell.slot)
        else:
            if self.max_flagged:
                return

            cell.flag()
            self._flagged_slots.append(cell.slot)

    def uncover_all(self):
        for cell in self.cells:
            cell.uncover()

    def sweep(self, cell, is_first_call=True):
        if is_first_call:
            self._last_swept = []

        self._sweep_cell(cell)
        adj_cells = self._get_adjacent_cells(cell)
        if not any([adj_cell.has_mine for adj_cell in adj_cells]):
            map(self._sweep_cell, adj_cells)
            for adj_cell in adj_cells:
                if adj_cell.slot not in self._swept_slots:
                    self.sweep(adj_cell, is_first_call=False)

    def _sweep_cell(self, cell):
        if not cell.is_flagged:
            cell.uncover()
            if cell.slot not in self._last_swept:
                self._last_swept.append(cell.slot)

        if cell.slot not in self._swept_slots:
            self._swept_slots.append(cell.slot)

    def _generate_board_data(self):
        board_data = self._create_empty_board_data()
        board_data = self._setup_mines(board_data=board_data)
        board_data = self._add_hints(board_data=board_data)
        return board_data

    def _create_empty_board_data(self):
        data = {}
        for x in range(self._width):
            for y in range(self._height):
                data[(x, y)] = cellar.Cell(x=x, y=y)
        return data

    def _setup_mines(self, board_data):
        # Use random seed to generate exactly the same
        # random mines for test/dev/debug at runtime
        if self._dev_env:
            random.seed(50)

        random_slots = [slot for slot in board_data.keys()]  # Copy of keys
        random.shuffle(random_slots)
        self._mine_slots = random_slots[:self._nb_mines]

        for slot in self._mine_slots:
            cell = board_data[slot]
            cell.set_mine()

        return board_data

    def _add_hints(self, board_data):
        hints = {}
        for slot, cell in board_data.items():
            if cell.has_mine:
                continue

            hint = 0
            adjacent_slots = self._get_adjacent_slots(slot, board_data)
            for adjacent_slot in adjacent_slots:
                cell = board_data[adjacent_slot]
                if cell.has_mine:
                    hint += 1

            hints[slot] = hint

        for slot, hint in hints.items():
            cell = board_data[slot]
            cell.hint = hint

        return board_data

    def _get_adjacent_cells(self, cell):
        adjacent_slots = self._get_adjacent_slots(cell.slot, self.data)
        return list(map(self.get_cell, adjacent_slots))

    def _get_adjacent_slots(self, slot, board_data):
        slots = board_data.keys()
        if slot not in slots:
            error_msg = f'The slot<{slot}> is not on board: {slots}'
            raise ValueError(error_msg)

        x, y = slot
        adjacent = []
        for x_slot in [x - 1, x, x + 1]:
            for y_slot in [y - 1, y, y + 1]:
                neighbour = (x_slot, y_slot)
                if self._not_a_valid_neighbour(neighbour, slot):
                    continue
                adjacent.append(neighbour)

        return adjacent

    def _not_a_valid_neighbour(self, neighbour, slot):
        x, y = neighbour
        return any([
            neighbour == slot,
            x < self.min_x,
            x > self.max_x,
            y < self.min_y,
            y > self.max_y,
        ])

    def __repr__(self):
        header = f'[{self._width} x {self._height}] ({self._nb_mines})'
        body = self.display()
        footer = ''
        return f'{header}\n{body}\n{footer}'

    def _validate_args(self, width, height, nb_mines):
        allowed_width = self.MIN_CELLS < width < self.MAX_CELLS
        allowed_height = self.MIN_CELLS < height < self.MAX_CELLS
        if not allowed_width or not allowed_height:
            error_msg = (
                f'Both `width={width}` and '
                f'`height={height}`` should be between '
                f'{self.MIN_CELLS} and {self.MAX_CELLS}'
            )
            raise RuntimeError(error_msg)

        nb_tiles = width * height
        if nb_mines > nb_tiles:
            error_msg = (
                f'No. of mines={nb_mines} cannot be '
                f'greater no. of tiles {nb_tiles}'
                f'(width={width} x height={height})'
            )
            raise RuntimeError(error_msg)
