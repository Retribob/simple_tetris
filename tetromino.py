import pygame
from timer import Timer
from settings import *
from random import choice
from sys import exit
from button1 import Button

#game class. The game class runs the generation of pieces as sprites,  the generation of ghost pieces as sprites as well as movement and controls
class Game:
	def __init__(self, new_piece, score_update):
		self.board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
		self.window = pygame.display.get_surface()
		self.board_surface.fill(GRAY)
		self.board_surface.get_rect(topleft = (6 * CELL_SIZE, 5 * CELL_SIZE))
		self.grid_surface = self.board_surface.copy()
		self.grid_surface.set_alpha(50)
		self.mask_surface = pygame.Surface((BOARD_WIDTH, 4 * CELL_SIZE))
		self.mask_surface.get_rect(topleft = (6 * CELL_SIZE, 5 * CELL_SIZE))
		self.mask_surface.fill(BLACK)
		self.font = pygame.font.Font("assets/font.ttf", 13)

		self.game_over = False
		self.board_data = [[0 for x in range(10)] for y in range(24)]
		self.sprites = pygame.sprite.Group()
		self.tetromino = Tetromino(self.sprites, choice(list(TETROMINOS.keys())), self.create_new_tetromino, self.board_data)
		self.new_piece = new_piece
		self.score_update = score_update
		self.new_score = 0
		self.new_level = 1
		self.score_interval = score_interval
		self.time_interval = TIME_INTERVAL
		self.time_interval2 = 1

		self.timer_event = pygame.USEREVENT+1
		pygame.time.set_timer(self.timer_event, self.time_interval)
		self.timer_event2 = pygame.USEREVENT+2
		pygame.time.set_timer(self.timer_event2, self.time_interval2)

	#draw grid function
	def grid(self):
		for i in range(1, BOARD_WIDTH):
			x = i*CELL_SIZE
	#line syntax: (surface, color, startpos, endpos)
			pygame.draw.line(self.grid_surface, LINE_COLOUR, (x, 0), (x, self.grid_surface.get_height()))
		for i in range(1, BOARD_HEIGHT):
			y = i*CELL_SIZE
			pygame.draw.line(self.grid_surface, LINE_COLOUR, (0, y), (self.grid_surface.get_width(), y))

	#check pieces pos on the board, if y pos is below a certain value, run game over function in main
	def check_game_over(self):
		for cell in self.tetromino.cells:
			if cell.pos.y < 3:
				self.game_over = True

	#creates a new tetromino. also checks for row clear and game over whenever a new piece is generated.
	def create_new_tetromino(self):
		self.clear_rows()
		self.check_game_over()
		self.tetromino = Tetromino(self.sprites, self.new_piece(), self.create_new_tetromino, self.board_data)

	#very simple and score counter. Every row cleared is 100 score. Once score exceeds an interval drop speed is increased.
	def score_multiplier(self, delete_rows):
		self.new_score += 100 * delete_rows

		if self.new_score >= self.score_interval:
			self.score_interval += self.new_score
			self.new_level += 1
			self.time_interval -= LEVEL_INTERVAL
			print(self.time_interval)
			pygame.time.set_timer(self.timer_event, self.time_interval)

		self.score_update(self.new_score, self.new_level)

	#function for increasing drop speed once the arrow down key is pressed
	def decrease_time(self, direction):
		self.time_interval -= direction*200
		pygame.time.set_timer(self.timer_event, self.time_interval)

	#clear row function. Check board data for a full row and clears both the board data and the sprites contained in the board data
	def clear_rows(self):
		delete_rows = []
		for i, row in enumerate(self.board_data):
			if all(row):
				delete_rows.append(i)


		if delete_rows:
			self.score_multiplier(len(delete_rows))
			for delete_row in delete_rows:
				for sprite in self.board_data[delete_row]:
					sprite.kill()

				for row in self.board_data:
					for cell in row:
						if cell and cell.pos.y < delete_row:
							cell.pos.y += 1
			self.board_data = [[0 for x in range(10)] for y in range(24)]
			for cell in self.sprites:
				self.board_data[int(cell.pos.y)][int(cell.pos.x)] = cell

	#run function that is called in the main loop
	def run(self):
		self.PAUSE_BUTTON = Button(CELL_SIZE, CELL_SIZE, '||',self.font)
		self.mouseclick = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == self.timer_event:
				self.tetromino.move_down(self.sprites)
			elif event.type == self.timer_event2:
				self.tetromino.move_down_ghostcell(self.sprites)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.PAUSE_BUTTON.mouseInput():
					self.mouseclick = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.tetromino.move_leftright_ghostcell(-1, self.sprites)
					self.tetromino.move_leftright(-1, self.sprites)
				if event.key == pygame.K_RIGHT:
					self.tetromino.move_leftright_ghostcell(1, self.sprites)
					self.tetromino.move_leftright(1, self.sprites)
				if event.key == pygame.K_x:
					self.tetromino.rotate(self.sprites, 1)
					self.tetromino.rotate_ghostcell(self.sprites, 1)
				if event.key == pygame.K_z:
					self.tetromino.rotate(self.sprites, -1)
					self.tetromino.rotate_ghostcell(self.sprites, -1)
				if event.key == pygame.K_DOWN:
					self.decrease_time(1)
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					self.decrease_time(-1)


	        #blit group
		self.PAUSE_BUTTON.mouseInput()
		self.PAUSE_BUTTON.run()
		self.window.blit(self.board_surface, (6*CELL_SIZE, 2*CELL_SIZE))
		self.window.blit(self.grid_surface, (6*CELL_SIZE, 2*CELL_SIZE))
		self.window.blit(self.mask_surface, (6*CELL_SIZE, 2*CELL_SIZE))

		self.tetromino.check_overlap()
		self.grid()
		self.sprites.update()
		self.board_surface.fill(GRAY)
		self.sprites.draw(self.board_surface)
		self.clear_rows()




