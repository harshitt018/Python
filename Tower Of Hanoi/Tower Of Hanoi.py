import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkfont

class TowerOfHanoiGUI:
    def _init_(self, root, num_disks):
        self.root = root
        self.num_disks = num_disks
        self.towers = [list(reversed(range(1, num_disks + 1))), [], []]
        self.move_count = 0
        self.create_widgets()
        self.draw_towers()
        self.solution_steps = []
        self.current_step = 0

    def create_widgets(self):
        self.root.configure(bg='#f0f0f0')
        
        # Title
        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        title_label = tk.Label(self.root, text="Tower of Hanoi", font=title_font, bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Canvas for towers
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white', borderwidth=2, relief="sunken")
        self.canvas.pack(pady=10)
        
        # Frame for buttons and entry fields
        self.buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.buttons_frame.pack(pady=10)
        
        # Move button
        self.move_button = tk.Button(self.buttons_frame, text="Move", command=self.move_disk, bg='#4CAF50', fg='white', font=("Arial", 12, "bold"))
        self.move_button.grid(row=0, column=0, padx=5)
        
        # Solve button
        self.solution_button = tk.Button(self.buttons_frame, text="Solve", command=self.solve_puzzle, bg='#2196F3', fg='white', font=("Arial", 12, "bold"))
        self.solution_button.grid(row=0, column=1, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_puzzle, bg='#f44336', fg='white', font=("Arial", 12, "bold"))
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Move counter
        self.move_counter_label = tk.Label(self.buttons_frame, text="Moves: 0", font=("Arial", 12), bg='#f0f0f0')
        self.move_counter_label.grid(row=0, column=3, padx=5)

        # Input fields for rod numbers
        self.from_rod_label = tk.Label(self.buttons_frame, text="From Rod:", bg='#f0f0f0')
        self.from_rod_label.grid(row=1, column=0, padx=5)
        self.from_rod_entry = tk.Entry(self.buttons_frame, font=("Arial", 12))
        self.from_rod_entry.grid(row=1, column=1, padx=5)
        
        self.to_rod_label = tk.Label(self.buttons_frame, text="To Rod:", bg='#f0f0f0')
        self.to_rod_label.grid(row=1, column=2, padx=5)
        self.to_rod_entry = tk.Entry(self.buttons_frame, font=("Arial", 12))
        self.to_rod_entry.grid(row=1, column=3, padx=5)

    def draw_towers(self):
        self.canvas.delete("all")
        for i in range(3):
            self.canvas.create_line(100 + i * 200, 300, 100 + i * 200, 100, width=4, fill='black')
            for j, disk in enumerate(self.towers[i]):
                disk_color = self.get_disk_color(disk)
                self.canvas.create_rectangle(
                    100 + i * 200 - disk * 10, 280 - j * 20,
                    100 + i * 200 + disk * 10, 300 - j * 20,
                    fill=disk_color, outline='black', width=2
                )

    def get_disk_color(self, disk):
        # Use a color gradient
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
        return colors[(disk - 1) % len(colors)]

    def move_disk(self):
        try:
            from_rod = int(self.from_rod_entry.get()) - 1
            to_rod = int(self.to_rod_entry.get()) - 1
            if from_rod < 0 or from_rod > 2 or to_rod < 0 or to_rod > 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid rod numbers (1, 2, or 3).")
            return

        if len(self.towers[from_rod]) == 0:
            messagebox.showerror("Invalid move", f"Rod {from_rod + 1} is empty.")
            return

        if len(self.towers[to_rod]) == 0 or self.towers[from_rod][-1] < self.towers[to_rod][-1]:
            self.towers[to_rod].append(self.towers[from_rod].pop())
            self.move_count += 1
            self.update_move_counter()
            self.draw_towers()
            if self.is_solved():
                messagebox.showinfo("Congratulations", "You solved the Tower of Hanoi puzzle!")
        else:
            messagebox.showerror("Invalid move", f"Cannot move disk from Rod {from_rod + 1} to Rod {to_rod + 1}.")

    def update_move_counter(self):
        self.move_counter_label.config(text=f"Moves: {self.move_count}")

    def is_solved(self):
        return len(self.towers[2]) == self.num_disks

    def solve_puzzle(self):
        self.solution_steps = []
        self.towers = [list(reversed(range(1, self.num_disks + 1))), [], []]
        self.move_count = 0
        self.update_move_counter()
        self.toh(self.num_disks, 0, 1, 2)
        self.current_step = 0
        self.animate_solution()

    def toh(self, disks, source, aux, target):
        if disks == 1:
            self.solution_steps.append((source, target))
        else:
            self.toh(disks - 1, source, target, aux)
            self.solution_steps.append((source, target))
            self.toh(disks - 1, aux, source, target)

    def animate_solution(self):
        if self.current_step < len(self.solution_steps):
            from_rod, to_rod = self.solution_steps[self.current_step]
            if len(self.towers[from_rod]) > 0:
                disk = self.towers[from_rod][-1]
                self.towers[to_rod].append(self.towers[from_rod].pop())
                self.move_count += 1
                self.update_move_counter()
                self.draw_towers()
            self.current_step += 1
            self.root.after(1000, self.animate_solution)

    def reset_puzzle(self):
        self.towers = [list(reversed(range(1, self.num_disks + 1))), [], []]
        self.move_count = 0
        self.update_move_counter()
        self.draw_towers()
        self.solution_steps = []
        self.current_step = 0

def main():
    root = tk.Tk()
    root.title("Tower of Hanoi")
    num_disks = int(simpledialog.askstring("Input", "Enter the number of disks:"))
    app = TowerOfHanoiGUI(root, num_disks)
    root.mainloop()

if __name__ == "__main__":
    main()