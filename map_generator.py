import tkinter as tk
from tkinter import filedialog

class MapGenerator:

    def __init__(self, root, map=None, map_width=5, map_height=5):
        self.root = root
        self.grid_size = 50
        self.map_width = map_width
        self.map_height = map_height
        self.grid_map = map or [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        # Tkinter window setup
        self.window_padding_x = 100 
        self.window_padding_y = 120 
        self.canvas_height, self.canvas_width = self.map_height * self.grid_size, self.map_width * self.grid_size
        self.root.geometry(f"{self.canvas_width + self.window_padding_x}x{self.canvas_height + self.window_padding_y}")  

        self.create_ui()
        self.draw_map()

        self.root.bind('<Button-1>', self.reverse_grid_status)

    def reverse_grid_status(self, event):
        if self.canvas != self.root.winfo_containing(event.x_root, event.y_root):
            return  # Ignore clicks outside the canva
        
        select_x = event.x // self.grid_size
        select_y = event.y // self.grid_size
        # Ensure select_x and select_y are within valid map indices
        if 0 <= select_x < self.map_width and 0 <= select_y < self.map_height:
            self.grid_map[select_x][select_y] = -1 if self.grid_map[select_x][select_y] == 0 else 0 # Fix row-column indexing
            self.draw_map()
        

    def create_ui(self):
        
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="green")
        self.canvas.pack(expand=True, anchor="center")

        self.rule_label = tk.Label(self.root, text="Create obstacles by clicking the grid", font=("Arial", 14))
        self.rule_label.pack()

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clean_map)
        self.clear_button.pack(side='left')

        self.cancel_button = tk.Button(self.root, text="Export", command=self.export_map)
        self.cancel_button.pack(side='right')

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
                if self.grid_map[x][y] == -1:
                    self.draw_rectangle(x, y, "gray", "black")
                else:
                    self.draw_rectangle(x, y, "white", "black")

    def clean_map(self):
        self.grid_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.operation_history = []
        self.draw_map()

    def export_map(self):
        """Save the map grid to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All Files", "*.*")]
        )

        if file_path:  # Check if the user selected a file
            with open(file_path, "w") as file:
                for row in self.grid_map:
                    file.write(",".join(map(str, row)) + "\n")  # Save each row as CSV format
            print(f"Map saved to: {file_path}")

if __name__ == '__main__':
    # map_width_limit = 10
    # map_height_limit = 10
    # map_width = min(map_width_limit, input('Please input map width: '))
    # map_height = min(map_height_limit, input('Please input map height: '))
    root = tk.Tk()
    root.title("MapGenerator")
    root.resizable(width=False, height=False)
    game = MapGenerator(root)
    root.mainloop()