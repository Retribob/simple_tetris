import pygame

#importing modules
from settings import *
from tetromino import *
from random import choice
from preview import Preview
from score import Score
from sys import exit
from button1 import Button
from inputBox import InputBox

#things to note:
#1. the game does not have a seven bag system. Pieces are completely random.
#2. No swap pieces
#To do:
#1. Allow rotations when pieces are next to other pieces.
#2. Some bugs with ghost pieces and rotations
#3. Implement a settings menu to adjust sound and control settings.
#4. Implement a timing in which you can still move the piece after it can no longer move down


#initializes pygame
pygame.init()
frame_tick = pygame.time.Clock()

#global function for font size
def get_font(size):
		return pygame.font.Font("assets/font.ttf", size)





class TetrisGame():
	def __init__(self, get_font):
		self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.get_font = get_font
		self.preview_pieces = [choice(list(TETROMINOS.keys())) for shape in range(3)]
		self.game = Game(self.new_piece, self.score_update)
		self.preview = Preview()
		self.score = Score()
		self.new_game = False


	#this function takes a piece from the preview list and returns the piece
	def new_piece(self):
		self.next_piece = self.preview_pieces.pop(0)
		self.preview_pieces.append(choice(list(TETROMINOS.keys())))
		return self.next_piece

	#function for updating score and level between score.py and tetromino.py
	def score_update(self, score1, level1):
		self.score.myscore = score1
		self.score.mylevel = level1

	#game over function. Draws over the game board and gives the option to quit or retry
	def game_over(self):
		while True:
			self.window.fill('black')
			self.GAME_OVER_TEXT = get_font(50).render("GAME OVER", True, '#FFFFFF')
			self.GAME_OVER_RECT = self.GAME_OVER_TEXT.get_rect(center = (WINDOW_WIDTH/2, CELL_SIZE*10))
			self.RETRY_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*14, 'RETRY', font=self.get_font(30))
			self.QUIT2_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*16, 'QUIT', font=self.get_font(30))
			self.RETRY_BUTTON.mouseInput()
			self.RETRY_BUTTON.run()
			self.QUIT2_BUTTON.mouseInput()
			self.QUIT2_BUTTON.run()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.RETRY_BUTTON.mouseInput():
						self.new_game = True
						self.game_board()
					if self.QUIT2_BUTTON.mouseInput():
						pygame.quit()
						exit()
			self.window.blit(self.GAME_OVER_TEXT, self.GAME_OVER_RECT)
			pygame.display.update()
			frame_tick.tick(60)

	#pause menu function. Draws over the game board when the 'pause' button is clicked on
	def pause_menu(self):
		while True:
			self.window.fill('black')
			self.RESUME_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'RESUME', font=self.get_font(30))
			self.MENU_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*14, 'MAIN MENU', font=self.get_font(30))
			self.QUIT1_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*16, 'QUIT', font=self.get_font(30))

			for button in [self.RESUME_BUTTON, self.MENU_BUTTON, self.QUIT1_BUTTON]:
				button.mouseInput()
				button.run()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.RESUME_BUTTON.mouseInput():
						self.game_board()
					elif self.MENU_BUTTON.mouseInput():
						self.main_menu()
					elif self.QUIT1_BUTTON.mouseInput():
						pygame.quit()
						exit()
			pygame.display.update()
			frame_tick.tick(60)


	#game function. Draws the preview, score and game board. The game is run from this function.
	def game_board(self):
		if self.new_game:
			self.preview_pieces = [choice(list(TETROMINOS.keys())) for shape in range(3)]
			self.game = Game(self.new_piece, self.score_update)
			self.preview = Preview()
			self.score = Score()
			self.new_game = False

		pygame.mixer.music.unload()
		pygame.mixer.music.load('music/03. A-Type Music (Korobeiniki).mp3')
		pygame.mixer.music.set_volume(0)
		pygame.mixer.music.play(-1)

		while True:
			self.window.fill('black')
			self.score.run()
			self.preview.run(self.preview_pieces)
			self.game.run()

			if self.game.mouseclick:
				self.pause_menu()


			if self.game.game_over:
				self.game_over()

			pygame.display.update()
			frame_tick.tick(60)


