import sys
import numpy as np
from optparse import OptionParser

def solve(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i,j] == 0:
                possible = [x for x in range(1,10) \
                               if x not in puzzle[i,:] \
                              and x not in puzzle[:,j] \
                              and x not in puzzle[i-(i%3):i-(i%3)+3, \
                                                   j-(j%3):j-(j%3)+3]]
                for val in possible:
                    puzzle[i,j] = val
                    if solve(puzzle):
                        return True
                puzzle[i,j] = 0
                return False
    return True

def check(answer):
    for k in range(1,10):
        for i in range(9): # rows
            assert k in answer[i,:], "%d not in row %d\n%s" % (k, i, answer)
        for j in range(9): # columns
            assert k in answer[:,j], "%d not in col %d\n%s" % (k ,j, answer)
        for i in [0, 3, 6]: # blocks
            for j in [0, 3, 6]:
                assert k in answer[i:i+3,j:j+3], \
                    "%d not in block at (%d,%d)\n%s" % (k, i, j, answer)
    return True

def main():
    print "Welcome to ducky!"

    parser = OptionParser()
    parser.add_option("--puzzle", dest="puzzle_filename", default='puzzle.txt')
    (options, args) = parser.parse_args()

    puzzle = np.ndarray((9,9))
    with open(options.puzzle_filename) as pfile:
        for i in range(9):
            line = pfile.readline().split()
            if len(line) != 9: continue
            for j in range(9):
                puzzle[i,j] = line[j]

    print "Solving:\n%s" % puzzle
    if not solve(puzzle):
        print "No solution exists."
        print puzzle
    else:
        assert check(puzzle)
        print "Answer:\n%s" % puzzle

if __name__ == '__main__':
  main()
