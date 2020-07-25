import os
import unittest
import collections
import random
import hashlib


from minescrubber_core import boarder


TEST_SLOTS = collections.namedtuple(
    'TEST_SLOTS',
    [
        'tl',  # top_left
        'tm',  # top_mid
        'tr',  # top_right
        'ml',  # mid_left
        'mm',  # mid_mid
        'mr',  # mid_right
        'bl',  # bottom_left
        'bm',  # bottom_mid
        'br',  # bottom_right
    ]
)


def get_test_slots(width, height):
    import math
    min_x = 0
    min_y = 0
    mid_x = math.ceil(width / 2)
    mid_y = math.ceil(height / 2)
    max_x = width - 1
    max_y = height - 1

    return TEST_SLOTS(
        tl=(min_x, min_y),
        tm=(mid_x, min_y),
        tr=(max_x, min_y),
        ml=(min_x, mid_y),
        mm=(mid_x, mid_y),
        mr=(max_x, mid_y),
        bl=(min_x, max_y),
        bm=(mid_x, max_y),
        br=(max_x, max_y)
    )


def _shift(slot, x=0, y=0):
    return (slot[0] + x, slot[1] + y)


def move(slot, op):
    if op == 'u':
        return _shift(slot, y=-1)
    elif op == 'd':
        return _shift(slot, y=1)
    elif op == 'l':
        return _shift(slot, x=-1)
    elif op == 'r':
        return _shift(slot, x=1)
    elif op == 'ul':
        return _shift(slot, x=-1, y=-1)
    elif op == 'ur':
        return _shift(slot, x=1, y=-1)
    elif op == 'dl':
        return _shift(slot, x=-1, y=1)
    elif op == 'dr':
        return _shift(slot, x=1, y=1)


class TestBoard(unittest.TestCase):
    def setUp(self):
        random.seed(50)
        self.width = random.randint(5, 16)
        self.height = random.randint(5, 16)
        self.nb_mines = int(self.width * self.height * 0.12)
        self.board_hash = (
            '41a2e501c2500ec3a6208e96d2360f66e226c258cf0f19533192b215b89402d6'
        )

        ts = get_test_slots(self.width, self.height)
        self.adjacent_map = {
            ts.tl: [
                move(ts.tl, 'r'),
                move(ts.tl, 'd'),
                move(ts.tl, 'dr'),
            ],
            ts.tm: [
                move(ts.tm, 'l'),
                move(ts.tm, 'r'),
                move(ts.tm, 'dl'),
                move(ts.tm, 'd'),
                move(ts.tm, 'dr'),
            ],
            ts.tr: [
                move(ts.tr, 'l'),
                move(ts.tr, 'dl'),
                move(ts.tr, 'd'),
            ],
            ts.ml: [
                move(ts.ml, 'u'),
                move(ts.ml, 'ur'),
                move(ts.ml, 'r'),
                move(ts.ml, 'd'),
                move(ts.ml, 'dr'),
            ],
            ts.mm: [
                move(ts.mm, 'ul'),
                move(ts.mm, 'u'),
                move(ts.mm, 'ur'),
                move(ts.mm, 'l'),
                move(ts.mm, 'r'),
                move(ts.mm, 'dl'),
                move(ts.mm, 'd'),
                move(ts.mm, 'dr'),
            ],
            ts.mr: [
                move(ts.mr, 'ul'),
                move(ts.mr, 'u'),
                move(ts.mr, 'l'),
                move(ts.mr, 'dl'),
                move(ts.mr, 'd'),
            ],
            ts.bl: [
                move(ts.bl, 'u'),
                move(ts.bl, 'ur'),
                move(ts.bl, 'r'),
            ],
            ts.bm: [
                move(ts.bm, 'ul'),
                move(ts.bm, 'u'),
                move(ts.bm, 'ur'),
                move(ts.bm, 'l'),
                move(ts.bm, 'r'),
            ],
            ts.br: [
                move(ts.br, 'ul'),
                move(ts.br, 'u'),
                move(ts.br, 'l'),
            ],
        }

        self.board = boarder.Board(
            width=self.width,
            height=self.height,
            nb_mines=self.nb_mines
        )

    def test_board(self):
        current_hash = hashlib.sha256(
            str(self.board).encode('utf-8')
        ).hexdigest()

        if 'MINESCRUBBER_DEV' not in os.environ:
            hint_msg = 'The dev env is not set, use export MINESCRUBBER_DEV=1'
            raise ValueError(hint_msg)

        self.assertEqual(current_hash, self.board_hash)

    def test_nb_mines(self):
        nb_mines_on_generatedboard = len(
            [
                cell for cell in self.board.cells
                if cell.has_mine
            ]
        )
        self.assertEqual(
            nb_mines_on_generatedboard,
            self.nb_mines,
        )

    def test_mine_slots(self):
        mine_slots = [
            (cell.x, cell.y)
            for cell in self.board.cells
            if cell.has_mine
        ]
        self.assertListEqual(
            sorted(mine_slots),
            sorted(self.board.mine_slots),
        )

    def test_get_adjacent_slots(self):
        for slot, expected_adjacent in self.adjacent_map.items():
            adjacent = self.board._get_adjacent_slots(slot, self.board.data)
            self.assertEqual(
                sorted(adjacent),
                sorted(expected_adjacent),
            )

    def test_cell_has_mine(self):
        for mine_slot in self.board.mine_slots:
            cell = self.board.get_cell(mine_slot)
            self.assertTrue(cell.has_mine)


if __name__ == "__main__":
    unittest.main()
