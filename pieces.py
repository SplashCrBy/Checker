'''
Author: Sizhao Li
Date: 2020-11-10 10:16:48
LastEditors: Sizhao Li
LastEditTime: 2020-12-14 14:17:34
Description: Piece class for manipulating relative piece function
'''


class piece(object):
    '''
    piece class

    attrs:
      pos_x: the x axis value of the piece, represents the top left corner of
      the piece
      pos_y: the y axis value of the piece, represents the top left corner of
      the piece
      color: which side the piece belongs to
      dead: whether the piece is checked or not
      king: if the piece is a king piece
      jumpable: if the piece is jumpable or not
    '''

    def __init__(self, pos_x, pos_y, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.dead = False
        self.king = False
        self.jumpable = False

    def valid_pos_x(self, pen_pos, board_size, grid_number):
        '''
        Function -- valid_pos_x
            determine whether the x axis value is valid on board
        Parameter:
          pen_pos - the x axis value of click position
          board_size - the size of the border
          grid_number - how many grid a row the board should have
        return:
          A boolean, true if the x is a valid value, false if not
        '''
        return (self.pos_x < pen_pos and pen_pos < self.pos_x + (board_size /
                                                                 grid_number))

    def valid_pos_y(self, pen_pos, board_size, grid_number):
        '''
        Function -- valid_pos_x
            determine whether the x axis value is valid on board
        Parameter:
          pen_pos - the y axis value of click position
          board_size - the size of the border
          grid_number - how many grid a row the board should have
        return:
          A boolean, true if the y is a valid value, false if not
        '''
        return self.pos_y >= pen_pos and pen_pos >= self.pos_y - (board_size /
                                                                  grid_number)

    def out_board(self, board_size, grid_number, direction):
        '''
        Function -- out_board
            determine whether the piece will be out of board after move
        Parameter:
          board_size - the size of the border
          grid_number - how many grid a row the board should have
          direction - the direction the piece is going to move
        return:
          A boolean, true if the piece will be out of board, false if not
        '''
        if direction == 'up_left':
            return (round(self.pos_x - board_size/grid_number) < round
                    (-board_size/2) or round(self.pos_y +
                                             board_size/grid_number) > round
                    (board_size/2))
        elif direction == 'up_right':
            return (round(self.pos_x + board_size/grid_number) >= round
                    (board_size/2) or round(self.pos_y +
                                            board_size/grid_number) > round
                    (board_size/2))
        elif direction == 'jump_upright':
            return (round(self.pos_x + board_size*2/grid_number) >= round
                    (board_size/2) or round(self.pos_y +
                                            board_size*2/grid_number)
                    > round(board_size/2))
        elif direction == 'jump_upleft':
            return (round(self.pos_x - board_size*2/grid_number) < round
                    (-board_size/2) or round(self.pos_y+board_size*2 /
                                             grid_number) >
                    round(board_size/2))
        if direction == 'down_left':
            return (round(self.pos_x - board_size/grid_number) < round
                    (-board_size/2) or round(self.pos_y -
                                             board_size/grid_number)
                    <= round(-board_size/2))
        elif direction == 'down_right':
            return (round(self.pos_x + board_size/grid_number) >= round
                    (board_size/2) or round(self.pos_y -
                                            board_size/grid_number) <= round
                    (-board_size/2))
        elif direction == 'jump_downright':
            return (round(self.pos_x + board_size*2/grid_number) >= round
                    (board_size/2) or round(self.pos_y-2*board_size /
                                            grid_number) <=
                    round(-board_size/2))
        elif direction == 'jump_downleft':
            return (round(self.pos_x - board_size*2/grid_number) < round
                    (-board_size/2) or round(self.pos_y-2*board_size /
                                             grid_number) <=
                    round(-board_size/2))


class black_piece(piece, object):

    '''
    black_piece class
    subclass of piece

    attrs:
      pos_x: the x axis value of the piece, represents the top left corner of
      the piece
      pos_y: the y axis value of the piece, represents the top left corner of
      the piece
      color: which side the piece belongs to
      dead: whether the piece is checked or not
      king: if the piece is a king piece
      jumpable: if the piece is jumpable or not
    '''

    def king_upgrade(self, board_size, grid_number):
        '''
        Function -- king_upgrade
            determine if the black piece reaches the border
        Parameter:
          pen_pos - the y axis value of click position
          board_size - the size of the border
          grid_number - how many grid a row the board should have
        return:
          A boolean, true if the y is a valid value, false if not
        '''
        if round(self.pos_y) == round(board_size/2):
            self.king = True
            return True

    def move(self, board_size, grid_number, direction, occupied):
        '''
        Function -- move
            determine if the piece execute a valid movement
        Parameter
          board_size - the size of the border
          grid_number - how many grid a row the board should have
          direction - the direction the piece is going to move
          occupied - if the next position of the piece is occupied by
          other piece
        return:
          A boolean, true if the piece moves normally, false if not
        '''
        if occupied:
            return False
        if self.out_board(board_size, grid_number, direction) is False:
            if direction == 'up_left':
                self.pos_x -= board_size/grid_number
                self.pos_y += board_size/grid_number
                return True
            elif direction == 'up_right':
                self.pos_x += board_size/grid_number
                self.pos_y += board_size/grid_number
                return True
            elif direction == 'jump_upright':
                self.pos_x += board_size/grid_number * 2
                self.pos_y += board_size/grid_number * 2
                self.is_jumped = True
                return True
            elif direction == 'jump_upleft':
                self.pos_x -= board_size/grid_number * 2
                self.pos_y += board_size/grid_number * 2
                self.is_jumped = True
                return True
        return False


class red_piece(piece, object):
    '''
    red_piece class
    subclass of piece

    attrs:
      pos_x: the x axis value of the piece, represents the top left corner of
      the piece
      pos_y: the y axis value of the piece, represents the top left corner of
      the piece
      color: which side the piece belongs to
      dead: whether the piece is checked or not
      king: if the piece is a king piece
      jumpable: if the piece is jumpable or not
    '''

    def move(self, board_size, grid_number, direction, occupied):
        '''
        Function -- move
            determine if the piece execute a valid movement
        Parameter
          board_size - the size of the border
          grid_number - how many grid a row the board should have
          direction - the direction the piece is going to move
          occupied - if the next position of the piece is occupied by
          other piece
        return:
          A boolean, true if the piece moves normally, false if not
        '''
        if occupied:
            return False
        if self.out_board(board_size, grid_number, direction) is False:
            if direction == 'down_left':
                self.pos_x -= board_size/grid_number
                self.pos_y -= board_size/grid_number
                return True
            elif direction == 'down_right':
                self.pos_x += board_size/grid_number
                self.pos_y -= board_size/grid_number
                return True
            elif direction == 'jump_downleft':
                self.pos_x -= board_size/grid_number * 2
                self.pos_y -= board_size/grid_number * 2
                self.is_jumped = True
                return True
            elif direction == 'jump_downright':
                self.pos_x += board_size/grid_number * 2
                self.pos_y -= board_size/grid_number * 2
                self.is_jumped = True
                return True
        return False

    def king_upgrade(self, board_size, grid_number):
        '''
        Function -- king_upgrade
            determine if the red piece reaches the border
        Parameter:
          pen_pos - the y axis value of click position
          board_size - the size of the border
          grid_number - how many grid a row the board should have
        return:
          A boolean, true if the y is a valid value, false if not
        '''
        if round(self.pos_y-board_size/grid_number) == round(-board_size/2):
            self.king = True
            return True


class king_piece(black_piece, red_piece, object):
    '''
    king_piece class
    subclass of black_piece and red_piece

    attrs:
      pos_x: the x axis value of the piece, represents the top left corner of
      the piece
      pos_y: the y axis value of the piece, represents the top left corner of
      the piece
      color: which side the piece belongs to
      dead: whether the piece is checked or not
      king: if the piece is a king piece
      jumpable: if the piece is jumpable or not
    '''

    def __init__(self, piece):
        self.pos_x = piece.pos_x
        self.pos_y = piece.pos_y
        self.color = piece.color
        self.dead = piece.dead
        self.king = True
        self.jumpable = piece.jumpable

    def move(self, board_size, grid_number, direction, occupied):
        '''
        Function -- move
            determine if the piece execute a valid movement
        Parameter
          board_size - the size of the border
          grid_number - how many grid a row the board should have
          direction - the direction the piece is going to move
          occupied - if the next position of the piece is occupied by
          other piece
        return:
          A boolean, true if the piece moves normally, false if not
        '''
        if occupied:
            return False
        if self.out_board(board_size, grid_number, direction) is False:
            if direction == 'up_left':
                self.pos_x -= board_size/grid_number
                self.pos_y += board_size/grid_number
                return True
            elif direction == 'up_right':
                self.pos_x += board_size/grid_number
                self.pos_y += board_size/grid_number
                return True
            elif direction == 'jump_upright':
                self.pos_x += board_size/grid_number * 2
                self.pos_y += board_size/grid_number * 2
                self.is_jumped = True
                return True
            elif direction == 'jump_upleft':
                self.pos_x -= board_size/grid_number * 2
                self.pos_y += board_size/grid_number * 2
                self.is_jumped = True
                return True
            elif direction == 'down_left':
                self.pos_x -= board_size/grid_number
                self.pos_y -= board_size/grid_number
                return True
            elif direction == 'down_right':
                self.pos_x += board_size/grid_number
                self.pos_y -= board_size/grid_number
                return True
            elif direction == 'jump_downleft':
                self.pos_x -= board_size/grid_number * 2
                self.pos_y -= board_size/grid_number * 2
                self.is_jumped = True
                return True
            elif direction == 'jump_downright':
                self.pos_x += board_size/grid_number * 2
                self.pos_y -= board_size/grid_number * 2
                self.is_jumped = True
                return True
        return False
