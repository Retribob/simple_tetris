from settings import *
import pygame
from os import path


class Preview:
	def __init__(self):
		self.window = pygame.display.get_surface()
		self.preview_surface =  pygame.Surface((PREVIEW_WIDTH, PREVIEW_HEIGHT))
		self.preview_surface.fill(GRAY)	
		self.rect = self.preview_surface.get_rect(topleft = (WINDOW_WIDTH - (6*CELL_SIZE), 6*CELL_SIZE))

	#create dict of shapes with images
		self.shape_dict = {shape: pygame.image.load(path.join('assets', f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}


	def print_preview(self, shapes):
		# enumerate is used for iterating through the shapes list
		self.preview_surface.fill(GRAY)
		for i, shape in enumerate(shapes):
			shape_surface = self.shape_dict[shape]
			x = PREVIEW_WIDTH/2
			y = (PREVIEW_HEIGHT/3)*i + CELL_SIZE
			rect = shape_surface.get_rect(midtop = (x, y))
			self.preview_surface.blit(shape_surface, rect)


	def run(self, shapes):
		self.print_preview(shapes)
		self.window.blit(self.preview_surface, self.rect)
