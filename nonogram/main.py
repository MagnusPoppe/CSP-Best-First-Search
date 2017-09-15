import os

from file_tostring import read_file_to_string
from nonogram._old.board import NonogramBoard
from nonogram.puzzle import Puzzle

file_folder = "/Users/MagnusPoppe/Google Drive/Utvikling/appsPython/AI_project_1/nonogram/boards"
files = [
    "nono-example.txt",
    "nono-cat.txt",
    "nono-chick.txt",
    "nono-clover.txt",
    "nono-elephant.txt",
    "nono-fox.txt",
    "nono-rabbit.txt",
    "nono-reindeer.txt",
    "nono-sailboat.txt",
    "nono-snail2.txt",
    "nono-telephone.txt"
 ]

if __name__ == '__main__':

    file = files[0]
    input = read_file_to_string(os.path.join(file_folder, file))

    puzzle = Puzzle(input)

    print("ROWS:")
    for row in puzzle.rows:
        text = ""
        for i in range(len(row)):
            text += str(row[i])
        print(str(row)+" = " + text)

    print("\nCOLUMNS:")
    for row in puzzle.columns:
        text = ""
        for i in range(len(row)):
            text += str(row[i]) + "  -  "
        print(str(row)+" = " + text)

    pass