'''
Author: Sizhao Li
Date: 2020-11-10 10:14:35
LastEditTime: 2020-12-14 14:18:59
LastEditors: Sizhao Li
Description: the main function of the checker game
'''
import turtle
import random
import time
from State import state
from pieces import piece, black_piece, red_piece, king_piece

GREY = ('#585858')
WHITE = ('#ffffff')
RED = ('#b22222')
BLACK = ('#000000')

red_only = ['down_left', 'down_right']
black_only = ['up_left', 'up_right', 'jump_upleft', 'jump_upright']
all_direction = ['up_left', 'up_right', 'down_left', 'down_right',
                 'jump_upleft', 'jump_upright', 'jump_downleft',
                 'jump_downright']
jump_only = ['jump_upleft', 'jump_upright', 'jump_downleft', 'jump_downright']
jump_red_only = ['jump_downleft', 'jump_downright']

pen = turtle.Turtle()
state_pen = turtle.Turtle()
circle_pen = turtle.Turtle()
win_pen = turtle.Turtle()
board_state = state(BLACK)

default_size = 8
edge_win = 11
red_border = 3
black_border = 4
screen_border = 480
right_angle = 90
piece_list = []
red_list = []
black_list = []
selected_piece = None

turtle.setup(640, 640)
turtle.screensize(480, 480)
width = turtle.screensize()[0]
height = turtle.screensize()[1]

grid_size = width / default_size

pen.hideturtle()
state_pen.hideturtle()
circle_pen.hideturtle()
win_pen.hideturtle()
circle_pen.penup()
pen.penup()


def main():
    pen.setpos(-width/2, height/2)
    turtle.title("checker")
    draw_board()
    draw_state(board_state.black, board_state.red, board_state.turn)
    turtle.onscreenclick(move_piece)
    turtle.done()


def draw_board(board_size=default_size):
    '''
    Function -- draw_board
      this function draws the initial board and pieces
    Parameter:
      board_size - the size of each grid on the board
    return:
      none
    '''
    turtle.tracer(False)
    grey_first = True

    # draw from the top left corner
    for row in range(board_size):
        for column in range(board_size):
            circle_pen.goto(pen.pos()[0], pen.pos()[1])
            if column % 2 == 0:
                if grey_first:
                    rectangle(pen, GREY)
                    if row < red_border:
                        circle(circle_pen, RED)
                    elif row > black_border:
                        circle(circle_pen, BLACK)
                else:
                    rectangle(pen, WHITE)
            else:
                if not grey_first:
                    rectangle(pen, WHITE)
                else:
                    rectangle(pen, GREY)
                    if row < red_border:
                        circle(circle_pen, RED)
                    elif row > black_border:
                        circle(circle_pen, BLACK)
            # change the color of each grid
            grey_first = not grey_first
            pen.forward(width/board_size)
        # go to next row
        pen.setx(-width/2)
        pen.rt(right_angle)
        pen.fd(width/board_size)
        pen.lt(right_angle)
        # change the color of the first grid
        grey_first = not grey_first
    turtle.tracer(True)


def rectangle(pen, color):
    '''
    Function -- rectangle
      this function draws one single grid
    Parameter:
      pen - the turtle object used to draw
      color - what color should the pen use
    return:
      none
    '''
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()
    for step in range(4):
        # minus 2 to offset the width of pen
        pen.fd(grid_size)
        pen.rt(right_angle)
    pen.end_fill()
    pen.penup()


def circle(pen, color):
    '''
    Function -- circle
      this function draws a single piece
    Parameter:
      pen - the turtle object used to draw the piece
      color - the color that pen should use
    return:
      none
    '''

    # add piece to their own list
    if color == RED:
        red_list.append(red_piece(pen.pos()[0], pen.pos()[1],  color))
    else:
        black_list.append(black_piece(pen.pos()[0], pen.pos()[1], color))
    pen.forward(grid_size/2)
    pen.seth(right_angle*2)
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(grid_size/2)
    pen.end_fill()
    pen.penup()
    pen.seth(0)
    pen.bk(grid_size/2)


