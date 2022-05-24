import time
import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )
        self.play = False
        self.play_again()

    def play_again(self):
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"

        self.config(bg="black")

        self.restart_key = ""

        self.score = 0

        self.load_assets()
        self.create_objects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(
            35, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        self.create_image(self.food_position[0], self.food_position[1], image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def load_restart_assets(self):
        self.delete(tk.ALL) # delete all objects, snake, food, score bar
        self.unbind_all("<Key>") # now do not do anything on key press
        self.config(bg="#196984")

        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2 - 50,
            text=f"Game over! You scored {self.score}!\n\nDo you want to play again (y or n)!",
            fill="black",
            font=14,
            tags="game-over"
        )

        self.bind_all("<Key>", self.on_key_press_restart)

    def on_key_press_restart(self, e):
        """
        Key listener on the game restart window, It will restart game on key "y",
        say thank you on "n" otherwise keep listening to keys.
        """
        new_key = e.keysym
        print("on restart: ", new_key) # For testing

        if new_key == "y" or new_key == "n":
            self.restart_key = new_key

    def end_game(self):
        self.delete(tk.ALL)
        self.unbind_all("<Key>")

        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Thanks for playing!",
            fill="#fff",
            font=14,
            tags="Thanks"
        )

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        new_direction = e.keysym
        print("In game: ", new_direction)

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
                new_direction in all_directions
                and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction


    def game_restart(self):
        id = self.after(1500, self.game_restart)

        if self.restart_key == "y":
            self.delete("game-over")
            self.unbind_all("<Key>")
            self.play_again()
        elif self.restart_key == "n":
            self.delete(tk.ALL)
            self.unbind_all("<Key>")

            self.end_game()
            self.after_cancel(id)

            # self.quit()


    def perform_actions(self):

        if self.check_collisions():
            self.load_restart_assets()
            self.game_restart()
        else:
            self.check_food_collision()
            self.move_snake()

            self.after(GAME_SPEED, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position



root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()

root.mainloop()
