from rush_hour.board import Board




if __name__ == '__main__':
    board = Board("easy-3.txt")
    print(board)

    print(board.vehicles[1])
    up, down = board.get_moves(board.vehicles[1])

    print ("Can move? up/left="+str(up)+", down/right="+str(down))