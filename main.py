import pygame

#importing modules
from settings import *
from tetromino import *
from random import choice
from preview import Preview
from score import Score
from sys import exit
from button1 import Button


#initializes pygame
pygame.init()
frame_tick = pygame.time.Clock()

#windows and surfaces
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def create_new_tetromino():
	tetromino = Tetromino(sprites, choice(list(TETROMINOS.keys())))


def get_font(size):
	return pygame.font.Font("assets/font.ttf", size)


preview_pieces = [choice(list(TETROMINOS.keys())) for shape in range(3)]
def new_piece():
	new_piece = preview_pieces.pop(0)
	preview_pieces.append(choice(list(TETROMINOS.keys())))
	return new_piece


score = Score()

def score_update(score1, level1):
	score.myscore = score1
	score.mylevel = level1



#timer_event = pygame.USEREVENT+1
#pygame.time.set_timer(timer_event, game.time_interval)
game = Game(new_piece, score_update)
preview = Preview()


def tetrisGame():
#this is where everything is run
	while True:
		window.fill('black')
		score.run()
		preview.run(preview_pieces)
		game.run()

		if game.mouseclick:
			pause_menu()


		pygame.display.update()
		frame_tick.tick(60)


def setting_menu():
	while True:
		window.fill('black')
		pygame.display.update()
		frame_tick.tick(60)


def pause_menu():
	while True:
		window.fill('black')
		RESUME_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'RESUME', font=get_font(30))
		MENU_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*14, 'MAIN MENU', font=get_font(30))
		QUIT1_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*16, 'QUIT', font=get_font(30))

		for button in [RESUME_BUTTON, MENU_BUTTON, QUIT1_BUTTON]:
			button.mouseInput()
			button.run()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if RESUME_BUTTON.mouseInput():
					tetrisGame()
				elif MENU_BUTTON.mouseInput():
					main_menu()
				elif QUIT1_BUTTON.mouseInput():
					pygame.quit()
					exit()
		pygame.display.update()
		frame_tick.tick(60)

def main_menu():
	while True:

		window.fill('black')
		MENU_TEXT = get_font(50).render("TETRIS", True, "#FFFFFF")
		MENU_RECT = MENU_TEXT.get_rect(center = (WINDOW_WIDTH/2, CELL_SIZE*4))

		PLAY_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*10, 'PLAY', font=get_font(30))
		SETTINGS_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'SETTINGS', font=get_font(30))
		QUIT_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*14, 'QUIT',  font=get_font(30))

		for button in [PLAY_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
			button.mouseInput()
			button.run()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.mouseInput():
					tetrisGame()
				elif SETTINGS_BUTTON.mouseInput():
					setting_menu()
				elif QUIT_BUTTON.mouseInput():
					pygame.quit()
					exit()


		window.blit(MENU_TEXT, MENU_RECT)
		pygame.display.update()
		frame_tick.tick(60)

main_menu()
