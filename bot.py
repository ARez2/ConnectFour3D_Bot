import sys
import random
import math

MINIMAX_DEPTH = 5

class Board():
    EMPTY = 255
    def __init__(self, player, enemy):
        self.data = bytearray(4 * 4 * 4)
        for i in range(len(self.data)):
            self.data[i] = self.EMPTY
        self.player = player
        self.enemy = enemy


    def copy(self):
        b = Board(self.player, self.enemy)
        b.data = self.data.copy()
        return b


    def xyz_to_offset(self, x, y, z):
        return z * 16 + y * 4 + x

    def column_to_xy(self, column):
        x = column % 4
        y = int(column / 4)
        return x, y

    def get_piece(self, x, y, z):
        return self.data[self.xyz_to_offset(x, y, z)]

    def drop_piece(self, player, column):
        x, y = self.column_to_xy(column)
        for z in range(4):
            if self.get_piece(x, y, z) == self.EMPTY:
                self.data[self.xyz_to_offset(x, y, z)] = player
                return
        #self.print()
        print(f"Stapel {column} ist voll")


    def print(self):
        print("Board:")
        for y in range(4):
            output = ""
            for z in range(4):
                for x in range(4):
                    piece = self.get_piece(x, y, z)
                    if piece == self.EMPTY:
                        output += f"[white]{'-'}[/white]"
                    elif piece == self.player:
                        output += f"[green]{'0'}[/green]"
                    elif piece == self.enemy:
                        output += f"[blue]{'1'}[/blue]"
                    else:
                        output += f"[red]{'?'}[/red]"
                    output += " "
                output += "    "
            print(output)


    def is_stack_full(self, column):
        x, y = self.column_to_xy(column)
        return self.get_piece(x, y, 3) != self.EMPTY

    def get_valid_columns(self):
        valid_columns = []
        for column in range(16):
            if not self.is_stack_full(column):
                valid_columns.append(column)
        return valid_columns


    def is_win_state(self, player):
        return self.is_win_state_x(player) or \
            self.is_win_state_y(player) or \
            self.is_win_state_z(player) or \
            self.is_win_state_xz(player) or \
            self.is_win_state_yz(player) or \
            self.is_win_state_xy(player) or \
            self.is_win_state_corners(player)

    def is_win_state_x(self, player):
        """Checks all x rows"""
        for z in range(4):
            for y in range(4):
                row = [self.get_piece(x, y, z) for x in range(4)]
                if self.check_row(row, player):
                    return True
        return False

    def is_win_state_y(self, player):
        """Checks all y rows"""
        for z in range(4):
            for x in range(4):
                row = [self.get_piece(x, y, z) for y in range(4)]
                if self.check_row(row, player):
                    return True
        return False

    def is_win_state_z(self, player):
        """Checks all z columns"""
        for y in range(4):
            for x in range(4):
                row = [self.get_piece(x, y, z) for z in range(4)]
                if self.check_row(row, player):
                    return True
        return False

    def is_win_state_xz(self, player):
        """Checks diagonals along Y axis in XZ plane"""
        for y in range(4):
            row = [self.get_piece(i, y, i) for i in range(4)]
            if self.check_row(row, player):
                return True
            row = [self.get_piece(i, y, 3 - i) for i in range(4)]
            if self.check_row(row, player):
                return True
        return False

    def is_win_state_yz(self, player):
        """Checks diagonals along X axis in YZ plane"""
        for x in range(4):
            row = [self.get_piece(x, i, i) for i in range(4)]
            if self.check_row(row, player):
                return True
            row = [self.get_piece(x, i, 3 - i) for i in range(4)]
            if self.check_row(row, player):
                return True
        return False

    def is_win_state_xy(self, player):
        """Checks diagonals along Z axis in XY plane"""
        for z in range(4):
            row = [self.get_piece(i, i, z) for i in range(4)]
            if self.check_row(row, player):
                return True
            row = [self.get_piece(i, 3 - i, z) for i in range(4)]
            if self.check_row(row, player):
                return True
        return False

    def is_win_state_corners(self, player):
        """Checks from corners diagonally through the cube"""
        row = [self.get_piece(i, i, i) for i in range(4)]
        if self.check_row(row, player):
            return True
        row = [self.get_piece(i, i, 3 - i) for i in range(4)]
        if self.check_row(row, player):
            return True
        row = [self.get_piece(i, 3 - i, i) for i in range(4)]
        if self.check_row(row, player):
            return True
        row = [self.get_piece(3 - i, i, i) for i in range(4)]
        if self.check_row(row, player):
            return True
        return False

    def check_row(self, row, player):
        return all(e == player for e in row)

    
    def score(self, player):
        score = 0
        score += self.score_x(player)
        score += self.score_y(player)
        score += self.score_z(player)
        score += self.score_xz(player)
        score += self.score_yz(player)
        score += self.score_xy(player)
        score += self.score_corners(player)
        return score
    
    def score_x(self, player):
        """Scores all x rows"""
        score = 0
        for z in range(4):
            for y in range(4):
                row = [self.get_piece(x, y, z) for x in range(4)]
                score += self.score_row(row, player)
        return score
    
    def score_y(self, player):
        """Scores all y rows"""
        score = 0
        for z in range(4):
            for x in range(4):
                row = [self.get_piece(x, y, z) for y in range(4)]
                score += self.score_row(row, player)
        return score
    
    def score_z(self, player):
        """Scores all z rows"""
        score = 0
        for y in range(4):
            for x in range(4):
                row = [self.get_piece(x, y, z) for z in range(4)]
                score += self.score_row(row, player)
        return score
    
    def score_xz(self, player):
        """Scores diagonals along Y axis in XZ plane"""
        score = 0
        for y in range(4):
            row = [self.get_piece(i, y, i) for i in range(4)]
            score += self.score_row(row, player)
            
            row = [self.get_piece(i, y, 3 - i) for i in range(4)]
            score += self.score_row(row, player)
        return score
    
    def score_yz(self, player):
        """Scores diagonals along Y axis in XZ plane"""
        score = 0
        for x in range(4):
            row = [self.get_piece(x, i, i) for i in range(4)]
            score += self.score_row(row, player)
            
            row = [self.get_piece(x, i, 3 - i) for i in range(4)]
            score += self.score_row(row, player)
        return score
    
    def score_xy(self, player):
        """Scores diagonals along Y axis in XZ plane"""
        score = 0
        for z in range(4):
            row = [self.get_piece(i, i, z) for i in range(4)]
            score += self.score_row(row, player)
            
            row = [self.get_piece(i, 3 - i, z) for i in range(4)]
            score += self.score_row(row, player)
        return score

    def score_corners(self, player):
        """Scores from corners diagonally through the cube"""
        score = 0
        row = [self.get_piece(i, i, i) for i in range(4)]
        score += self.score_row(row, player)
        row = [self.get_piece(i, i, 3 - i) for i in range(4)]
        score += self.score_row(row, player)
        row = [self.get_piece(i, 3 - i, i) for i in range(4)]
        score += self.score_row(row, player)
        row = [self.get_piece(3 - i, i, i) for i in range(4)]
        score += self.score_row(row, player)
        return score
    
    def score_row(self, row, player):
        score = 0
        if row.count(player) == 4:
            score += 10000 * 101
        if row.count(player) == 3 and row.count(self.EMPTY) == 1:
            score += 5
        elif row.count(player) == 2 and row.count(self.EMPTY) == 2:
            score += 2
        #elif row.count(player) == 1 and row.count(self.EMPTY) == 3:
        #    score += 1
        opp = self.enemy if player == self.player else self.player
        if row.count(opp) == 3 and row.count(self.EMPTY) == 1:
            score -= 4#1000
        return score