class Tetromino:

	def __init__(self, group, shape, create_new_tetromino, board_data):
		self.shape = shape
		self.blockpos = TETROMINOS[shape]['shape']
		self.color = TETROMINOS[shape]['color']
		self.cells = [Cell(group, pos, self.color) for pos in self.blockpos]
		self.ghostcells = [Ghostcell(group, pos) for pos in self.blockpos]
		self.create_new_tetromino = create_new_tetromino
		self.board_data = board_data


	def check_overlap(self):
		self.ghostpos = []
		self.cellpos = []
		for cell in self.cells:
			self.cellpos.append(cell.pos.x)
			self.cellpos.append(cell.pos.y)
		for cell in self.ghostcells:
			self.ghostpos.append(cell.pos.x)
			self.ghostpos.append(cell.pos.y)

		if self.ghostpos == self.cellpos:
			for sprite in self.ghostcells:
				sprite.kill()

	def move_down(self, group):
		if not self.vertical_collide(self.cells):
			for cell in self.cells:
				cell.pos.y += 1
		else:
			for cell in self.cells:
				self.board_data[int(cell.pos.y)][int(cell.pos.x)] = cell
			self.create_new_tetromino()



	def move_leftright(self, move, group):
		if not self.horizontal_collide(self.cells, move):
			for cell in self.cells:
				cell.pos.x += move

	def rotate(self, group, direction):
		if self.shape != 'O':
			pivot_pos = self.cells[0].pos
			rotated = [cell.rotate(pivot_pos, direction) for cell in self.cells]
			for pos in rotated:
				if not 0 <= pos.x:
					for pos in rotated:
						pos.x += 1
				if not pos.x < 10:
					for pos in rotated:
						pos.x -= 1

				if not pos.y < 24:
					for pos in rotated:
						pos.y -= 1

				if self.board_data[int(pos.y)][int(pos.x)]:
					return

			for i, cell in enumerate(self.cells):
				cell.pos = rotated[i]


	def horizontal_collide(self, cells, move):
		collision_list = [cell.horizontal_collide(int(cell.pos.x + move), self.board_data) for cell in self.cells]
		if any(collision_list) == True:
			return True
		else:
			return False

	def vertical_collide(self, cells):
		collision_list = [cell.vertical_collide(int(cell.pos.y + 1), self.board_data) for cell in self.cells]
		if any(collision_list) == True:
			return True
		else:
			return False

