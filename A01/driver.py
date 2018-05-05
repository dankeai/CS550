from boardtypes import TileBoard


def driver():
    tile_board = TileBoard(8)
    print("Valid Commands: Left, Right, Up, Down, Quit")
    while not tile_board.solved():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(tile_board)
        print(" ---  ---  ---  ---  ---  ")
        valid = False
        while not valid:
            move = input("Move?")
            if "QUIT" == move.upper():
                print("Bye")
                exit(0)
            elif "LEFT" == move.upper():
                tile_board = tile_board.move([-1, 0])
            elif "RIGHT" == move.upper():
                tile_board = tile_board.move([1, 0])
            elif "UP" == move.upper():
                tile_board = tile_board.move([0, -1])
            elif "DOWN" == move.upper():
                tile_board = tile_board.move([0, 1])
            else:
                print("Try Again")
                print("Valid Commands: Left, Right, Up, Down, Quit")
                continue
            valid = True

    print(tile_board)
    print("Congratulations, puzzle solved", end="")


driver()
