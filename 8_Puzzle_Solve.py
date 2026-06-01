import tkinter as tk
from tkinter import messagebox
from collections import deque
import time
import threading
import heapq
import random

class EightPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle")
        self.root.geometry("500x700") 
        self.root.resizable(False, False)
        
        self.goal_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)
        
        self.start_state = ()
        self.current_state = []
        self.is_solving = False
        
        self.setup_ui()
        self.shuffle_puzzle()

    def setup_ui(self):
        title_label = tk.Label(self.root, text="8-PUZZLE SOLVER", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Khung hiển thị ô 3x3
        self.grid_frame = tk.Frame(self.root, bg="gray", bd=2)
        self.grid_frame.pack(pady=5)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Label(self.grid_frame, text="", font=("Arial", 24, "bold"), 
                           width=5, height=2, bd=1, relief="solid")
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)
        
        # Ô nhập/Hiển thị trạng thái
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)
        tk.Label(input_frame, text="Trạng thái hiện tại (9 số từ 0-8):", font=("Arial", 9)).pack()
        self.state_entry = tk.Entry(input_frame, font=("Arial", 11), width=30, justify='center')
        self.state_entry.pack(pady=5)

        # Điều khiển cấu hình ma trận
        config_frame = tk.Frame(self.root)
        config_frame.pack(pady=5)

        self.btn_set = tk.Button(config_frame, text="Áp Dụng Dãy Số Nhập", font=("Arial", 10, "bold"), 
                                   command=self.set_custom_state, bg="#2196F3", fg="white", width=20)
        self.btn_set.grid(row=0, column=0, padx=5)

        self.btn_shuffle = tk.Button(config_frame, text="Trộn", font=("Arial", 10, "bold"), 
                                   command=self.shuffle_puzzle, bg="#9c27b0", fg="white", width=10)
        self.btn_shuffle.grid(row=0, column=1, padx=5)
        
        # Các nút thuật toán
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Dòng thuật toán mù & cơ bản
        self.bfs_btn = tk.Button(control_frame, text="BFS", font=("Arial", 10, "bold"), 
                                 bg="#99ccff", width=8, command=lambda: self.start_solving_thread("BFS"))
        self.bfs_btn.grid(row=0, column=0, padx=3, pady=3)
        
        self.dfs_btn = tk.Button(control_frame, text="DFS", font=("Arial", 10, "bold"), 
                                 bg="#ff9999", width=8, command=lambda: self.start_solving_thread("DFS"))
        self.dfs_btn.grid(row=0, column=1, padx=3, pady=3)
        
        self.IDS_btn = tk.Button(control_frame, text="IDS", font=("Arial", 10, "bold"), 
                                   bg="#ffcc99", width=8, command=lambda: self.start_solving_thread("IDS"))
        self.IDS_btn.grid(row=0, column=2, padx=3, pady=3)

        self.ucs_btn = tk.Button(control_frame, text="UCS", font=("Arial", 10, "bold"), 
                                   bg="#c2f0c2", width=8, command=lambda: self.start_solving_thread("UCS"))
        self.ucs_btn.grid(row=0, column=3, padx=3, pady=3)

        self.astar_btn = tk.Button(control_frame, text="A*", font=("Arial", 10, "bold"), 
                                   bg="#e6b3ff", width=8, command=lambda: self.start_solving_thread("A*"))
        self.astar_btn.grid(row=0, column=4, padx=3, pady=3)
        
        self.idastar_btn = tk.Button(control_frame, text="IDA*", font=("Arial", 10, "bold"), 
                                   bg="#d9b3ff", width=12, command=lambda: self.start_solving_thread("IDA*"))
        self.idastar_btn.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

        self.shc_btn = tk.Button(control_frame, text="Leo đồi đơn giản", font=("Arial", 10, "bold"), 
                                   bg="#ffff99", width=15, command=lambda: self.start_solving_thread("Leo đồi đơn giản"))
        self.shc_btn.grid(row=1, column=2, padx=3, pady=3)

        self.sahc_btn = tk.Button(control_frame, text="Leo đồi dốc nhất", font=("Arial", 10, "bold"), 
                                   bg="#ffe680", width=15, command=lambda: self.start_solving_thread("Leo đồi dốc nhất"))
        self.sahc_btn.grid(row=1, column=3, columnspan=2, padx=3, pady=3)
        
        # Hiển thị trạng thái xử lý
        self.status_label = tk.Label(self.root, text="Hệ thống đã tự động trộn ma trận mẫu!", font=("Arial", 11, "italic"), fg="blue", wraplength=400)
        self.status_label.pack(pady=10)

    def update_grid(self):
        for i in range(9):
            val = self.current_state[i]
            if val == 0:
                self.buttons[i].config(text="", bg="#e0e0e0") 
            else:
                self.buttons[i].config(text=str(val), bg="#ffffff")

    def shuffle_puzzle(self):
        if self.is_solving: return
        
        state = list(self.goal_state)
        shuffle_steps = random.randint(25, 35)
        for _ in range(shuffle_steps):
            neighbors = self.get_moves(tuple(state))
            if neighbors:
                state = list(random.choice(neighbors))
        
        self.start_state = tuple(state)
        self.current_state = list(state)
        
        self.state_entry.delete(0, tk.END)
        self.state_entry.insert(0, " ".join(map(str, state)))
        
        self.update_grid()
        self.status_label.config(text=f"Đã tự động trộn ngẫu nhiên ({shuffle_steps} bước cách trạng thái mục tiêu)!", fg="purple")

    def set_custom_state(self):
        if self.is_solving: return
        try:
            val_str = self.state_entry.get().strip().split()
            vals = [int(x) for x in val_str]
            if len(vals) != 9 or set(vals) != set(range(9)):
                raise ValueError
            self.start_state = tuple(vals)
            self.current_state = vals
            self.update_grid()
            self.status_label.config(text="Đã áp dụng trạng thái bạn nhập!", fg="green")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng 9 số từ 0 đến 8 không trùng lặp.")

    def set_buttons_state(self, state_mode):
        self.bfs_btn.config(state=state_mode)
        self.dfs_btn.config(state=state_mode)
        self.IDS_btn.config(state=state_mode)
        self.ucs_btn.config(state=state_mode)
        self.astar_btn.config(state=state_mode)
        self.idastar_btn.config(state=state_mode)
        self.shc_btn.config(state=state_mode)
        self.sahc_btn.config(state=state_mode)
        self.btn_set.config(state=state_mode)
        self.btn_shuffle.config(state=state_mode)

    def get_moves(self, state):
        moves = []
        zero_idx = state.index(0)
        r, c = zero_idx // 3, zero_idx % 3
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                next_idx = nr * 3 + nc
                new_state = list(state)
                new_state[zero_idx], new_state[next_idx] = new_state[next_idx], new_state[zero_idx]
                moves.append(tuple(new_state))
        return moves

    # Thuật toán BFS:
    def run_bfs(self):
        queue = deque([(self.start_state, [])])
        visited = {self.start_state}
        while queue:
            current, path = queue.popleft()
            if current == self.goal_state:
                return path + [current]
            for neighbor in self.get_moves(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [current]))
        return None

    # Thuật toán DFS:
    def run_dfs(self):
        stack = [(self.start_state, [], 0)]
        visited = {self.start_state: 0}
        max_depth = 30
        while stack:
            current, path, depth = stack.pop()
            if current == self.goal_state:
                return path + [current]
            if depth >= max_depth:
                continue
            for neighbor in self.get_moves(current):
                if neighbor not in visited or depth + 1 < visited[neighbor]:
                    visited[neighbor] = depth + 1
                    stack.append((neighbor, path + [current], depth + 1))
        return None

    # Thuật toán IDS
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

    def run_ids(self):
        depth = 0
        while depth <= 22:
            self.status_label.config(text=f"IDS đang tìm ở độ sâu: {depth}...", fg="orange")
            visited = set()
            path = self.dls(self.start_state, depth, visited)
            if path is not None:
                return path
            depth += 1
        return None

    # Thuật toán UCS
    def run_ucs(self):
        heap = []
        heapq.heappush(heap, (0, self.start_state, []))
        visited_costs = {self.start_state: 0}
        
        while heap:
            cost, current, path = heapq.heappop(heap)
            if current == self.goal_state:
                return path + [current]
            if cost > visited_costs.get(current, float('inf')):
                continue
            for neighbor in self.get_moves(current):
                new_cost = cost + 1
                if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                    visited_costs[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor, path + [current]))
        return None

    # Hàm Tính toán tổng khoảng cách Manhattan
    def get_manhattan_distance(self, state):
        distance = 0
        for i in range(9):
            val = state[i]
            if val != 0: 
                goal_idx = self.goal_state.index(val)
                curr_r, curr_c = i // 3, i % 3
                goal_r, goal_c = goal_idx // 3, goal_idx % 3
                distance += abs(curr_r - goal_r) + abs(curr_c - goal_c)
        return distance

    # Thuật toán A*
    def run_astar(self):
        heap = []
        h_start = self.get_manhattan_distance(self.start_state)
        heapq.heappush(heap, (h_start, 0, self.start_state, []))
        visited_costs = {self.start_state: 0}
        
        while heap:
            f, g, current, path = heapq.heappop(heap)
            if current == self.goal_state:
                return path + [current]
            if g > visited_costs.get(current, float('inf')):
                continue
            for neighbor in self.get_moves(current):
                new_g = g + 1
                if neighbor not in visited_costs or new_g < visited_costs[neighbor]:
                    visited_costs[neighbor] = new_g
                    h_score = self.get_manhattan_distance(neighbor)
                    f_score = new_g + h_score
                    heapq.heappush(heap, (f_score, new_g, neighbor, path + [current]))
        return None

    # Thuật toán IDA* 
    def run_idastar(self):
        def idastar_search(path, g, threshold):
            current = path[-1]
            f = g + self.get_manhattan_distance(current)
            if f > threshold:
                return f, None
            if current == self.goal_state:
                return f, list(path)
            
            minimum = float('inf')
            for neighbor in self.get_moves(current):
                if neighbor not in path:
                    path.append(neighbor)
                    t, res = idastar_search(path, g + 1, threshold)
                    if res is not None:
                        return t, res
                    if t < minimum:
                        minimum = t
                    path.pop()
            return minimum, None

        threshold = self.get_manhattan_distance(self.start_state)
        path = [self.start_state]
        
        while threshold != float('inf'):
            self.status_label.config(text=f"IDA* đang tìm với ngưỡng f (threshold): {threshold}...", fg="orange")
            t, res = idastar_search(path, 0, threshold)
            if res is not None:
                return res
            if t == float('inf'):
                return None
            threshold = t
        return None

    # Thuật toán Simple Hill Climbing (Leo đồi đơn giản)
    def run_simple_hill_climbing(self):
        current = self.start_state
        path = [current]
        max_steps = 1000  # Giới hạn số bước lặp để tránh loop vô hạn tại cực trị cục bộ
        
        for _ in range(max_steps):
            if current == self.goal_state:
                return path
            
            current_h = self.get_manhattan_distance(current)
            neighbors = self.get_moves(current)
            moved = False
            
            # Khảo sát từng node hàng xóm, thấy ai tốt hơn (h nhỏ hơn) đầu tiên là đi luôn
            for neighbor in neighbors:
                neighbor_h = self.get_manhattan_distance(neighbor)
                if neighbor_h < current_h:
                    current = neighbor
                    path.append(current)
                    moved = True
                    break
            
            # Nếu không tìm thấy node nào tốt hơn node hiện tại -> Bị kẹt
            if not moved:
                break
        return path if current == self.goal_state else None

    # Thuật toán Steepest-Ascent Hill Climbing (Leo đồi dốc nhất)
    def run_steepest_ascent_hill_climbing(self):
        current = self.start_state
        path = [current]
        max_steps = 1000
        
        for _ in range(max_steps):
            if current == self.goal_state:
                return path
            
            current_h = self.get_manhattan_distance(current)
            neighbors = self.get_moves(current)
            
            best_neighbor = None
            best_h = current_h
            
            # Đánh giá TOÀN BỘ node hàng xóm để chọn ra node tối ưu nhất (h nhỏ nhất)
            for neighbor in neighbors:
                neighbor_h = self.get_manhattan_distance(neighbor)
                if neighbor_h < best_h:
                    best_h = neighbor_h
                    best_neighbor = neighbor
            
            # Nếu node hàng xóm tốt nhất vẫn không bằng node hiện tại -> Đã đạt đỉnh cục bộ
            if best_neighbor is not None:
                current = best_neighbor
                path.append(current)
            else:
                break
                
        return path if current == self.goal_state else None


    def start_solving_thread(self, algo):
        if self.is_solving: return
        self.is_solving = True
        self.set_buttons_state(tk.DISABLED)
        self.status_label.config(text=f"Đang giải bằng {algo}...", fg="orange")
        
        thread = threading.Thread(target=self.solve, args=(algo,))
        thread.start()

    def solve(self, algo):
        start_time = time.time()
        
        if algo == "BFS":
            path = self.run_bfs()
        elif algo == "DFS":
            path = self.run_dfs()
        elif algo == "IDS":
            path = self.run_ids()  
        elif algo == "UCS":
            path = self.run_ucs()
        elif algo == "A*":
            path = self.run_astar()
        elif algo == "IDA*":
            path = self.run_idastar()
        elif algo == "Leo đồi đơn giản":
            path = self.run_simple_hill_climbing()
        elif algo == "Leo đồi dốc nhất":
            path = self.run_steepest_ascent_hill_climbing()
            
        end_time = time.time()
        execution_time = end_time - start_time

        if path:
            self.status_label.config(text=f"{algo} thành công! ({execution_time:.3f}s). Đang chạy...", fg="green")
            for state in path:
                self.current_state = list(state)
                self.update_grid()
                time.sleep(0.4)
            
            self.status_label.config(
                text=f"Thuật toán: {algo}\nThời gian xử lý: {execution_time:.4f}s | Số bước: {len(path) - 1}", 
                fg="green"
            )
        else:
            self.status_label.config(text=f"{algo} thất bại!\n(Thuật toán không tìm thấy lời giải hoặc bị kẹt ở trạng thái cực trị cục bộ).", fg="red")
        
        self.is_solving = False
        self.set_buttons_state(tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleApp(root)
    root.mainloop()