#ghostcell section

	def move_down_ghostcell(self, group):
		if not self.vertical_collide_ghostcell(self.ghostcells):
			for cell in self.ghostcells:
				cell.pos.y += 1


	def move_leftright_ghostcell(self, move, group):
		if not self.horizontal_collide_ghostcell(self.ghostcells, move) and not self.horizontal_collide(self.cells, move):
			for cell in self.ghostcells:
				cell.pos.x += move
			if self.piece_collide_ghostcell(self.ghostcells) and not self.horizontal_collide(self.cells, move):
				while self.piece_collide_ghostcell(self.ghostcells):
					for cell in self.ghostcells:
						cell.pos.y -= 1


	def vertical_collide_ghostcell(self, ghostcells):
		collision_list = [cell.vertical_collide(int(cell.pos.y + 1), self.board_data) for cell in self.ghostcells]
		if any(collision_list) == True:
			return True
		else:
			return False


	def horizontal_collide_ghostcell(self, ghostcells, move):
		collision_list1 = [cell.ghost_collide1(int(cell.pos.x + move)) for cell in self.ghostcells]
		if any(collision_list1) == True:
			return True


	def piece_collide_ghostcell(self, ghostcells):
		collision_list = [cell.ghost_collide2(int(cell.pos.x), self.board_data) for cell in self.ghostcells]
		if any(collision_list) == True:
			return True

	def rotate_ghostcell(self, group, direction):
		if self.shape != 'O':
			pivot_pos = self.ghostcells[0].pos
			rotated = [cell.rotate(pivot_pos, direction) for cell in self.ghostcells]
			for pos in rotated:
				if not 0 <= pos.x:
					for pos in rotated:
						pos.x += 1
				if not pos.x < 10:
					for pos in rotated:
						pos.x -= 1

				if not pos.y < 24:
					for pos in rotated:
						pos.y -= 1

				if self.board_data[int(pos.y)][int(pos.x)]:
					for pos in rotated:
						pos.y -= 1

			for i, cell in enumerate(self.ghostcells):
				cell.pos = rotated[i]


class Cell(pygame.sprite.Sprite):

	def __init__(self, group, pos, color):

		super().__init__(group)
		self.image = pygame.image.load(f'assets/{color}.png').convert_alpha()
		self.pos = pygame.Vector2(pos) + (4, 3)
		self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)
		self.cell_mask = pygame.mask.from_surface(self.image)


	def rotate(self, pivot_pos, direction):
		distance = self.pos - pivot_pos
		rotated_vector = distance.rotate(direction*90)
		new_pos = pivot_pos + rotated_vector
		return new_pos

	def horizontal_collide(self, posx, board_data):
		if not 0 <= posx < 10:
			return True
		if board_data[int(self.pos.y)][posx]:
			return True

	def vertical_collide(self, posy, board_data):
		if posy >= 24:
			return True
		if board_data[posy][int(self.pos.x)]:
			return True

	def update(self):
		self.rect.topleft = self.pos * CELL_SIZE



class Ghostcell(pygame.sprite.Sprite):
	def __init__(self, group, pos):
		super().__init__(group)
		self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
		self.image.fill('#FFFFFF')
		self.image.set_alpha(50)
		self.pos = pygame.Vector2(pos) + (4, 3)
		self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)



	def rotate(self, pivot_pos, direction):
		distance = self.pos - pivot_pos
		rotated_vector = distance.rotate(direction*90)
		new_pos = pivot_pos + rotated_vector
		return new_pos


	def ghost_collide1(self, posx):
		if not 0 <= posx < 10:
			return True

	def ghost_collide2(self, posx, board_data):
		if board_data[int(self.pos.y)][posx]:
			return True

	def vertical_collide(self, posy, board_data):
		if posy >= 24:
			return True
		if board_data[posy][int(self.pos.x)]:
			return True

	def update(self):
		self.rect.topleft = self.pos * CELL_SIZE




