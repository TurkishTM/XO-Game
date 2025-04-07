'''
This Projcet got created by: Ali Turkey
This is a one file project contains:
    1- Tic-Tac-Toe Game base and logic
    2- Gui code for the Game
    
'''
import tkinter as tk
from tkinter import messagebox
import os

class TicTacToe:
    def __init__(self):
        self.board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.scores = [0, 0]
        self.current_player = 0

    def is_empty(self, index):
        row, col = divmod(index, 3)
        return self.board[row][col] not in ['X', 'O']

    def replace_char(self, index, char):
        if self.is_empty(index):
            row, col = divmod(index, 3)
            self.board[row][col] = char
            return True
        return False

    def is_win(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True
        return False

    def is_full(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def reset_board(self):
        self.board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

class TicTacToeGUI:
    def __init__(self):
        self.game = TicTacToe()
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.players = ["Player 1", "Player 2"]
        self.colors = ["#FF6F00", "#1976D2"]  # Orange and Dark Blue
        self.symbols = ["X", "O"]
        self.frames = {}
        self.buttons = []
        self.create_frames()
        self.setup_name_page()

        # Load saved game data
        self.load_game_data()

    def create_frames(self):
        for frame_name in ["name", "symbol", "game"]:
            frame = tk.Frame(self.root, bg="#1E1E1E", pady=20, padx=20)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[frame_name] = frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def switch_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")

    def setup_name_page(self):
        frame = self.frames["name"]
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text="Enter Player Names", font=("Helvetica", 20, 'bold'), bg="#1E1E1E", fg="#FFFFFF").pack(pady=10)
        self.p1_name_entry = tk.Entry(frame, font=("Helvetica", 16))
        self.p1_name_entry.pack(pady=5)

        self.p2_name_entry = tk.Entry(frame, font=("Helvetica", 16))
        self.p2_name_entry.pack(pady=5)

        tk.Button(frame, text="Next", font=("Helvetica", 16), command=self.setup_symbol_page, bg="#D84315", fg="white").pack(pady=15)
        self.switch_frame("name")

    def setup_symbol_page(self):
        frame = self.frames["symbol"]
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Use default names if no input is provided
        self.players[0] = self.p1_name_entry.get() if self.p1_name_entry.get().strip() else "Player 1"
        self.players[1] = self.p2_name_entry.get() if self.p2_name_entry.get().strip() else "Player 2"

        player_name = self.players[0]
        tk.Label(frame, text=f"{player_name}, Choose Your Symbol", font=("Helvetica", 20, 'bold'), bg="#1E1E1E", fg="#FFFFFF").pack(pady=10)
        tk.Button(frame, text="X", font=("Helvetica", 16), command=lambda: self.select_symbol("X"), bg="#FF6F00", fg="black").pack(pady=5)
        tk.Button(frame, text="O", font=("Helvetica", 16), command=lambda: self.select_symbol("O"), bg="#1976D2", fg="black").pack(pady=5)
        self.switch_frame("symbol")

    def select_symbol(self, symbol):
        self.symbols = [symbol, "X" if symbol == "O" else "O"]
        self.setup_game_page()

    def setup_game_page(self):
        frame = self.frames["game"]
        for widget in frame.winfo_children():
            widget.destroy()

        score_frame = tk.Frame(frame, bg="#1E1E1E")
        score_frame.pack(fill=tk.X)

        self.score_labels = [
            tk.Label(score_frame, text=f"⚔ {self.players[0]}: {self.game.scores[0]}", font=("Helvetica", 16), bg="#1E1E1E", fg="white"),
            tk.Label(score_frame, text=f"⚔ {self.players[1]}: {self.game.scores[1]}", font=("Helvetica", 16), bg="#1E1E1E", fg="white")
        ]
        self.score_labels[0].pack(side=tk.LEFT, padx=10)
        self.score_labels[1].pack(side=tk.RIGHT, padx=10)

        board_frame = tk.Frame(frame, bg="#2E2E2E", pady=20)
        board_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Helvetica", 30, 'bold'), width=7, height=3,
                                bg="#546E7A", fg="#FFFFFF", command=lambda idx=i * 3 + j: self.make_move(idx))
                btn.grid(row=i, column=j, padx=10, pady=10)
                row.append(btn)
            self.buttons.append(row)
        self.switch_frame("game")

    def make_move(self, index):
        row, col = divmod(index, 3)
        current_symbol = self.symbols[self.game.current_player]

        if self.game.replace_char(index, current_symbol):
            self.buttons[row][col].config(text=current_symbol, state=tk.DISABLED, bg=self.colors[self.game.current_player])
            if self.game.is_win():
                messagebox.showinfo("Game Over", f"{self.players[self.game.current_player]} wins!")
                self.game.scores[self.game.current_player] += 1
                self.update_scores()
                self.ask_play_again()
            elif self.game.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.ask_play_again()
            else:
                self.game.current_player = 1 - self.game.current_player

    def ask_play_again(self):
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            same_names_scores = messagebox.askyesno("Same Names and Scores", "Do you want to play again with the same names and scores?")
            if same_names_scores:
                self.reset_game(keep_names_scores=True)
            else:
                self.reset_game(keep_names_scores=False)
        else:
            self.save_game_data()
            self.root.destroy()

    def reset_game(self, keep_names_scores=True):
        self.game.reset_board()
        self.game.current_player = 0
        if not keep_names_scores:
            self.game.scores = [0, 0]
            self.players = ["Player 1", "Player 2"]
            self.symbols = ["X", "O"]
            self.setup_name_page()
        else:
            self.setup_game_page()

    def update_scores(self):
        self.score_labels[0].config(text=f"⚔ {self.players[0]}: {self.game.scores[0]}")
        self.score_labels[1].config(text=f"⚔ {self.players[1]}: {self.game.scores[1]}")

    def save_game_data(self):
        with open("game_data.txt", "w") as file:
            file.write(f"{self.players[0]},{self.players[1]}\n")
            file.write(f"{self.game.scores[0]},{self.game.scores[1]}\n")

    def load_game_data(self):
        if os.path.exists("game_data.txt"):
            with open("game_data.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    self.players = lines[0].strip().split(",")
                    self.game.scores = list(map(int, lines[1].strip().split(",")))

if __name__ == "__main__":
    app = TicTacToeGUI()
    app.root.mainloop()
