'''
Author: Sizhao Li
Date: 2020-11-11 14:38:23
LastEditors: Sizhao Li
LastEditTime: 2020-12-14 11:23:35
Description: record the state of the game
'''

red = ('#b22222')
black = ('#000000')

max_score = 12


class state(object):
    '''
    state class
    record the state of the game

    attrs:
      black: how many scores does human player get
      red: how many scores does computer get
      turn: whose turn in this round

    '''

    def __init__(self, color):
        self.black = 0
        self.red = 0
        self.turn = color

    def score_change(self, piece):
        '''
        Function -- score_change
          update the score when needed
        Parameter:
          piece - which piece makes the update
        return:
          none
        '''
        if piece.color == red:
            self.red += 1
        else:
            self.black += 1

    def state_change(self, color, direction):
        '''
        Function -- state_change
          change the turn of next round
        Parameter:
          color - determine whose turn the next round should be
          direction - update score if capture happened
        return:
          none
        '''
        if color == red:
            self.turn = black
        elif color == black:
            self.turn = red
        if (direction == 'jump_upright' or direction == 'jump_upleft' or
                direction == 'jump_downleft' or direction == 'jump_downright'):
            if color == black:
                self.black += 1
            elif color == red:
                self.red += 1

    def win(self):
        '''
        Function -- win
          determine if there is a winner
        Parameter:
          none
        return:
          none
        '''
        return self.black == max_score or self.red == max_score
