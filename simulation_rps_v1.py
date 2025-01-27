from random import randint
import pygame
import matplotlib.pyplot as plt

# ----------------------------editable-variables--------------------------------

colors = [(209, 156, 151), (154, 139, 79), (140, 165, 113), (115, 145, 200), (166, 146, 186)]

board_size = 100
start_count = 5 * board_size
pixel_size = 2
new_time = 10
speed = 1

# -------------------------noneditable-variables--------------------------------

size = width, height = pixel_size * board_size, pixel_size * board_size
populations = [0] * len(colors)  # Track population sizes for each color

data_history = [[] for _ in colors]  # History of population sizes for saving

frame_counter = 0  # Frame counter for saving graphs

def update_population():
    global populations
    populations = [0] * len(colors)
    for row in board:
        for cell in row:
            for pixel in cell:
                populations[pixel.index] += 1

def save_graph():
    global frame_counter
    plt.figure()
    for i, history in enumerate(data_history):
        plt.plot(history, label=f"Color {i}", color=[c / 255 for c in colors[i]])
    plt.legend()
    plt.title("Pixel Population Over Time")
    plt.xlabel("Time")
    plt.ylabel("Population Size")
    plt.savefig(f"population_graph.png")
    plt.close()
    frame_counter += 1

# --------------------------------classes---------------------------------------
class pixel:
    def __init__(self, index, x_pos, y_pos):
        global screen, board, board_size
        self.color = colors[index]
        self.index = index
        self.lesser_index = (index + 1) % len(colors)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.active = True
        board[self.x_pos][self.y_pos].append(self)
        self.pixel_rect = pygame.Rect(self.x_pos * pixel_size, self.y_pos * pixel_size, pixel_size, pixel_size)

    def interact(self):  # check if there are any other pixels on the same position
        count = 1
        for item in board[self.x_pos][self.y_pos]:
            if item.index == self.lesser_index:
                item.active = False
            elif item.index == self.index:
                count += 1
                if count >= 3:
                    item.active = False
            else:
                self.active = False

    def move(self):
        board[self.x_pos][self.y_pos].remove(self)  # remove from current position on board
        self.y_pos += randint(-speed, speed)
        self.x_pos += randint(-speed, speed)
        if self.x_pos >= board_size:  # check to see if pixel is off the board
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = board_size - 1
        if self.y_pos >= board_size:
            self.y_pos = 0
        elif self.y_pos < 0:
            self.y_pos = board_size - 1
        self.pixel_rect.move(self.x_pos * pixel_size, self.y_pos * pixel_size)  # update rect position
        board[self.x_pos][self.y_pos].append(self)  # update board

    def update(self):
        global screen
        self.show()
        if randint(1, new_time) == 1:
            pixel(self.index, self.x_pos, self.y_pos)
        self.move()

    def show(self):
        pygame.draw.rect(screen, self.color, self.pixel_rect)

# --------------------------------functions-------------------------------------

def add_pixel(index, x_pos, y_pos):
    pixel(index, x_pos, y_pos)

def start():
    global board, generation, active_colors, total_list
    generation = 0
    board = []
    total_list = []
    for xx in range(0, board_size):  # create board
        board.append([])
        for yy in range(0, board_size):
            board[xx].append([])
    for ii in range(start_count):  # add first pixels
        for ii in range(len(colors)):
            add_pixel(ii, randint(1, board_size - 1), randint(1, board_size - 1))

# ---------------------------------main-loop-----------------------------------

def run():
    global screen, board, data_history

    board_length = len(board)
    while True:
        screen.fill((116, 104, 88))
        for ii in range(board_length):
            for jj in range(board_length):
                for item in board[ii][jj]:
                    if item.active:
                        item.update()
                    else:
                        board[ii][jj].remove(item)

        for ii in range(board_length):
            for jj in range(board_length):
                for item in board[ii][jj]:
                    item.interact()

        update_population()
        for i, history in enumerate(data_history):
            history.append(populations[i])
        save_graph()  # Save the graph after each update

        pygame.display.flip()

# ---------------------------------main-code-----------------------------------

pygame.init()
screen = pygame.display.set_mode(size)
start()
run()
