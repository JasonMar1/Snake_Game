import tkinter
from tkinter import *
import random
import time

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 60
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="Snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction

    elif new_direction == "right":
        if direction != "left":
            direction = new_direction

    if new_direction == "up":
        if direction != "down":
            direction = new_direction

    if new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for snake_body_part in snake.coordinates[1:]:
        if x == snake_body_part[0] and y == snake_body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Arial", 60),
                       text="GAME OVER", fill="red")
    window.update()
    time.sleep(2)

    button_restart.grid(row=0, column=0, padx=(10, 10))
    button_exit.grid(row=0, column=1, padx=(10, 10))
    label.grid_remove()


def new_game():
    global score, direction
    score = 0
    direction = "down"

    label.config(text="Score:{}".format(score))
    label.grid(row=0, column=0)
    button_restart.grid_remove()
    button_exit.grid_remove()

    canvas.delete(ALL)
    canvas.config(bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

    food = Food()
    snake = Snake()
    next_turn(snake, food)


def window_quit():
    exit()


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

pic = PhotoImage(file="snake.png")
window.iconphoto(True, pic)

score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=("Arial", 40))
label.grid(row=0, column=0, columnspan=2)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.grid(row=1, column=0, columnspan=2)

button_restart = Button(window, text="Restart?", font=("Arial", 40), command=new_game)
button_exit = Button(window, text="Exit", font=("Arial", 40), command=window.quit)

button_restart.grid(row=0, column=0, padx=(10, 10))
button_exit.grid(row=0, column=1, padx=(10, 10))
button_restart.grid_remove()
button_exit.grid_remove()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
