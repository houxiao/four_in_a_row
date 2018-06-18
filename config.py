# 初始化游戏变量

import pygame

# board size: 7*6
BOARDWIDTH = 7
BOARDHEIGHT = 6

DIFFICULTY = 2 # 游戏难度 AI搜索深度

CHESSSIZE = 50

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BORDER_X = int((WINDOWWIDTH - BOARDWIDTH * CHESSSIZE) / 2)
BORDER_Y = int((WINDOWHEIGHT - BOARDHEIGHT * CHESSSIZE) / 2)

TEXTCOLOR = (255, 255, 255)
# BGCOLOR = (0, 50, 255)
BGCOLOR = (255, 245, 238) # #FFF5EE

RED = 'red'
BLACK = 'black'

HUMAN = 'human'
COMPUTER = 'computer'

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Four in a Row')

REDPILERECT = pygame.Rect(int(CHESSSIZE / 2), WINDOWHEIGHT - int(3 * CHESSSIZE / 2), CHESSSIZE, CHESSSIZE)
BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * CHESSSIZE / 2), WINDOWHEIGHT - int(3 * CHESSSIZE / 2), CHESSSIZE,
                            CHESSSIZE)

REDTOKENIMG = pygame.transform.smoothscale(pygame.image.load('images/red.png'), (CHESSSIZE, CHESSSIZE))
BLACKTOKENIMG = pygame.transform.smoothscale(pygame.image.load('images/black.png'), (CHESSSIZE, CHESSSIZE))

BOARDIMG = pygame.transform.smoothscale(pygame.image.load('images/board.png'), (CHESSSIZE, CHESSSIZE))

HUMANWINNERIMG = pygame.image.load('images/human_win.png')
COMPUTERWINNERIMG = pygame.image.load('images/computer_win.png')
TIEWINNERIMG = pygame.image.load('images/tie.png')
WINNERRECT = HUMANWINNERIMG.get_rect()
WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))