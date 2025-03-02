import tkinter as tk
from tkinter import messagebox
from Game_Master_Offline import set_game, set_players, runGame
from RandomPlayer import OurAgent
from game_types import TTT, FIAR, Cassini
from winTesterForK import winTesterForK

class KInARowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("K-in-a-Row Game")
        self.game_type = None
        self.player = None
        self.random_agent = None

        # Game type selection
        self.game_type_var = tk.StringVar(value="TTT")
        self.game_type_label = tk.Label(root, text="Choose Game Type:")
        self.game_type_label.grid(row=0, column=0, padx=10, pady=10)
        self.game_type_menu = tk.OptionMenu(root, self.game_type_var, "TTT", "5-in-a-Row", "Cassini")
        self.game_type_menu.grid(row=0, column=1, padx=10, pady=10)

        # Who goes first selection
        self.first_move_var = tk.StringVar(value="Player")
        self.first_move_label = tk.Label(root, text="Who goes first:")
        self.first_move_label.grid(row=1, column=0, padx=10, pady=10)
        self.first_move_menu = tk.OptionMenu(root, self.first_move_var, "Player", "Random Agent")
        self.first_move_menu.grid(row=1, column=1, padx=10, pady=10)

        # Start game button
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Game board (placeholder)
        self.board_frame = tk.Frame(root)
        self.board_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.board_buttons = []

    def start_game(self):
        # Set the game type based on selection
        game_type = self.game_type_var.get()
        if game_type == "TTT":
            set_game(TTT)
            self.k = 3
        elif game_type == "5-in-a-Row":
            set_game(FIAR)
            self.k = 5
        elif game_type == "Cassini":
            set_game(Cassini)
            self.k = 4

        # Initialize players
        self.player = OurAgent()
        self.random_agent = OurAgent(twin=True)
        set_players(self.player, self.random_agent)

        # Set who goes first
        if self.first_move_var.get() == "Random Agent":
            TTT.initial_state.whose_move = "O"
            FIAR.initial_state.whose_move = "O"
            self.random_agent_move()

        # Start the game
        self.run_game()

    def run_game(self):
        # Clear the board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.board_buttons = []

        # Initialize the board
        board = TTT.initial_state.board if self.game_type_var.get() == "TTT" else FIAR.initial_state.board
        for i in range(len(board)):
            row = []
            for j in range(len(board[i])):
                button = tk.Button(self.board_frame, text=board[i][j], width=5, height=2,
                                   command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.board_buttons.append(row)

    def make_move(self, i, j):
        # Handle player move
        current_state = TTT.initial_state if self.game_type_var.get() == "TTT" else FIAR.initial_state
        if current_state.board[i][j] != ' ':
            messagebox.showwarning("Invalid Move", "This square is already occupied!")
            return

        # Update the board
        self.board_buttons[i][j].config(text=current_state.whose_move)
        current_state.board[i][j] = current_state.whose_move
        current_state.whose_move = 'O' if current_state.whose_move == 'X' else 'X'

        # Check for win
        if self.check_win(current_state, (i, j)):
            messagebox.showinfo("Game Over", f"{current_state.whose_move} wins!")
            self.reset_board()
            return

        # Random agent's turn
        self.random_agent_move()

    def random_agent_move(self):
        # Random agent makes a move
        current_state = TTT.initial_state if self.game_type_var.get() == "TTT" else FIAR.initial_state

        # Ensure the random agent's repeat_count is initialized
        if not hasattr(self.random_agent, 'repeat_count'):
            self.random_agent.repeat_count = 0  # Initialize repeat_count if it doesn't exist

        move_result = self.random_agent.make_move(current_state, "", 1000)
        if move_result is None:
            return

        move, new_state = move_result[0]
        i, j = move
        self.board_buttons[i][j].config(text=new_state.whose_move)
        current_state.board[i][j] = new_state.whose_move
        current_state.whose_move = 'O' if current_state.whose_move == 'X' else 'X'

        # Check for win
        if self.check_win(current_state, (i, j)):
            messagebox.showinfo("Game Over", f"{new_state.whose_move} wins!")
            self.reset_board()

    def check_win(self, state, move):
        # Check for a win using winTesterForK
        result = winTesterForK(state, move, self.k)
        if result != 'No win':
            return True
        return False

    def reset_board(self):
        # Reset the board for a new game
        for row in self.board_buttons:
            for button in row:
                button.config(text=' ')
        if self.game_type_var.get() == "TTT":
            TTT.initial_state.board = [[' ' for _ in range(3)] for _ in range(3)]
            TTT.initial_state.whose_move = "X"
        else:
            FIAR.initial_state.board = [[' ' for _ in range(7)] for _ in range(7)]
            FIAR.initial_state.whose_move = "X"

if __name__ == "__main__":
    root = tk.Tk()
    app = KInARowGUI(root)
    root.mainloop()