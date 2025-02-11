import random, os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from map_generator import MapGenerator 

class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.id = player_id  # Unique identifier for the player

    def __str__(self):
        return f"{self.name}"
    
class GridContender:
    """
    Logic:
    - Players capture grids within a time limit.
    - If two players land on the same grid, game over.
    - The last player on a grid owns it.
    """
    def __init__(self, root, map_width=12, map_height=12, grid_size=50, round_time=5):
        self.root = root
        self.map_height, self.map_width, self.grid_size = map_height, map_width, grid_size
        self.round_time, self.countdown = round_time, round_time
        self.grid_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.game_over = False
        self.winner = None
        self.over_condition = None
        self.generate_map_window = None
        
        # Tkinter window setup
        window_padding_x = 100 
        window_padding_y = 200
        self.canvas_height, self.canvas_width = self.map_height * self.grid_size, self.map_width * self.grid_size
        self.root.geometry(f"{self.canvas_width + window_padding_x}x{self.canvas_height + window_padding_y}")  

        self.create_ui()
        self.root.bind("<KeyPress>", self.handle_keypress)

    def create_ui(self):
        """Creates the GUI elements"""

        # Button to open the map generator
        self.open_map_generator_button = tk.Button(self.root, text="Open Map Editor", command=self.open_map_generator)
        self.open_map_generator_button.pack(pady=5) 

        self.import_map_button = tk.Button(self.root, text="Load Existing Map", command = self.import_map_from_file)
        self.import_map_button.pack()

         # Create a container frame for all three labels
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)  # Stretch across the window

        # Player 1 (Left)
        container_p1 = tk.Frame(top_frame)
        container_p1.pack(side="left", padx=10)

        color_block_p1 = tk.Frame(container_p1, width=20, height=20, bg="red")
        color_block_p1.pack(side="left")

        player1_label = tk.Label(container_p1, text="Player 1", font=("Arial", 14))
        player1_label.pack(side="left")

        # Timer (Center)
        self.timer_label = tk.Label(top_frame, text=f"Round time: {self.countdown}s", font=("Arial", 14))
        self.timer_label.pack(side="left", expand=True)  # Expands to center it

        # Player 2 (Right)
        container_p2 = tk.Frame(top_frame)
        container_p2.pack(side="right", padx=10)

        color_block_p2 = tk.Frame(container_p2, width=20, height=20, bg="blue")
        color_block_p2.pack(side="right")

        player2_label = tk.Label(container_p2, text="Player 2", font=("Arial", 14))
        player2_label.pack(side="left")

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack(expand=True, anchor="center")

        # Load image
        cwd = os.getcwd()
        image_path = cwd + "/background.jpg"  # Change this to your image path
        original_image = Image.open(image_path)
        resized_image = original_image.resize((self.canvas_width, self.canvas_height))  # Resize to fit canvas
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Add image to canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)  # Place at top-left

        self.rule_label = tk.Label(self.root, text="Use WASD for Player1, IJKL for Player2", font=("Arial", 14))
        self.rule_label.pack()

        self.new_game_button = tk.Button(self.root, text="Start game with default map", command=self.start_new_game)
        self.new_game_button.pack(pady=10)
    
    def open_map_generator(self):
        """Opens the map generator in a new window."""
        map_window = tk.Toplevel(self.root)  # Create a new window
        map_window.title("Map Generator")
        self.generate_map_window = map_window
        # Create an instance of MapGenerator inside the new window
        self.map_generator = MapGenerator(map_window, self.grid_map, self.map_width, self.map_height)
        
        # Add a button to save and load the map
        save_button = tk.Button(map_window, text="Save & Load Map", command=self.load_generated_map)
        save_button.pack(pady=10)

    def load_generated_map(self):
        """Loads the generated map from the MapGenerator instance into GridContender."""
        self.grid_map = self.map_generator.grid_map  # Copy the generated map
        self.draw_map()  # Redraw the map in the main game
        # messagebox.showinfo("Success", "Generated map loaded into the game!")
        self.new_game_button.config(text="Start with the new map")
        self.generate_map_window.destroy()
     

    def import_map_from_file(self):
        """Load a map grid from a file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "r") as file:
                    loaded_map = [list(map(int, line.strip().split(","))) for line in file]

                # Validate map dimensions
                if len(loaded_map) == self.map_height and all(len(row) == self.map_width for row in loaded_map):
                    self.grid_map = loaded_map  # Update the map
                    self.draw_map()
                    self.new_game_button.config(text="Start with the new map")

                    print(f"Map imported from {file_path}")
                else:
                    print("Error: The map dimensions do not match the current grid size.")

            except Exception as e:
                print(f"Error loading map: {e}")


    def reset_game_params(self):
        """Reset game state without reinitializing everything."""
        self.countdown = self.round_time
        self.game_over = False
        self.winner = None
        self.reset_map()
        self.update_timer()
        self.over_condition = None

    def reset_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.grid_map[x][y] != -1:
                    self.grid_map[x][y] = 0

    def reset_players(self): 
        """Initialize players and assign starting positions."""
        self.player1 = Player("p1", 1)
        self.player2 = Player("p2", 2)
        self.player_positions = {}

        # Set unique starting positions for both players
        self.player_positions[self.player1] = self.get_random_position()
        self.player_positions[self.player2] = self.get_random_position(avoid=[self.player_positions[self.player1]])

        # Mark players on the map
        self.grid_map[self.player_positions[self.player1][0]][self.player_positions[self.player1][1]] = 1
        self.grid_map[self.player_positions[self.player2][0]][self.player_positions[self.player2][1]] = 2

    def get_random_position(self, avoid=None):
        """Returns a random valid position, avoiding blocked positions and specified avoid list."""
        avoid = avoid or []
        while True:
            x, y = random.randint(0, self.map_width - 1), random.randint(0, self.map_height - 1)
            if self.grid_map[x][y] != -1 and (x, y) not in avoid:
                return x, y

    def start_new_game(self):
        """Resets the game and ensures players don't start at the same position."""
        self.reset_game_params()
        self.reset_players()
        
        # Draw the map, blocked cells, and players
        self.draw_map()
        self.draw_players()

    def update_timer(self):
        """Updates the countdown timer and checks if time is up."""
        if self.countdown > 0 and not self.game_over:
            self.timer_label.config(text=f"Time left: {self.countdown}s")
            self.countdown -= 1
            self.new_game_button.config(state=tk.DISABLED)
            self.import_map_button.config(state=tk.DISABLED)
            self.open_map_generator_button.config(state=tk.DISABLED)
            self.root.after(1000, self.update_timer)  # Call update_timer again after 1 sec
        else:
            self.over_condition = 'time'
            self.end_game()

    def end_game(self):
        """Ends the game when the timer reaches zero."""
        if self.game_over:
            return
        self.game_over = True
        self.set_winner()
        # if self.over_condition == 'time':
        #     messagebox.showinfo("Game Over", f"Time's up! Game Over!")
        # elif self.over_condition == 'collision':
        #     messagebox.showinfo("Game Over", f"Both players collided! Game Over!")
        if self.winner is None:
            self.timer_label.config(text="DRAW")
        else:
            self.timer_label.config(text=f"{self.winner} WIN!")
        self.new_game_button.config(text="Start new game", state=tk.NORMAL)
        self.import_map_button.config(state=tk.NORMAL)
        self.open_map_generator_button.config(state=tk.NORMAL)


    def draw_rectangle(self, x, y, fill_color, outline_color):
        self.canvas.create_rectangle(
            x * self.grid_size, y * self.grid_size,
            (x + 1) * self.grid_size, (y + 1) * self.grid_size,
            fill=fill_color, outline=outline_color
        )

    def draw_map(self):
        """Draws the grid and blocked positions."""
        for y in range(self.map_height):
            for x in range(self.map_width):
                # Check if the current position is blocked
                # if self.grid_map[x][y] == -1:
                #     self.draw_rectangle(x, y, "gray", "black")
                # elif self.grid_map[x][y] == 1:
                #     self.draw_rectangle(x, y, "#F07167", "black")
                # elif self.grid_map[x][y] == 2:
                #     self.draw_rectangle(x, y, "#0081A7", "black")
                # else:
                #     self.draw_rectangle(x, y, "white", "black")

                match self.grid_map[x][y]:
                    case -1:
                        self.draw_rectangle(x, y, "gray", "black")
                    case 1:
                        self.draw_rectangle(x, y, "#F07167", "black")
                    case 2:
                        self.draw_rectangle(x, y, "#0081A7", "black")
                    case _:
                        self.draw_rectangle(x, y, "white", "black")

    def draw_players(self):
        """Draws the players on the canvas."""
        for player, (x, y) in self.player_positions.items():
            color = "red" if player == self.player1 else "blue"
            self.draw_rectangle(x, y, color, 'black')

    def handle_keypress(self, event):
        """Handles player movement and checks for game over."""
        if self.game_over:
            return  # Ignore input if game is over

        key = event.keysym
        moves = {
            "w": (self.player1, 0, -1), "a": (self.player1, -1, 0),
            "s": (self.player1, 0, 1), "d": (self.player1, 1, 0),
            "i": (self.player2, 0, -1), "j": (self.player2, -1, 0),
            "k": (self.player2, 0, 1), "l": (self.player2, 1, 0)
        }

        if key in moves:
            player, dx, dy = moves[key]
            x, y = self.player_positions[player]
            new_x, new_y = x + dx, y + dy

            # Ensure movement is within bounds
            if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
                # Ensure the cell is not blocked
                if self.grid_map[new_x][new_y] != -1:
                    self.player_positions[player] = (new_x, new_y)

                    # Check collision
                    if self.player_positions[self.player1] == self.player_positions[self.player2]:
                        self.over_condition = 'collision'
                        self.end_game()
                        return
                    self.grid_map[new_x][new_y] = 1 if player == self.player1 else 2
                    self.draw_map()
                    self.draw_players()

    def set_winner(self):
        flag = 0
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.grid_map[x][y] == 1:
                    flag += 1
                elif self.grid_map[x][y] == 2:
                    flag -= 1

        if flag > 0:
            self.winner = self.player1
        elif flag < 0:
            self.winner = self.player2

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GridContender")
    root.resizable(width=False, height=False)
    game = GridContender(root)
    root.mainloop()


