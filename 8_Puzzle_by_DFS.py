import tkinter as tk
from tkinter import messagebox
import time

class EightPuzzleDFS:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle - DFS")
        self.root.geometry("400x500")
        
        self.start_state = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
        self.goal_state = ((1, 2, 3), (8, 0, 4), (7, 6, 5))
        
        self.current_state = list(list(row) for row in self.start_state)
        self.solution_path = []
        self.step_index = 0
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_frame = tk.Frame(self.root, bg="#333", bd=5)
        self.grid_frame.pack(pady=30)
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.grid_frame, text="", font=("Arial", 24, "bold"), 
                                width=4, height=2, bd=2, bg="#fff")
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn
                
        self.update_grid(self.current_state)
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.solve_btn = tk.Button(control_frame, text="Tìm đường đi (DFS)", font=("Arial", 12, "bold"), 
                                   bg="#ff9999", command=self.solve)
        self.solve_btn.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(self.root, text="Bấm nút để bắt đầu giải", font=("Arial", 12, "italic"))
        self.status_label.pack(pady=10)

    def update_grid(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val == 0:
                    self.buttons[i][j].config(text="", bg="#777")
                else:
                    self.buttons[i][j].config(text=str(val), bg="#fff")

    def get_neighbors(self, state):
        neighbors = []
        r, c = -1, -1
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    r, c = i, j
                    break
        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = list(list(row) for row in state)
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                neighbors.append(tuple(tuple(row) for row in new_state))
        return neighbors

    def solve(self):
        self.solve_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Đang tìm kiếm bằng DFS...")
        self.root.update()
        
        
        stack = [(self.start_state, [], 0)]
        visited = {self.start_state: 0} 
        found = False
        max_depth = 40
        
        while stack:
            current, path, depth = stack.pop()
            
            if current == self.goal_state:
                self.solution_path = path + [current]
                found = True
                break
                
            if depth >= max_depth:
                continue
                
            for neighbor in self.get_neighbors(current):
              
                if neighbor not in visited or depth + 1 < visited[neighbor]:
                    visited[neighbor] = depth + 1
                    stack.append((neighbor, path + [current], depth + 1))
                    
        if found:
            self.status_label.config(text=f"Tìm thấy bằng DFS! Tổng: {len(self.solution_path)-1} bước.")
            self.animate_solution()
        else:
            self.status_label.config(text=f"Không tìm thấy đường đi trong giới hạn {max_depth} tầng.")
            self.solve_btn.config(state=tk.NORMAL)

    def animate_solution(self):
        if self.step_index < len(self.solution_path):
            self.update_grid(self.solution_path[self.step_index])
            self.status_label.config(text=f"Bước: {self.step_index} / {len(self.solution_path)-1}")
            self.step_index += 1
            self.root.after(500, self.animate_solution)
        else:
            messagebox.showinfo("Thành công", "Giải xong trò chơi bằng DFS!")
            self.solve_btn.config(state=tk.NORMAL)
            self.step_index = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleDFS(root)
    root.mainloop()