def update_piece():
    '''
    Function -- update_piece
      this function redraws the pieces in order to reflect the game status
    Parameter:
      none
    return:
      none
    '''
    # skip the drawing animation
    turtle.tracer(False)
    circle_pen.clear()
    # redraw every piece based on their position
    for piece in piece_list:
        if (piece.dead is False):
            circle_pen.goto(piece.pos_x, piece.pos_y)
            circle_pen.forward(grid_size/2)
            circle_pen.seth(right_angle*2)
            circle_pen.pendown()
            circle_pen.fillcolor(piece.color)
            circle_pen.begin_fill()
            circle_pen.circle(grid_size/2)
            circle_pen.end_fill()
            # draw a white circle to tell player it is a king piece
            if(piece.king is True):
                circle_pen.pencolor('white')
                circle_pen.circle(grid_size/4)
                circle_pen.pencolor('black')
            circle_pen.penup()
            circle_pen.seth(0)
            circle_pen.bk(grid_size/2)
    turtle.tracer(True)


def move_piece(pen_x, pen_y):
    '''
    Function -- move_piece
      this function is the core function of this game, mainly controls the
      moving behavior of each piece
    Parameter:
      pen_x - the x axis value of click position
      pen_y - the y axis value of click position
    return:
      none
    '''
    red_win = False

    # use a global variable to control the behavior of the function
    global selected_piece

    moved = False

    # build a list of every pieces
    if piece_list == []:
        piece_list.extend(black_list)
        piece_list.extend(red_list)

    # the second click of the user, move the selected piece to valid place
    if selected_piece is not None and board_state.turn == selected_piece.color:
        direction = which_direction(
            selected_piece, pen_x, pen_y, selected_piece.jumpable)
        occupied = board_occupied(selected_piece, direction)
        moved = selected_piece.move(
            width, default_size, direction, occupied)
        jumpable = selected_piece.jumpable
        # not moved because user clicks invalid place on the board, so just
        # wait for the next valid click
        if moved is False:
            board_state.turn = selected_piece.color
            print("Invalid move!")
        else:
            # upgrade to king piece if the regular piece reach the border
            if(selected_piece.king_upgrade(width, default_size)):
                piece_list.remove(selected_piece)
                piece_list.append(king_piece(selected_piece))
                piece_list[len(piece_list)-1].jumpable = False
                selected_piece.jumpable = False
            # kill the piece which is checked by the opponents
            piece_clear(selected_piece, direction)
            # update the jumpable variable of each piece in case of continuous
            # jump
            jump_determine()
            # if jump is over, the computer takes the next move
            if (jumpable != selected_piece.jumpable or not selected_piece.
                    jumpable):
                board_state.state_change(selected_piece.color, direction)
                update_piece()
                draw_state(board_state.black,
                           board_state.red, board_state.turn)
                if board_state.win():
                    draw_state(board_state.black,
                               board_state.red, board_state.turn)
                    draw_win("black")
                    turtle.exitonclick()
                ai_move()

                # edge case, determine if the last piece is movable
                for item in piece_list:
                    if (board_state.red == edge_win and item.color == BLACK and
                            not item.dead):
                        red_win = True
                        if isinstance(item, king_piece):
                            for direction in all_direction:
                                if (not item.out_board(width, default_size,
                                                       direction) and not
                                    board_occupied(item,
                                                   direction)):
                                    red_win = False
                                    break
                        else:
                            for direction in black_only:
                                if (not item.out_board(width, default_size,
                                                       direction) and not
                                    board_occupied(item,
                                                   direction)):
                                    red_win = False
                                    break
                if red_win:
                    draw_win("red")
                    draw_state(board_state.black,
                               board_state.red, board_state.turn)
                    turtle.exitonclick()
            else:
                board_state.score_change(selected_piece)
        selected_piece = None

    draw_state(board_state.black, board_state.red, board_state.turn)
    board_state.jump_list = []

    # select the piece user clicked, usually the first click in a round
    for piece in piece_list:
        if piece.jumpable:
            board_state.jump_list.append(piece)
    for piece in piece_list:
        if (piece.valid_pos_x(pen_x, width, default_size) and piece.valid_pos_y
            (pen_y, screen_border, default_size) and not piece.dead and piece.
                color == BLACK):
            if (board_state.jump_list != [] and board_state.jump_list[0].color
                    == board_state.turn):
                if piece in board_state.jump_list:
                    selected_piece = piece
                else:
                    continue
            else:
                selected_piece = piece
    update_piece()


