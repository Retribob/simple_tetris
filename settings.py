import pygame

#windows and game size settings
CELL_SIZE = 30
BOARD_WIDTH = 10 * CELL_SIZE
BOARD_HEIGHT = 24 * CELL_SIZE
PREVIEW_WIDTH = 5 * CELL_SIZE
PREVIEW_HEIGHT = BOARD_HEIGHT - (4*CELL_SIZE)
SCORE_WIDTH = 4* CELL_SIZE
SCORE_HEIGHT = SCORE_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + (8*CELL_SIZE)
WINDOW_WIDTH = BOARD_WIDTH + SCORE_WIDTH + PREVIEW_WIDTH + (4*CELL_SIZE)


#colours
YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'
LINE_COLOUR = '#FFFFFF'
BLACK = '#000000'


#tetromino structure
TETROMINOS = {
'T': {'shape':[(0, 0), (-1, 0), (1, 0), (0, 1)], 'color': 'Purple'},
'Z': {'shape':[(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': 'Red'},
'S': {'shape':[(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': 'Green'},
'L': {'shape':[(0, 0), (0, -1), (0, 1), (1, 1)], 'color': 'Orange'},
'J':{'shape':[(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': 'Blue'},
'I':{'shape':[(0, 0), (0, -1), (0, -2), (0, 1)], 'color': 'Cyan'},
'O':{'shape':[(0, 0), (1, 0), (0, -1), (1, -1)], 'color': 'Yellow'}
}

#time settings
TIME_INTERVAL = 300
LEVEL_INTERVAL = 50
MOVE_INTERVAL = 50
DEAD_INTERVAL = 100


#score settings
score_interval = 1000
