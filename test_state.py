'''
Author: Sizhao Li
Date: 2020-12-14 13:57:30
LastEditors: Sizhao Li
LastEditTime: 2020-12-14 14:14:25
Description: file content
'''
from pieces import piece, black_piece, red_piece, king_piece
from State import state

RED = ('#b22222')
BLACK = ('#000000')

black_piece1 = black_piece(320, 320, BLACK)
red_piece1 = red_piece(320, 320, RED)
stateA = state(RED)
stateA.score_change(red_piece1)
stateA.score_change(black_piece1)


def test_state():
    assert(stateA.red == 1)
    assert(stateA.black == 1)