def ai_move():
    '''
    Function -- ai_move
      this function performs a simple computer player
    Parameter:
      none
    return:
      none
    '''
    # slow down the movement so player can understand what's happened
    time.sleep(1)
    red_piece = None
    red_direction = None
    possible_direction = []
    lost = True
    occupied = True

    # if all piece are dead, human player declares the win
    for piece in piece_list:
        if not piece.dead and piece.color == RED:
            lost = False
            break
    if lost:
        return

    # check if there is any jumpable piece first
    for piece in piece_list:
        if piece.jumpable and piece.color == RED and not piece.dead:
            # king piece and red piece performs different movement so
            # deal with them seperately
            if isinstance(piece, king_piece):
                for direction in jump_only:
                    if (not board_occupied(piece, direction) and not piece.
                            out_board(width, default_size, direction)):
                        occupied = False
                        possible_direction.append(direction)
            else:
                for direction in jump_red_only:
                    if (not board_occupied(piece, direction) and not piece.
                            out_board(width, default_size, direction)):
                        occupied = False
                        possible_direction.append(direction)
            red_piece = piece
            # if there are multiple jump possibilities, randomly choose one
            red_direction = possible_direction[random.randint(
                0, len(possible_direction)-1)]
            break
    # if there is no jumpable piece, pick a piece from the list
    for piece in piece_list:
        if red_piece is not None:
            break
        if (isinstance(piece, king_piece) and not piece.dead and piece.color ==
                RED):
            for direction in all_direction:
                occupied = board_occupied(piece, direction)
                if (not occupied and not piece.out_board(width,
                                                         default_size,
                                                         direction)):
                    red_direction = direction
                    red_piece = piece
                    break
        if (not isinstance(piece, king_piece) and not piece.dead and piece.
                color == RED):
            for direction in red_only:
                occupied = board_occupied(piece, direction)
                if (not occupied and not piece.out_board(width,
                                                         default_size,
                                                         direction)):
                    red_direction = direction
                    red_piece = piece
                    break
    if red_piece is None:
        draw_win("black")
        return
    moved = red_piece.move(width, default_size, red_direction, occupied)
    jumpable = red_piece.jumpable
    # no move means human player wins
    if moved is False:
        board_state.turn = red_piece.color
        draw_win("black")
        return
    else:
        # upgrade the red piece to king piece when it reaches the border
        if(red_piece.king_upgrade(width, default_size) and not isinstance
           (red_piece, king_piece)):
            piece_list.remove(red_piece)
            piece_list.append(king_piece(red_piece))
            piece_list[len(piece_list)-1].jumpable = False
            red_piece.jumpable = False
        piece_clear(red_piece, red_direction)
        jump_determine()
        if jumpable != red_piece.jumpable or not red_piece.jumpable:
            board_state.state_change(red_piece.color, red_direction)
        else:
            board_state.score_change(red_piece)
            update_piece()
            ai_move()
    update_piece()
    if board_state.win():
        draw_win("red")
        draw_state(board_state.black, board_state.red, board_state.turn)
        turtle.exitonclick()
        return


