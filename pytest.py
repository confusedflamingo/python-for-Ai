import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class BouncingPixelApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Worm Game (Early Alpha) v0.1.05")

        # Welcome the player with a dialog box
        self.show_welcome_dialog()

        # Set up the canvas for a 32x32 grid
        self.pixel_size = 20  # Size of each "pixel"
        self.grid_size = 32  # Grid is now 32x32
        self.canvas_size = self.grid_size * self.pixel_size  # 32 pixels * 20 px size = 640px canvas
        self.canvas = tk.Canvas(window, width=self.canvas_size, height=self.canvas_size, bg="black")
        self.canvas.pack()

        # Draw the grid of "pixels"
        self.pixels = []
        for row in range(self.grid_size):
            row_pixels = []
            for col in range(self.grid_size):
                x1 = col * self.pixel_size
                y1 = row * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size

                # Initially set all pixels to gray
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="")
                row_pixels.append(rect)
            self.pixels.append(row_pixels)

        # Initialize the worm's position and direction
        self.reset_worm()

        # Initialize the green pixel's position
        self.green_pixel_row = -1
        self.green_pixel_col = -1
        self.spawn_green_pixel()

        # Initialize the score
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=('Helvetica', 12))

        # Set up keyboard bindings for arrow keys
        self.window.bind("<a>", self.move_left)
        self.window.bind("<d>", self.move_right)
        self.window.bind("<w>", self.move_up)
        self.window.bind("<s>", self.move_down)

        # Start the animation loop
        self.move_and_blink()

    def show_welcome_dialog(self):
        """Show a welcome dialog to the player."""
        welcome_message = (
            "Welcome to Worm Game (Early Alpha) v0.1.05!\n\n"
            "Use arrow keys to control the worm.\n"
            "Avoid the walls and collect the food.\n\n"
            "Press OK to start the game."
        )
        messagebox.showinfo("Welcome to Worm Game!", welcome_message)

    def move_left(self, event):
        self.direction_row, self.direction_col = 0, -1

    def move_right(self, event):
        self.direction_row, self.direction_col = 0, 1

    def move_up(self, event):
        self.direction_row, self.direction_col = -1, 0

    def move_down(self, event):
        self.direction_row, self.direction_col = 1, 0

    def reset_worm(self):
        """Reset the worm's position and stop movement."""
        self.pixel_row = self.grid_size // 2
        self.pixel_col = self.grid_size // 2
        self.direction_row = 0
        self.direction_col = 0

        # Redraw the worm in the middle
        self.canvas.itemconfig(self.pixels[self.pixel_row][self.pixel_col], fill="yellow")

    def spawn_green_pixel(self):
        """Randomly place the green pixel on the grid."""
        # Clear the old green pixel
        if self.green_pixel_row != -1 and self.green_pixel_col != -1:
            self.canvas.itemconfig(self.pixels[self.green_pixel_row][self.green_pixel_col], fill="gray")

        # Spawn a new green pixel
        while True:
            self.green_pixel_row = random.randint(0, self.grid_size - 1)
            self.green_pixel_col = random.randint(0, self.grid_size - 1)
            if self.green_pixel_row != self.pixel_row or self.green_pixel_col != self.pixel_col:
                break

        self.canvas.itemconfig(self.pixels[self.green_pixel_row][self.green_pixel_col], fill="green")

    def move_and_blink(self):
        # Turn off the previous worm (yellow pixel)
        self.canvas.itemconfig(self.pixels[self.pixel_row][self.pixel_col], fill="gray")

        # Update the position of the worm
        next_row = self.pixel_row + self.direction_row
        next_col = self.pixel_col + self.direction_col

        # Check for collision with walls
        if next_row < 0 or next_row >= self.grid_size or next_col < 0 or next_col >= self.grid_size:
            self.reset_game()  # Reset game on collision
            return

        # Update the worm's position
        self.pixel_row = next_row
        self.pixel_col = next_col

        # Check if the worm has eaten the green pixel
        if self.pixel_row == self.green_pixel_row and self.pixel_col == self.green_pixel_col:
            self.score += 1
            self.update_scoreboard()
            self.spawn_green_pixel()

        # Turn on the worm (yellow pixel)
        self.canvas.itemconfig(self.pixels[self.pixel_row][self.pixel_col], fill="yellow")

        # Schedule the next update
        self.window.after(200, self.move_and_blink)

    def update_scoreboard(self):
        """Update the score displayed on the canvas."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def reset_game(self):
        """Reset the game after death."""
        play_again = messagebox.askyesno("Game Over", f"You scored {self.score}!\nDo you want to play again?")
        if play_again:
            # Reset the game
            self.canvas.itemconfig(self.pixels[self.pixel_row][self.pixel_col], fill="gray")
            self.score = 0  # Reset score
            self.update_scoreboard()
            self.reset_worm()  # Reset worm's position
            self.spawn_green_pixel()  # Spawn a new green pixel
            self.window.after(200, self.move_and_blink)  # Restart the game loop
        else:
            self.window.destroy()  # Close the application


if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingPixelApp(root)
    root.mainloop()
