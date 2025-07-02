import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe: User vs Computer")
        self.window.configure(bg="black")
        self.difficulty = None
        self.grid_size = 3
        self.board = []
        self.current_player = "User"
        self.bg_colors = ["#1a1a1a", "#2a2a2a", "#1a1a1a"]
        self.bg_index = 0
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_window()

        self.animate_background()

        title = tk.Label(self.window, text="Welcome to Tic Tac Toe", font=("Arial", 28, "bold"), fg="white", bg=self.window["bg"])
        title.pack(pady=50)

        anim_label = tk.Label(self.window, text="Choose your difficulty", font=("Arial", 16), fg="white", bg=self.window["bg"])
        anim_label.pack(pady=20)
        self.blink_label(anim_label)

        tk.Button(self.window, text="Easy", font=("Arial", 16), command=lambda: self.start_game("Easy"), width=20).pack(pady=10)
        tk.Button(self.window, text="Intermediate", font=("Arial", 16), command=lambda: self.start_game("Intermediate"), width=20).pack(pady=10)
        tk.Button(self.window, text="Hard", font=("Arial", 16), command=lambda: self.start_game("Hard"), width=20).pack(pady=10)

    def animate_background(self):
        self.bg_index = (self.bg_index + 1) % len(self.bg_colors)
        self.window.configure(bg=self.bg_colors[self.bg_index])
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.bg_colors[self.bg_index])
        self.window.after(1000, self.animate_background)

    def blink_label(self, label):
        def toggle():
            current = label.cget("fg")
            label.config(fg="black" if current == "white" else "white")
            self.window.after(500, toggle)
        toggle()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.grid_size = 3 if difficulty == "Easy" else (4 if difficulty == "Intermediate" else 5)
        self.clear_window()

        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.current_player = "User"

        top_frame = tk.Frame(self.window, bg="black")
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="Start", font=("Arial", 12), command=self.display_start_message).pack(side="left", padx=5)
        tk.Button(top_frame, text="Pause", font=("Arial", 12), command=self.pause_game).pack(side="left", padx=5)
        tk.Button(top_frame, text="Restart", font=("Arial", 12), command=self.create_start_screen).pack(side="left", padx=5)

        board_frame = tk.Frame(self.window, bg="black")
        board_frame.pack()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                btn = tk.Button(board_frame, text="", font=("Arial", 24, "bold"), height=2, width=4,
                                bg="lightgray", fg="black", activebackground="white",
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.board[i][j] = btn

    def display_start_message(self):
        messagebox.showinfo("Start", f"Game Started - Difficulty: {self.difficulty}")

    def pause_game(self):
        messagebox.showinfo("Pause", "Game is paused")

    def on_click(self, row, col):
        if self.board[row][col]["text"] == "" and self.current_player == "User":
            self.board[row][col]["text"] = "X"
            self.board[row][col]["fg"] = "blue"
            if self.check_winner("X"):
                self.highlight_winner("X")
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.create_start_screen()
                return
            else:
                self.current_player = "Computer"
                self.window.after(500, self.computer_move)

    def computer_move(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.board[i][j]["text"] == ""]
        if not empty_cells:
            return

        if self.difficulty == "Hard":
            move = self.find_best_move("O") or random.choice(empty_cells)
        elif self.difficulty == "Intermediate":
            move = self.find_best_move("O")
            if not move:
                move = random.choice(empty_cells)
        else:
            move = random.choice(empty_cells)

        row, col = move
        self.board[row][col]["text"] = "O"
        self.board[row][col]["fg"] = "red"

        if self.check_winner("O"):
            self.highlight_winner("O")
            return
        elif self.is_draw():
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.create_start_screen()
            return
        else:
            self.current_player = "User"

    def find_best_move(self, player):
        opponent = "X" if player == "O" else "O"
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j]["text"] == "":
                    self.board[i][j]["text"] = player
                    if self.check_winner(player):
                        self.board[i][j]["text"] = ""
                        return (i, j)
                    self.board[i][j]["text"] = ""

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j]["text"] == "":
                    self.board[i][j]["text"] = opponent
                    if self.check_winner(opponent):
                        self.board[i][j]["text"] = ""
                        return (i, j)
                    self.board[i][j]["text"] = ""
        return None

    def check_winner(self, player):
        for i in range(self.grid_size):
            if all(self.board[i][j]["text"] == player for j in range(self.grid_size)):
                return [(i, j) for j in range(self.grid_size)]
            if all(self.board[j][i]["text"] == player for j in range(self.grid_size)):
                return [(j, i) for j in range(self.grid_size)]

        if all(self.board[i][i]["text"] == player for i in range(self.grid_size)):
            return [(i, i) for i in range(self.grid_size)]

        if all(self.board[i][self.grid_size - 1 - i]["text"] == player for i in range(self.grid_size)):
            return [(i, self.grid_size - 1 - i) for i in range(self.grid_size)]

        return None

    def highlight_winner(self, player):
        winning_cells = self.check_winner(player)
        if winning_cells:
            for row, col in winning_cells:
                self.board[row][col].config(bg="yellow")
            messagebox.showinfo("Game Over", f"{'User' if player == 'X' else 'Computer'} wins!")
            self.create_start_screen()

    def is_draw(self):
        return all(self.board[i][j]["text"] != "" for i in range(self.grid_size) for j in range(self.grid_size))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
