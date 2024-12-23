class Player:
    def __init__(self, name=None, op=None):
        self.name = name
        self.op = op
        self.win_count = 0  # Track the number of wins for the player

    def set_name(self, name):
        self.name = name

    def set_op(self, op):
        self.op = op

    def get_name(self):
        return self.name

    def get_op(self):
        return self.op

    def increment_win_count(self):
        self.win_count += 1

    def reset_win_count(self):
        self.win_count = 0

    def get_win_count(self):
        return self.win_count


class Board:
    def __init__(self):
        self.arr = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']
        ]

    def get_row(self, idx):
        return (idx - 1) // 3

    def get_col(self, idx):
        return (idx - 1) % 3

    def is_empty(self, idx):
        if idx < 1 or idx > 9:
            return False
        row, col = self.get_row(idx), self.get_col(idx)
        return self.arr[row][col] not in ('x', 'o')

    def is_full(self):
        return all(self.arr[row][col] in ('x', 'o') for row in range(3) for col in range(3))

    def draw(self):
        for row in self.arr:
            print("--------------")
            print("| " + " | ".join(row) + " |")
        print("--------------")

    def replace_char(self, idx, op):
        if self.is_empty(idx):
            row, col = self.get_row(idx), self.get_col(idx)
            self.arr[row][col] = op
            return True
        return False

    def is_win(self, player):
        op = player.get_op()
        return self.check_rows(op) or self.check_columns(op) or self.check_diagonals(op)

    def check_rows(self, op):
        for row in self.arr:
            if all(cell == op for cell in row):
                return True
        return False

    def check_columns(self, op):
        for col in range(3):
            if all(self.arr[row][col] == op for row in range(3)):
                return True
        return False

    def check_diagonals(self, op):
        return all(self.arr[i][i] == op for i in range(3)) or all(self.arr[i][2 - i] == op for i in range(3))


class Game:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
        self.board = Board()
        self.count = 0

    def read_players_data(self):
        self.p1.set_name(input("Welcome, Enter Your Name (First Player): "))
        self.p1.set_op(self.get_player_operator("First Player"))

        self.p2.set_name(input("Enter Your Name (Second Player): "))
        self.p2.set_op('o' if self.p1.get_op() == 'x' else 'x')

    def get_player_operator(self, player_label):
        while True:
            op = input(f"Enter an Operator for {player_label} (x, o): ").lower()
            if op in ['x', 'o']:
                return op
            print("Invalid input! Please choose 'x' or 'o'.")

    def play(self):
        self.board = Board()  # Reset the board for a new game
        self.count = 0  # Reset move count
        self.board.draw()

        while not self.board.is_full():
            current_player = self.get_current_player()

            self.process_player_turn(current_player)

            if self.board.is_win(current_player):
                current_player.increment_win_count()
                self.display_winner(current_player)
                return

            self.count += 1

        self.display_draw()

    def get_current_player(self):
        return self.p1 if self.count % 2 == 0 else self.p2

    def process_player_turn(self, player):
        while True:
            try:
                pos = int(input(f"{player.get_name()}, choose an empty position (1-9): "))
                if self.board.replace_char(pos, player.get_op()):
                    break
                print("Position is not valid or already taken. Try again.")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 9.")
        self.board.draw()

    def display_winner(self, player):
        print(f"Congratulations, {player.get_name()}! You are the winner!")
        print(f"{self.p1.get_name()} has won {self.p1.get_win_count()} times.")
        print(f"{self.p2.get_name()} has won {self.p2.get_win_count()} times.")

    def display_draw(self):
        print("It's a draw! Well played both.")

    def ask_for_new_players(self):
        while True:
            choice = input("Do you want to use the same players? (1 for yes, 2 for new players): ")
            if choice in ['1', '2']:
                if choice == '2':
                    self.p1.reset_win_count()
                    self.p2.reset_win_count()
                    self.read_players_data()
                return choice == '2'
            print("Invalid input! Please enter '1' for same players or '2' for new players.")

    def play_again(self):
        while True:
            choice = input("Play Again? (1 for yes, 2 for no): ")
            if choice in ['1', '2']:
                return choice == '1'
            print("Invalid input! Please enter '1' for yes or '2' for no.")


def main():
    game = Game()
    game.read_players_data()

    while True:
        game.play()
        if not game.play_again():
            break
        if game.ask_for_new_players():
            continue


if __name__ == "__main__":
    main()



