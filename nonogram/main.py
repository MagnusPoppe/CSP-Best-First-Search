import os

from file_tostring import read_file_to_string
from nonogram.board import NonogramBoard

file_folder = "/Users/MagnusPoppe/Google Drive/Utvikling/appsPython/AI_project_1/nonogram/boards"
files = [
    "nono-cat.txt",
    "nono-chick.txt",
    "nono-clover.txt",
    "nono-elephant.txt",
    "nono-fox.txt",
    "nono-rabbit.txt",
    "nono-reindeer.txt",
    "nono-sailboat.txt",
    "nono-snail.txt",
    "nono-telephone.txt"
 ]

if __name__ == '__main__':

    file = files[0]
    input = read_file_to_string(os.path.join(file_folder, file))
    board = NonogramBoard(input)

    print(board)