def which_direction(piece, pos_x, pos_y, jumpable):
    '''
    Function -- which_direction
      this function determines what's the meaning of player's click position
    Parameter:
      piece - the piece user clicked at the first time in a round
      pos_x - the x axis value of click position
      pos_y - the y axis value of click position
      jumpable - if the piece is jumpable or not
    return:
      the direction that represents the click area
    '''
    if not jumpable:
        if(pos_x < piece.pos_x and pos_x > piece.pos_x - grid_size and pos_y >
           piece.pos_y and pos_y < piece.pos_y + grid_size):
            return 'up_left'
        elif(pos_x > piece.pos_x + grid_size and pos_x < piece.pos_x +
             2*grid_size and pos_y > piece.pos_y and pos_y < piece.pos_y +
             grid_size):
            return 'up_right'
        elif(pos_x < piece.pos_x and pos_x > piece.pos_x - grid_size and pos_y
             < piece.pos_y and pos_y < piece.pos_y - grid_size):
            return 'down_left'
        elif(pos_x > piece.pos_x + grid_size and pos_x < piece.pos_x +
             2*grid_size and pos_y < piece.pos_y and pos_y < piece.pos_y
             - grid_size):
            return 'down_right'
    else:
        if(pos_x < piece.pos_x - grid_size and pos_x > piece.pos_x - grid_size
           * 2 and pos_y > piece.pos_y + grid_size and pos_y < piece.pos_y +
           grid_size * 2):
            return 'jump_upleft'
        elif(pos_x > piece.pos_x + grid_size * 2 and pos_x < piece.pos_x + 3 *
             grid_size and pos_y > piece.pos_y + grid_size and pos_y < piece.
             pos_y +
             2*grid_size):
            return 'jump_upright'
        elif(pos_x < piece.pos_x - grid_size and pos_x > piece.pos_x - 2 *
             grid_size and pos_y < piece.pos_y - grid_size and pos_y < piece.
             pos_y -
             2*grid_size):
            return 'jump_downleft'
        elif(pos_x > piece.pos_x + grid_size*2 and pos_x < piece.pos_x +
             3*grid_size and pos_y < piece.pos_y - grid_size and pos_y < piece.
             pos_y
             - 2 * grid_size):
            return 'jump_downright'


