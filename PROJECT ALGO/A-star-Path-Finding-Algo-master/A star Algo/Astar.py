import pygame
import math
from queue import PriorityQueue

# this is dimension, setting the display !!
WIDTH = 500 
# WIN === window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# these are the color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
	 # init in python is similar as constructors in c++
	def __init__(self, row, col, width, total__rows):
		self.row = row 
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total__rows = total__rows

	 # gives the node postion
	def get_pos(self):
		return self.row,self.col 
	 # check whether it is closed..
	def is_closed(self):
		return self.color == RED
	 # check whether it is opened..
	def is_open(self):
		return self.color == GREEN
	 # check whether it is blocked..
	def is_barrier(self):
		return self.color == BLACK
	 # it give the starting point..
	def is_start(self):
		return self.color == ORANGE
	 # it give the ending point..
	def is_end(self):
		return self.color == TURQUOISE
	 # it reset whole to white...(making empty)
	def reset(self):
		self.color = WHITE    	

	# basically all this function sets the value
	
	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE
	
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = [] 
		 # here -1 becoz we checking " DOWN " whether we can add a one more grid in our 2D neighbour array and this must not be equal to barrier 
		if self.row < self.total__rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col]) # here +1 becoz we are adding a new grid

		 # think similary " UP "
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])

		 # think similary " RIGHT " 
		if self.col < self.total__rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])
		
		 # think similary " LEFT " 
		if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])

					

	 # here..lt stand for less than..comparison betweeon nodes
	def __lt__(self, other):
		return False
	

 # making for the heuristic distance finding function
def h(p1, p2):    
   x1, y1 = p1
   x2, y2 = p2
   return abs(x1-x2) + abs(y1-y2)

 # this is function which will show us the shortest path
def reconstruct_path(came_from, current, draw):
	while current in came_from:  # moving from end to prev connected -> prev connected -> ...... -> start !!
		current = came_from[current]
		current.make_path()
		draw()



# Here is our hero A* Algo starts work!!

def algorithm(draw, grid, start, end):
	count = 0 # if the f score was same then from count we can find which variable inserted first
	open_set = PriorityQueue() # pq is short form for PriorityQueue
	open_set.put((0, count, start)) # adding in pq
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}  # this is simply iterating every grid and set as infinity
	g_score[start] = 0 
	f_score = {node: float("inf") for row in grid for node in row}  # this is simply iterating every grid and set as infinity
	f_score[start] = h(start.get_pos(), end.get_pos()) 
	

	open_set_hash = {start} # as pq dont tell wheter the node is inside the queue, so we need this hash to track..
	
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # this gives us the lowest one
		open_set_hash.remove(current)
		
		if current == end:
			# we found the path
			reconstruct_path(came_from, end, draw)
			end.make_end() # becoz reconstruct path will make purple also here!!
			return True 
 
		 # this will give the temp g score assuming from this point to end     
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			# when we get a nice score we just update the distance
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1                                               # if the neighbor is not present then just add in pq and in openset hash and increase count
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False    
   




# making grids    
def make_grid(rows, width):
	grid = []
	gap = width // rows # it gives the gap inbetween the rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows) # making a object and calling the function
			grid[i].append(node)
	return grid		
# making the grids color as grey as we run from top to bottom and left to right
def draw_grid(win, rows, width):
	gap = width // rows  # it gives the gap inbetween the rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE) # its filling white

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()		
	 
# from this function we get the positon where the cursor clicks
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	
	row = y // gap  # as we are taking vertical as row 
	col = x // gap  # and horizontal as column..

	return row, col

# it is the main loop which checks what we are doing!!..
def main(win, width):
	ROWS = 50 # setting up the rows..its very dynamic we can change values
	grid = make_grid(ROWS, width)
	
	start = None # setting up start and
	end = None   # end points
	
	run  = True     # just setting up the variables

	 # this while is just loop through every event whatever happens in our win
	while run:
		draw(win, grid, ROWS, width) # this is draw function which will call in every loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # if event type is quit then stop
				run = False

		

			if pygame.mouse.get_pressed()[0]: # this pygame cmd stand for left mouse btn
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width) # actually this will give the x,y postion of the grid, which we clicked in win
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()
					
				elif node != end and node != start:
					 node.make_barrier()  

			elif pygame.mouse.get_pressed()[2]: # this pygame cmd stand for right mouse btn	
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width) # actually this will give the x,y postion of the grid, which we clicked in win
				node = grid[row][col]
				node.reset()  # reset everything to white means directly deleting the color in the grids
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:   # this is part where our algo start running
				if event.key == pygame.K_SPACE and start and end:  # checking wheter the space key is pressed and started is false
					for row in grid:                             # once the event starts this for loop will colects all the neighbours
						for node in row:
							node.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)		

					# here lambda means ===>>> x = def fun():
					#                                 print("hello")
					#                         x()     
					# lambda is an ananymous function , here its simply x = lambda : print("hello") 
					# indirectly calling a function by calling another function...

				if event.key == pygame.K_c:            # this is for setting reset, so we dont want to click close btn !!
					start = None
					end = None                    
					grid = make_grid(ROWS, width)

				


	pygame.quit() 			

main(WIN, WIDTH)    