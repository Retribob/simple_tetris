import pygame
from settings import *

class Button:
	def __init__(self, x, y, text_input, font):
		self.window = pygame.display.get_surface()
		self.x = x
		self.y = y
		self.font = font
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, '#FFFFFF')
		self.rect = self.text.get_rect(center = (self.x, self.y))
		self.mouse_pos = pygame.mouse.get_pos()

	def mouseInput(self):
		if self.rect.collidepoint(self.mouse_pos):
			self.text = self.font.render(self.text_input, True, 'YELLOW')
			return True
		else:
			self.text = self.font.render(self.text_input, True, '#FFFFFF')
			return False


	def run(self):
		self.window.blit(self.text, self.rect)
