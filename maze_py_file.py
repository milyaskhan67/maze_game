import tkinter as tk
import heapq
import random

# A* Algorithm for shortest path
def a_star_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_list = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        for d in directions:
            next_pos = (current[0] + d[0], current[1] + d[1])
            if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and maze[next_pos[0]][next_pos[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos, goal)
                    heapq.heappush(open_list, (priority, next_pos))
                    came_from[next_pos] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:  # No valid path found
            return []
    path.append(start)
    path.reverse()
    return path

# Enhanced Maze Generation with Multiple Paths
def generate_complex_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]
    start = (1, 1)
    stack = [start]
    maze[start[0]][start[1]] = 0

    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        carved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows - 1 and 0 < ny < cols - 1 and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx // 2][y + dy // 2] = 0
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()

    # Add random extra openings to ensure multiple paths
    for _ in range(rows * cols // 20):  # Adjust density of openings
        x, y = random.randint(1, rows - 2), random.randint(1, cols - 2)
        if maze[x][y] == 1:
            maze[x][y] = 0

    maze[1][1] = 0
    maze[rows - 2][cols - 2] = 0
    return maze

# Maze Game class
class MazeGame:
    def __init__(self, root, rows=21, cols=21, cell_size=30):
        self.rows, self.cols, self.cell_size = rows, cols, cell_size
        self.maze = generate_complex_maze(rows, cols)
        self.player_pos = (1, 1)
        self.goal_pos = (rows - 2, cols - 2)
        self.path = []
        self.showing_path = False

        # Canvas Setup
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack()
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.focus_set()

        # Buttons
        self.toggle_path_button = tk.Button(root, text="Show Path", command=self.toggle_path)
        self.toggle_path_button.pack()

        self.draw_game()

    def draw_game(self):
        self.canvas.delete("all")
        self.draw_maze()
        if self.showing_path:
            self.draw_path()
        self.draw_player()
        self.draw_goal()

    def draw_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "black" if self.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j+1) * self.cell_size, (i+1) * self.cell_size,
                                             fill=color, outline="gray")

    def draw_player(self):
        x, y = self.player_pos
        self.canvas.create_oval(y * self.cell_size + 5, x * self.cell_size + 5,
                                (y+1) * self.cell_size - 5, (x+1) * self.cell_size - 5,
                                fill="blue")

    def draw_goal(self):
        x, y = self.goal_pos
        self.canvas.create_oval(y * self.cell_size + 5, x * self.cell_size + 5,
                                (y+1) * self.cell_size - 5, (x+1) * self.cell_size - 5,
                                fill="red")

    def draw_path(self):
        for x, y in self.path:
            self.canvas.create_rectangle(y * self.cell_size + 10, x * self.cell_size + 10,
                                         (y+1) * self.cell_size - 10, (x+1) * self.cell_size - 10,
                                         fill="yellow", outline="")

    def on_key_press(self, event):
        move = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if event.keysym in move:
            dx, dy = move[event.keysym]
            new_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)
            if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and self.maze[new_pos[0]][new_pos[1]] == 0:
                self.player_pos = new_pos
                self.path = []  # Clear path when moving
                self.showing_path = False
                self.toggle_path_button.config(text="Show Path")
                self.draw_game()

        if self.player_pos == self.goal_pos:
            self.canvas.create_text(self.cols * self.cell_size // 2, self.rows * self.cell_size // 2,
                                    text="You Win!", font=("Arial", 24), fill="green")

    def toggle_path(self):
        if not self.showing_path:
            self.path = a_star_search(self.maze, self.player_pos, self.goal_pos)
            self.showing_path = True
            self.toggle_path_button.config(text="Hide Path")
        else:
            self.path = []
            self.showing_path = False
            self.toggle_path_button.config(text="Show Path")
        self.draw_game()

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Game with Multiple Paths")
    game = MazeGame(root)
    root.mainloop()
