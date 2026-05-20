import tkinter as tk
from tkinter import messagebox
import time
import threading

class EightPuzzleIDDFS:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (IDDFS)")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.current_state = list((1, 2, 3, 4, 0, 6, 7, 5, 8))
        
        self.solution_path = []
        self.is_solving = False

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(self.root, text="8-PUZZLE SOLVER (I-DFS)", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        self.grid_frame = tk.Frame(self.root, bg="gray", bd=2)
        self.grid_frame.pack(pady=10)
        self.buttons = []
        for i in range(9):
            btn = tk.Label(self.grid_frame, text="", font=("Arial", 24, "bold"), width=5, height=2, bd=1, relief="solid")
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)
        
        self.update_grid()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Trạng thái (0-8, cách nhau khoảng trắng):", font=("Arial", 10)).pack()
        self.state_entry = tk.Entry(input_frame, font=("Arial", 12), width=25, justify='center')
        self.state_entry.insert(0, "1 2 3 4 0 6 7 5 8")
        self.state_entry.pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.btn_set = tk.Button(btn_frame, text="Đặt Trạng Thái", font=("Arial", 10, "bold"), command=self.set_custom_state, bg="#2196F3", fg="white", width=12)
        self.btn_set.grid(row=0, column=0, padx=5)

        self.btn_solve = tk.Button(btn_frame, text="Giải Bài Toán", font=("Arial", 10, "bold"), command=self.start_solving_thread, bg="#4CAF50", fg="white", width=12)
        self.btn_solve.grid(row=0, column=1, padx=5)

        self.status_label = tk.Label(self.root, text="Sẵn sàng", font=("Arial", 11, "italic"), fg="blue")
        self.status_label.pack(pady=10)

    def update_grid(self):
        for i in range(9):
            val = self.current_state[i]
            if val == 0:
                self.buttons[i].config(text="", bg="#e0e0e0")
            else:
                self.buttons[i].config(text=str(val), bg="#ffffff")

    def set_custom_state(self):
        if self.is_solving: return
        try:
            val_str = self.state_entry.get().strip().split()
            vals = [int(x) for x in val_str]
            if len(vals) != 9 or set(vals) != set(range(9)):
                raise ValueError
            self.current_state = vals
            self.update_grid()
            self.status_label.config(text="Đã đặt trạng thái mới!", fg="green")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng 9 số từ 0 đến 8 không trùng lặp.")

    def get_moves(self, state):
        moves = []
        zero_idx = state.index(0)
        r, c = zero_idx // 3, zero_idx % 3

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                next_idx = nr * 3 + nc
                new_state = list(state)
                new_state[zero_idx], new_state[next_idx] = new_state[next_idx], new_state[zero_idx]
                moves.append(tuple(new_state))
        return moves

    def dls(self, state, depth, visited):
        if state == self.goal_state:
            return [state]
        if depth <= 0:
            return None

        visited.add(state)
        for next_state in self.get_moves(state):
            if next_state not in visited:
                res = self.dls(next_state, depth - 1, visited)
                if res is not None:
                    return [state] + res
        visited.remove(state)
        return None

    def iddfs(self, start_state):
        depth = 0
        while True:
            self.status_label.config(text=f"Đang tìm kiếm ở độ sâu: {depth}...", fg="orange")
            self.root.update()
            
            visited = set()
            path = self.dls(tuple(start_state), depth, visited)
            if path is not None:
                return path
            depth += 1
            if depth > 20: 
                return None

    def start_solving_thread(self):
        if self.is_solving: return
        self.is_solving = True
        self.btn_solve.config(state=tk.DISABLED)
        self.btn_set.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.solve)
        thread.start()

    def solve(self):
        start_time = time.time()
        path = self.iddfs(self.current_state)
        end_time = time.time()

        if path:
            self.status_label.config(text=f"Tìm thấy giải pháp! Đang mô phỏng...", fg="green")
            for state in path:
                self.current_state = list(state)
                self.update_grid()
                time.sleep(0.6)
            
            self.status_label.config(
                text=f"Hoàn thành trong {end_time - start_time:.2f}s!\nSố bước di chuyển: {len(path) - 1}", 
                fg="green"
            )
        else:
            self.status_label.config(text="Không tìm thấy lời giải (hoặc quá sâu > 20 bước).", fg="red")
        
        self.is_solving = False
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_set.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleIDDFS(root)
    root.mainloop()