#settings menu. Currently unused.
#	def settings_change(self):
#		self.window.fill('black')
#		self.Input_Box = InputBox(WINDOW_WIDTH/2, CELL_SIZE*9)
#		while True:
#			self.Input_Text = get_font(20).render('please key in your controls', True, '#FFFFFF')
#			self.Input_Text_Rect = self.Input_Text.get_rect(center = (WINDOW_WIDTH/2, CELL_SIZE*7))
#			for event in pygame.event.get():
#				if event.type == pygame.QUIT:
#					pygame.quit()
#					exit()
#				if event.type == pygame.KEYDOWN:
#					print(self.Input_Box.text)
#					self.Input_Box.key_event(event)
#
#			self.window.blit(self.Input_Text, self.Input_Text_Rect)
#			self.Input_Box.run()
#			pygame.display.update()
#			frame_tick.tick(60)
#

#	def settings_menu(self):
#		self.window.fill('black')
#		while True:
#			self.CLICK_TO_CHANGE = get_font(45).render('click to change', True, '#FFFFFF')
#			self.CLICK_RECT = self.CLICK_TO_CHANGE.get_rect(center=(WINDOW_WIDTH/2, CELL_SIZE*7))
#			self.MOVELEFT_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*10, 'LEFT CONTROLS', font=self.get_font(30))
#			self.MOVERIGHT_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'RIGHT CONTROLS', font=self.get_font(30))
#			self.ROTATE90_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*14, 'ROTATE CLOCKWISE', font=self.get_font(30))
#			self.ROTATE_90_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*16, 'ROTATE ANTICLOCKWISE', font=self.get_font(30))
#			self.SOFTDROP_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*18, 'SOFTDROP CONTROLS', font=self.get_font(30))
#			self.SOUND_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*20, 'SOUND VOLUME', font=self.get_font(30))
#			self.BACK_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*23, 'Back', font=self.get_font(30))
#
#
#			for button in [self.MOVELEFT_BUTTON, self.MOVERIGHT_BUTTON, self.ROTATE90_BUTTON, self.ROTATE_90_BUTTON, self.SOFTDROP_BUTTON, self.SOUND_BUTTON, self.BACK_BUTTON]:
#				button.mouseInput()
#				button.run()
#
#			for event in pygame.event.get():
#				if event.type == pygame.QUIT:
#					pygame.quit()
#					exit()
#				elif event.type == pygame.MOUSEBUTTONDOWN:
#					if self.BACK_BUTTON.mouseInput():
#						self.main_menu()
#					elif self.MOVELEFT_BUTTON.mouseInput():
#						self.settings_change()
#
#			self.window.blit(self.CLICK_TO_CHANGE, self.CLICK_RECT)
#			pygame.display.update()
#			frame_tick.tick(60)

#this function is run when main is first run. Clicking the play button starts the game and also resets the previous board state.
	def main_menu(self):
		pygame.mixer.music.unload()
		pygame.mixer.music.load('music/01. Title.mp3')
		pygame.mixer.music.set_volume(0)
		pygame.mixer.music.play(-1)

		while True:

			self.window.fill('black')
			self.MENU_TEXT = get_font(50).render("TETRIS", True, "#FFFFFF")
			self.MENU_RECT = self.MENU_TEXT.get_rect(center = (WINDOW_WIDTH/2, CELL_SIZE*4))
			self.PLAY_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*10, 'PLAY', font=self.get_font(30))
			#self.SETTINGS_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'SETTINGS', font=self.get_font(30))
			self.QUIT_BUTTON = Button(WINDOW_WIDTH/2, CELL_SIZE*12, 'QUIT',  font=self.get_font(30))


			for button in [self.PLAY_BUTTON, self.QUIT_BUTTON]:
				button.mouseInput()
				button.run()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.PLAY_BUTTON.mouseInput():
						self.new_game = True
						self.game_board()
					#if self.SETTINGS_BUTTON.mouseInput():
					#	self.settings_menu()
					if self.QUIT_BUTTON.mouseInput():
						pygame.quit()
						exit()
			self.window.blit(self.MENU_TEXT, self.MENU_RECT)
			pygame.display.update()
			frame_tick.tick(60)




main = TetrisGame(get_font)
main.main_menu()

