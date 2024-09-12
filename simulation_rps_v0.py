 #---------------------------------libraries------------------------------------
from random import randint
import sys, pygame
import matplotlib.pyplot as plt
import numpy as np
 
#----------------------------editable-variables--------------------------------
 
# create RGB values for colors that will be used
RGB_values = {"black": (10, 10, 10), "red": (255, 51, 0), "blue": (20, 20, 255),
"yellow": (200, 255, 0), "green": (0, 200, 0), "cyan": (102, 255, 204),
"purple": (200, 0, 255), "orange": (255, 180, 0), "white": (255, 255, 255), "background":(0,0,0)}
 
colors = ["red","yellow","blue"]#, "green", "blue","cyan","purple"]
 

board_size = 100
start_count = 5*board_size
pixel_size = 3
new_time = 2
speed = 2
 
#-------------------------noneditable-variables--------------------------------

size = width, height = pixel_size*board_size, pixel_size*board_size
 
#--------------------------------classes---------------------------------------
class pixel:
    def __init__(self, color, x_pos, y_pos):
        global screen, board, board_size
        self.color = color
        self.lesser_color = colors[(colors.index(color) + 1) % len(colors)]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.active = True
        board[self.x_pos][self.y_pos].append(self)
        self.pixel_rect = pygame.Rect(self.x_pos*pixel_size, self.y_pos*pixel_size, pixel_size, pixel_size)
        self.RGB = RGB_values[color]
       
    def interact(self): # check if there are any other pixels on the same position
        count = 1
        for item in board[self.x_pos][self.y_pos]:
            if item.color == self.lesser_color:
                item.active = False
            elif item.color == self.color:
                count += 1
                if count >= 3:
                    item.active = False
            else:
                self.active = False
       
    def move(self):
        board[self.x_pos][self.y_pos].remove(self) #remove from current postion on board
        self.y_pos += randint(-speed, speed)
        self.x_pos += randint(-speed, speed)
        if self.x_pos > board_size: # check to see if pixel is off the board
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = board_size
        if self.y_pos > board_size:
            self.y_pos = 0
        elif self.y_pos < 0:
            self.y_pos = board_size
        self.pixel_rect.move(self.x_pos*pixel_size,self.y_pos*pixel_size) # update rect position
        board[self.x_pos][self.y_pos].append(self) # update board
   
    def update(self):
        global screen, displaying
        self.show()
        if randint(1,new_time) == 1:
            add_pixel(self.color,self.x_pos,self.y_pos)
        self.move()

       
    def show(self):
        pygame.draw.rect(screen, self.RGB, self.pixel_rect)
       
 
#--------------------------------functions-------------------------------------
 
def add_pixel(color,x_pos,y_pos):
    pixel(color,x_pos,y_pos)
   
def start():
    global board, generation, active_colors, total_list
    generation = 0
    board = []
    total_list = []
    for xx in range(0,board_size+1):#create board
        board.append([])
        for yy in range(0,board_size+1):
            board[xx].append([])
    for ii in range(0,start_count):#add first pixels
        for item in colors:
            add_pixel(item,randint(1,board_size),randint(1,board_size))

   
#---------------------------------main-loop-----------------------------------
 
def run():
    global screen, board, generation, graphing, displaying, graph_last
    board_length = len(board)
    running = True
    generation = 0
    max_generations = 100000  # You can set a limit on the number of generations

    while running and generation < max_generations:  # Add a condition to break out of the loop
        screen.fill(RGB_values["background"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set running to False to exit the loop
        for ii in range(board_length):
            for jj in range(board_length):
                for item in board[ii][jj]:
                    if item.active:
                        item.update()
                    else:
                        board[ii][jj].remove(item)
        board_length = len(board)
        for ii in range(board_length):
            for jj in range(board_length):
                for item in board[ii][jj]:
                    item.interact()
        pygame.display.flip()
        generation += 1

       
#---------------------------------main-code-----------------------------------

graphing = True
displaying = True
printing = True
display_total = True
graph_last = True
pygame.init()
screen = pygame.display.set_mode(size)
start()
run()