def board_occupied(piece, direction):
    '''
    Function -- board_occupied
      this function determines whether possible movable grid is occupied by
      other piece
    Parameter:
      piece - the piece user wants to move
      direction - where they want to move the piece to
    return:
      a boolean, true if the area is being occupied by other piece,
      false if not
    '''
    no_jump = True
    for item in piece_list:
        if item.dead is False:
            if direction == 'up_left':
                if (round(item.pos_x) == round(piece.pos_x-grid_size) and round
                        (item.pos_y) == round(piece.pos_y+grid_size)):
                    return True
            elif direction == 'up_right':
                if (round(item.pos_x) == round(piece.pos_x+grid_size) and round
                        (item.pos_y) == round(piece.pos_y+grid_size)):
                    return True
            elif direction == 'jump_upleft':
                for surrounding in piece_list:
                    if not surrounding.dead:
                        if (round(surrounding.pos_x) == round(piece.
                                                              pos_x-grid_size)
                            and round
                            (surrounding.
                             pos_y) == round
                            (piece.pos_y+grid_size) and surrounding.color !=
                            piece.
                                color):
                            no_jump = False
                            break
                if no_jump:
                    return True

                elif (round(item.pos_x) == round(piece.pos_x-2*grid_size) and
                      round(item.pos_y) == round(piece.pos_y+2*grid_size)):

                    return True
            elif direction == 'jump_upright':
                for surrounding in piece_list:
                    if not surrounding.dead:
                        if (round(surrounding.pos_x) == round(piece.pos_x
                                                              + grid_size) and
                            round(surrounding.
                                  pos_y) == round
                            (piece.pos_y
                             + grid_size) and
                            surrounding.color
                                != piece.color):
                            no_jump = False
                            break
                if no_jump:
                    return True
                elif (round(item.pos_x) == round(piece.pos_x+2*grid_size) and
                      round(item.pos_y) == round(piece.pos_y+2*grid_size)):
                    return True
            elif direction == 'down_left':
                if (round(item.pos_x) == round(piece.pos_x-grid_size) and round
                        (item.pos_y) == round(piece.pos_y-grid_size)):
                    return True

            elif direction == 'down_right':
                if (round(item.pos_x) == round(piece.pos_x+grid_size) and round
                        (item.pos_y) == round(piece.pos_y-grid_size)):
                    return True
            elif direction == 'jump_downleft':
                for surrounding in piece_list:
                    if not surrounding.dead:
                        if (round(surrounding.pos_x) == round(piece.
                                                              pos_x-grid_size)
                            and round
                            (surrounding.
                             pos_y) == round
                            (piece.pos_y-grid_size) and surrounding.color !=
                            piece.
                                color):
                            no_jump = False
                            break
                if no_jump:
                    return True

                elif (round(item.pos_x) == round(piece.pos_x-2*grid_size) and
                      round(item.pos_y) == round(piece.pos_y-2*grid_size)):
                    return True
            elif direction == 'jump_downright':
                for surrounding in piece_list:
                    if not surrounding.dead:
                        if (round(surrounding.pos_x) == round(piece.pos_x
                                                              + grid_size) and
                            round(surrounding.
                                  pos_y) == round
                            (piece.
                             pos_y-grid_size)
                            and surrounding.
                            color != piece.
                                color):
                            no_jump = False
                            break
                if no_jump:
                    return True
                elif (round(item.pos_x) == round(piece.pos_x+2*grid_size) and
                      round(item.pos_y) == round(piece.pos_y-2*grid_size)):
                    return True
    return False


def piece_clear(selected_piece, direction):
    '''
    Function -- piece_clear
      this function kill the piece which is checked by other piece
    Parameter:
      selected_piece - the piece which kills other piece
      direction - selected_piece's movement direction
    return:
      none
    '''
    if direction == 'jump_upright':
        for red_piece in range(len(piece_list)):
            if (round(piece_list[red_piece].pos_x) == round(selected_piece.
                                                            pos_x - grid_size)
                and round(piece_list
                          [red_piece].pos_y)
                == round
                    (selected_piece.pos_y - grid_size)):
                piece_list[red_piece].dead = True
    elif direction == 'jump_upleft':
        for red_piece in range(len(piece_list)):
            if (round(piece_list[red_piece].pos_x) == round(selected_piece.
                                                            pos_x + grid_size)
                and round(piece_list
                          [red_piece].pos_y)
                == round
                    (selected_piece.pos_y - grid_size)):
                piece_list[red_piece].dead = True
    if direction == 'jump_downright':
        for red_piece in range(len(piece_list)):
            if (round(piece_list[red_piece].pos_x) == round(selected_piece.
                                                            pos_x - grid_size)
                and round(piece_list
                          [red_piece].pos_y)
                == round
                    (selected_piece.pos_y + grid_size)):
                piece_list[red_piece].dead = True
    elif direction == 'jump_downleft':
        for red_piece in range(len(piece_list)):
            if (round(piece_list[red_piece].pos_x) == round(selected_piece.
                                                            pos_x + grid_size)
                and round(piece_list
                          [red_piece].pos_y)
                == round
                    (selected_piece.pos_y + grid_size)):
                piece_list[red_piece].dead = True


