# -*- coding:utf-8 -*-
# !/usr/bin/python

import sys
from random import randint, choice
from copy import deepcopy

import pygame
from pygame.locals import *

from config import *

def get_human_move(board):
    draggingToken = False
    tokenX, tokenY = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #  press the mouse and in red chess area
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                draggingToken = True
                tokenX, tokenY = event.pos
            # start dragging
            elif event.type == MOUSEMOTION and draggingToken:
                # update dragged chess pos
                tokenX, tokenY = event.pos
            # if chess is above board
            elif event.type == MOUSEBUTTONUP and draggingToken:
                #如果棋子被拖拽在board的正上方
                if tokenY < BORDER_Y and tokenX > BORDER_X and tokenX < WINDOWWIDTH - BORDER_X:
                    # which column chess would drop
                    column = int((tokenX - BORDER_X) / CHESSSIZE)
                    if is_valid_move(board, column):
                        animate_dropping(board, column, RED)
                        board[column][get_lowest_empty_space(board, column)] = RED
                        draw_board(board)
                        pygame.display.update()
                        return
                tokenX, tokenY = None, None
                draggingToken = False
        if tokenX is not None and tokenY is not None:
            # chess moves with mouse
            draw_board(board, {'x': tokenX - int(CHESSSIZE / 2), 'y': tokenY - int(CHESSSIZE / 2), 'color': RED})
        else:
            #invalid movement and release the mouse
            draw_board(board)

        pygame.display.update()
        FPSCLOCK.tick()


def animate_dropping(board, column, color):
    x = BORDER_X + column * CHESSSIZE
    y = BORDER_Y - CHESSSIZE
    drop_speed = 1.0
    lowest_empty_space = get_lowest_empty_space(board, column)
    while True:
        y += int(drop_speed)
        drop_speed += 0.5
        if int((y-BORDER_Y) / CHESSSIZE) >= lowest_empty_space:
            return
        draw_board(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()


def get_computer_move(board):
    potentialMoves = get_potential_moves(board, BLACK, DIFFICULTY)
    bestMoves = []
    bestMoveFitness = -BOARDWIDTH
    for i in range(len(potentialMoves)):
        if potentialMoves[i] > bestMoveFitness and is_valid_move(board, i):
            bestMoveFitness = potentialMoves[i]
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and is_valid_move(board, i):
            bestMoves.append(i)
    return choice(bestMoves)


def get_potential_moves(board, p_color, depth):
    if depth is 0 or is_board_full(board):
        return [0] * BOARDWIDTH
    # make sure enemy's chess color
    if p_color is RED:
        enemy_color = BLACK
    else:
        enemy_color = RED

    # initialize a potential move list, with init_values are 0s
    potentialMoves = [0] * BOARDWIDTH
    for firstMove in range(BOARDWIDTH):
        # 对每一列进行遍历，将双方中的任一方的移动称为firstMove
        # 则另外一方的移动就称为对手，counterMove。
        # 这里我们的firstMove为AI，对手为玩家。
        dupeBoard = deepcopy(board)
        if not is_valid_move(dupeBoard, firstMove):
            continue
        make_move(dupeBoard, p_color, firstMove)
        if is_winner(dupeBoard, p_color):
            # 获胜的棋子自动获得一个很高的数值来表示其获胜的几率
            # 数值越大，获胜可能性越大，对手获胜可能性越小。
            potentialMoves[firstMove] = 1
            break
        else:
            if is_board_full(dupeBoard):
                # tie game
                potentialMoves[firstMove] = 0
            else:
                # consider enemy's moves
                for counterMove in range(BOARDWIDTH):
                    dupeBoard2 = deepcopy(dupeBoard)
                    if not is_valid_move(dupeBoard2, counterMove):
                        continue
                    make_move(dupeBoard2, enemy_color, counterMove)
                    if is_winner(dupeBoard2, enemy_color):
                        # enemy win
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        # 递归调用
                        result = get_potential_moves(dupeBoard2, p_color, depth-1)
                        potentialMoves[firstMove] += (sum(result)*1.0 / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves

def animate_computer_moving(board, column):
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 1.0
    # from black example to above board
    while y > (BORDER_Y - CHESSSIZE):
        y -= int(speed)
        speed += 0.5
        draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # drop black chess
    y = BORDER_Y - CHESSSIZE
    speed = 1.0
    while x > (BORDER_X + column * CHESSSIZE):
        x -= int(speed)
        speed += 0.5
        draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    animate_dropping(board, column, BLACK)


def get_lowest_empty_space(board, column):
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] is None:
            return y
    return -1


def make_move(board, player, column):
    lowest = get_lowest_empty_space(board, column)
    if lowest != -1:
        board[column][lowest] = player


def is_valid_move(board, column):
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] is not None:
        return False
    return True

def is_board_full(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] is None:
                return False
    return True


def is_winner(board, p_color):
    # herizontal
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] is p_color and board[x+1][y] is p_color and board[x+2][y] is p_color and board[x+3][y] is p_color:
                return True
    # vertical
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] is p_color and board[x][y+1] is p_color and board[x][y+2] is p_color and board[x][y+3] is p_color:
                return True
    # diagonal1
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] is p_color and board[x+1][y-1] is p_color and board[x+2][y-2] is p_color and board[x+3][y-3] is p_color:
                return True
    # diagonal2
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] is p_color and board[x+1][y+1] is p_color and board[x+2][y+2] is p_color and board[x+3][y+3] is p_color:
                return True
    return False


def get_new_board():
    board = []
    for x in range(BOARDWIDTH):
        board.append([None] * BOARDHEIGHT)
    return board


def draw_board(board, extraToken=None):
    DISPLAYSURF.fill(BGCOLOR)
    chessRect = pygame.Rect(0, 0, CHESSSIZE, CHESSSIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            chessRect.topleft = (BORDER_X + (x * CHESSSIZE), BORDER_Y + (y * CHESSSIZE))
            if board[x][y] == RED:
                DISPLAYSURF.blit(REDTOKENIMG, chessRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, chessRect)

    if extraToken is not None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(REDTOKENIMG,
                             (extraToken['x'], extraToken['y'], CHESSSIZE, CHESSSIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG,
                             (extraToken['x'], extraToken['y'], CHESSSIZE, CHESSSIZE))

    # draw board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            chessRect.topleft = (BORDER_X + (x * CHESSSIZE),
                                 BORDER_Y + (y * CHESSSIZE))
            DISPLAYSURF.blit(BOARDIMG, chessRect)

    # draw chess example
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT)
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)


def run_games(isFirstGame):
    if isFirstGame:
        turn = COMPUTER
    else:
        if randint(0, 1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN
    mainBoard = get_new_board()

    while True:
        if is_board_full(mainBoard):
            winnerImg = TIEWINNERIMG
            break
        if turn == HUMAN:
            get_human_move(mainBoard)
            if is_winner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG
                break
            turn = COMPUTER
        else:
            column = get_computer_move(mainBoard)
            animate_computer_moving(mainBoard, column)
            make_move(mainBoard, BLACK, column)
            if is_winner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG
                break
            turn = HUMAN

    while True:
        draw_board(mainBoard)
        DISPLAYSURF.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def main():
    isFirstGame = True
    while True:
        run_games(isFirstGame)
        isFirstGame = False

if __name__ == '__main__':
    main()