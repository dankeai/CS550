from basicsearch_lib.board import Board
import math
import random
import copy


class TileBoard(Board):
    """
    A Board for representing n-puzzles
    """
    __size = 0

    def __init__(self, n, force_state=None):
        # Now number of Squares in Puzzle
        self.__size = n + 1
        if not math.sqrt(self.__size).is_integer():
            print("Number of tiles \"{}\" is not representative of a square.".format(n))
            exit(2)
        side = int(math.sqrt(self.__size))
        super().__init__(side, side, self.__size)
        if force_state is None:
            # Generate Random Board
            self.initialize_board()
            self.shuffle_board()
            while (not self.solved()) and (not self.is_solveable()):
                self.shuffle_board()
        else:
            if not self.__size == len(force_state):
                print("Board size of {} is not representative of force_state: {}".format(n, force_state))
                exit(3)
            self.board = [[force_state.pop(0) for c in range(self.cols)] for r in range(self.rows)]

    def state_tuple(self):
        """Returns a tuple representation of the board"""
        temp_tuple = ()
        for i in range(self.rows):
            temp_tuple += tuple(self.board[i])
        return temp_tuple

    def initialize_board(self):
        """Initializes a new board in solved state"""
        temp_board = [x for x in range(1, self.__size)]
        temp_board.append(None)
        self.board = \
            [[temp_board.pop(0) for c in range(self.cols)] for r in range(self.rows)]

    def shuffle_board(self):
        """Shuffles current board"""
        temp_board = list(self.state_tuple())
        random.shuffle(temp_board)
        self.board = \
            [[temp_board.pop(0) for c in range(self.cols)] for r in range(self.rows)]

    def find_blank(self):
        """Returns a tuple with the location of the blank space"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] is None:
                    return c, r

    def get_actions(self):
        """Returns a list of the possible moves for the blank space"""
        blank_location = self.find_blank()
        moves = []
        if blank_location[0] > 0:  # Can Move to left
            moves.append([-1, 0])
        if blank_location[0] < self.cols - 1:  # Can Move to right
            moves.append([1, 0])
        if blank_location[1] > 0:  # Can Move up
            moves.append([0, -1])
        if blank_location[1] < self.rows - 1:  # Can Move down
            moves.append([0, 1])
        return moves

    def move(self, offset=None):
        """Moves the blank by the offset provided"""
        # If invalid move or no move, don't move
        if offset is None:
            return self
        elif offset not in self.get_actions():
            return self
        temp_tile_board = copy.deepcopy(self)
        blank_location = temp_tile_board.find_blank()
        # Location Blank Tile moves to
        col = blank_location[0] + offset[0]
        row = blank_location[1] + offset[1]
        temp_tile_board.board[row][col] = None
        # Copies number from old board
        temp_tile_board.board[blank_location[1]][blank_location[0]] = self.board[row][col]
        return temp_tile_board

    def get_inversion_count(self):
        """Returns the number of inversions on the puzzle board"""
        inversion_count = 0
        board = list(self.state_tuple())
        board.remove(None)
        for i in range(self.__size):
            for j in range(i + 1, self.__size - 1):
                if board[i] > board[j]:
                    inversion_count += 1
        if self.rows & 1 == 0:
            # If even amount of rows add the row number of the empty slot
            inversion_count += self.find_blank()[1]
        return inversion_count

    def is_solveable(self):
        """Returns True/False depending if Puzzle is solvable"""
        inversion_count = self.get_inversion_count()
        return inversion_count & 1 == 0

    def solved(self):
        """Returns True/False depending if Puzzle is solved"""
        solve_state = [x for x in range(1, self.__size)]
        solve_state.append(None)
        return self.state_tuple() == tuple(solve_state)

    def __eq__(self, other):
        # Different Size
        if self.rows != other.rows:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.get(i, j) != other.get(i, j):
                    return False
        return True