def jump_determine():
    '''
    Function -- jump_determine
      this function updates the jumpable infomation of each piece after
       every move
    Parameter:
      none
    return:
      none
    '''
    for item in piece_list:
        item.jumpable = False
        for other_piece in piece_list:
            if not other_piece.dead and not item.dead:
                if (round(other_piece.pos_x) == round(item.pos_x-grid_size) and
                    round(other_piece.pos_y) == round(item.pos_y+grid_size) and
                        other_piece.color != item.color):
                    for piece in piece_list:
                        if (not piece.dead and round(piece.pos_x) == round
                            (item.pos_x-2*grid_size) and round(piece.pos_y) ==
                            round(item.pos_y+2*grid_size) or
                            item.out_board(width, default_size, "jump_upleft")
                                is True):
                            item.jumpable = False
                            break
                        else:
                            if (item.color == BLACK or isinstance(item,
                                                                  king_piece)):
                                item.jumpable = True
                    if item.jumpable:
                        break
                elif (round(other_piece.pos_x) == round(item.pos_x+grid_size)
                      and round(other_piece.pos_y) == round(item.pos_y
                                                            + grid_size) and
                      other_piece.color != item.color):
                    for piece in piece_list:
                        if (not piece.dead and round(piece.pos_x) == round
                            (item.pos_x+2*grid_size) and round(piece.pos_y) ==
                                round(item.pos_y+2*grid_size) or item.out_board
                                (width, default_size, 'jump_upright') is True):
                            item.jumpable = False
                            break
                        else:
                            if (item.color == BLACK or isinstance(item,
                                                                  king_piece)):
                                item.jumpable = True
                    if item.jumpable:
                        break
                elif (round(other_piece.pos_x) == round(item.pos_x-grid_size)
                      and round(other_piece.pos_y)
                      == round(item.pos_y-grid_size) and
                      other_piece.color != item.color):
                    for piece in piece_list:
                        if (not piece.dead and round(piece.pos_x) == round
                                (item.pos_x-2*grid_size) and round(piece.pos_y)
                                == round(item.pos_y-2*grid_size) or item.
                                out_board(width, default_size, 'jump_downleft')
                                is True):
                            item.jumpable = False
                            break
                        else:
                            if (item.color == RED or isinstance(item,
                                                                king_piece)):
                                item.jumpable = True
                    if item.jumpable:
                        break
                elif (round(other_piece.pos_x) == round(item.pos_x+grid_size)
                      and round(other_piece.pos_y)
                      == round(item.pos_y-grid_size) and
                      other_piece.color != item.color):
                    for piece in piece_list:
                        if (not piece.dead and round(piece.pos_x) == round
                                (item.pos_x+2*grid_size) and round(piece.pos_y)
                                == round(item.pos_y-2*grid_size) or item.
                                out_board(width, default_size,
                                          'jump_downright') is True):
                            item.jumpable = False
                            break
                        else:
                            if (item.color == RED or isinstance(item,
                                                                king_piece)):
                                item.jumpable = True
                    if item.jumpable:
                        break


def draw_state(black_score, red_score, turn):
    '''
    Function -- draw_state
      this function draws the score and turn of the game
    Parameter:
      black_score - points human player gets
      red_score - points computer gets
      turn - who take the turn in this round
    return:
      none
    '''
    turtle.tracer(False)
    state_pen.clear()
    state_pen.penup()
    state_pen.color('black')
    state_pen.goto(-width/2, -width/2-(((turtle.window_width()-width)/2)/2))
    state_pen.write("red_score : " + str(red_score),  align="left")
    state_pen.forward(width/6)
    state_pen.write("black_score: " + str(black_score), True, align="left")
    state_pen.forward(width/2)
    if turn == BLACK:
        state_pen.pencolor('black')
        turn = 'black'
    elif turn == RED:
        state_pen.pencolor('red')
        turn = 'red'
    state_pen.write("turn: " + turn)
    turtle.tracer(True)


def draw_win(side):
    '''
    Function -- draw_win
      this function informs the player when one of the player win the game
    Parameter:
      side - the player who win the game
    return:
      none
    '''
    win_pen.penup()
    win_pen.goto(-width/4, 0)
    win_pen.pendown()
    win_pen.pencolor("green")
    win_pen.write(side+" win!", align='left', font=("Arial", '40', 'normal'))


if __name__ == "__main__":
    main()