class Game():
    def __init__(self, botplayernumber, filename):
        self.filename = filename
        self.game_running = True
        self.bot_playernumber = botplayernumber
        self.enemynumber = 0 if botplayernumber == 1 else 1
        self.current_board = Board(self.bot_playernumber, self.enemynumber)
        self.gameloop()


    def gameloop(self):
        while self.game_running:
            contents = None
            with open(self.filename, "r") as f:
                contents = f.readline().strip()

            if contents == "start":
                self.make_bot_move()
            elif contents == "end":
                self.game_running = False
            elif contents.startswith("<"):
                enemy_move = int(contents[1:])
                print("Enemy move: ", enemy_move)
                # Add enemy move to board
                self.current_board.drop_piece(self.enemynumber, int(enemy_move))
                self.make_bot_move()
                #self.current_board.print()


    def make_bot_move(self):
        column, score = self.minimax(self.current_board, MINIMAX_DEPTH, -math.inf, math.inf, False)
        #print("Score: ", score)
        if column is None:
            print("Game over")
        else:
            print(f"Bot move: {column}")
            self.current_board.drop_piece(self.bot_playernumber, column)
            with open(self.filename, "w") as f:
                f.write(f">{int(column)}")
            if self.current_board.is_win_state(self.bot_playernumber):
                print("Bot wins")
                #self.current_board.print()
                exit()
            elif self.current_board.is_win_state(self.enemynumber):
                print("Player wins")
                #self.current_board.print()
                exit()


    # Pick the best move by looking at all possible future moves and comparing their scores
    def minimax(self, board, depth, alpha, beta, maximisingPlayer):
        if board.is_win_state(self.bot_playernumber):
            # Player wins the game
            return (None, math.inf)

        if board.is_win_state(self.enemynumber):
            # Enemy wins the game
            return (None, -math.inf)

        valid_columns = board.get_valid_columns()
        if len(valid_columns) == 0:
            # No valid moves left
            return (None, 0)

        if depth == 0:
            # Return this boards score
            return (None, board.score(self.bot_playernumber))

        # Randomize locations in case of same score
        random.shuffle(valid_columns)

        if maximisingPlayer:
            # Maximising player score
            max_score = -math.inf
            max_column = valid_columns[0]
            for col in valid_columns:
                # Drop a piece into copy of current board
                new_board = board.copy()
                new_board.drop_piece(self.bot_playernumber, col)

                # Calculate score of board which results from the last move
                score = self.minimax(new_board, depth - 1, alpha, beta, not maximisingPlayer)[1]
                if score > max_score:
                    max_score = score
                    max_column = col

                # Minimax stuff
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break
            return max_column, max_score
        else:
            # Minimising enemy score
            min_score = math.inf
            min_column = valid_columns[0]
            for col in valid_columns:
                # Drop a piece into copy of current board
                new_board = board.copy()
                new_board.drop_piece(self.enemynumber, col)

                # Calculate score of board which results from the last move
                score = self.minimax(new_board, depth - 1, alpha, beta, not maximisingPlayer)[1]
                if score < min_score:
                    min_score = score
                    min_column = col

                # Minimax stuff
                beta = min(beta, min_score)
                if alpha >= beta:
                    break
            return min_column, min_score



if __name__ == "__main__":
    args = sys.argv
    player = args[1]
    file = args[2]
    bot = Game(int(player), file)