from settings import *
import pygame


class Score:
	def __init__(self):
		self.window = pygame.display.get_surface()
		self.score_surface = pygame.Surface((SCORE_WIDTH, SCORE_HEIGHT)) 
		self.score_surface.fill(GRAY)
		self.myscore = 0
		self.mylevel = 1



	def display_text(self):
		pygame.font.init()
		self.my_font = pygame.font.Font('assets/font.ttf', 12)
		self.text_surface = self.my_font.render(f'Score:{self.myscore}', True, (255, 255, 255))
		self.level_surface = self.my_font.render(f'Level:{self.mylevel}', True, (255, 255, 255))
		self.score_surface.fill(GRAY)
		self.score_surface.blit(self.text_surface, (0, 0))
		self.score_surface.blit(self.level_surface, (0, 2*CELL_SIZE))

	def run(self):
		self.window.blit(self.score_surface, (CELL_SIZE, 6*CELL_SIZE))
		self.display_text()
