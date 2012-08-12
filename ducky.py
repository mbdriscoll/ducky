"""
ducky.py

A soduko solver in python. Solves puzzles in the following format, where '0'
stands for unknown value. Requires numpy. Tested on Python 2.7.

$ cat p0.txt
0 0 9  0 0 0  0 4 0
0 0 2  0 0 8  0 9 7
0 0 7  6 3 0  2 0 0
0 0 0  0 0 6  0 0 1
0 0 0  0 5 0  3 6 0
0 7 0  0 0 0  0 0 0
3 0 0  7 0 1  0 0 0
8 1 0  0 4 3  0 0 0
0 2 0  0 0 0  0 0 0

$ python ducky.py --puzzle p0.txt
...

"""

import sys, time, math
import numpy as np
from itertools import *
from optparse import OptionParser

def possible_vals(puzzle, i, j):
    """ The possible values a given variable can take. """
    blksz = int(math.sqrt(puzzle.shape[0]))
    bi,bj = i-(i%blksz),j-(j%blksz)
    vals = [x for x in range(1,puzzle.shape[0]+1) \
               if x not in puzzle[i,:] \
              and x not in puzzle[:,j] \
              and x not in puzzle[bi:bi+blksz,bj:bj+blksz]]
    return vals

def solve(puzzle):
    """ Fill in blanks in puzzle and return True if a solution exists. """
    for i,j in ifilter(lambda ij: not puzzle[ij], \
                       product( *[range(x) for x in puzzle.shape] )):
       for val in possible_vals(puzzle, i, j):
           puzzle[i,j] = val
           if solve(puzzle):
               return True # found a solution
       puzzle[i,j] = 0.
       return False # no solution found
    return True # all spaces filled in

def check(answer):
    """ Return true if ANSWER is a valid solution. """
    puzsz = answer.shape[0]
    blksz = int(math.sqrt(puzsz))
    blkbases = range(0, puzsz, blksz)
    for k in range(1,puzsz+1):
        for m in range(puzsz): # rows and columns
            assert k in answer[m,:], \
                   "%d not in row %d\n%s" % (k, m, answer)
            assert k in answer[:,m], \
                   "%d not in col %d\n%s" % (k, m, answer)
        for i,j in product(blkbases, blkbases): # blocks
            assert k in answer[i:i+blksz,j:j+blksz], \
                   "%d not in block at (%d,%d)\n%s" % (k, i, j, answer)
    return True

def main():
    """ Parse args, read input, call solve, print result. """
    parser = OptionParser()
    parser.add_option("--puzzle", dest="puzzle_filename", default='puzzle00.txt')
    (options, args) = parser.parse_args()

    with open(options.puzzle_filename) as pfile:
        puzzle = np.array([x.split() for x in pfile.readlines()], dtype=np.int8)

    assert puzzle.shape[0] == puzzle.shape[1], \
        "Puzzle must have same size in boths dimensions"
    assert int(math.sqrt(puzzle.shape[0]))**2 == puzzle.shape[0], \
        "Puzzle dimension must be a perfect square"

    print "Solving puzzle:\n%s" % puzzle
    start_time = time.time()
    solvable = solve(puzzle)
    duration = time.time() - start_time

    if not solvable:
        print "No solution exists (took %f seconds):\n%s" % (duration, puzzle)
    else:
        assert check(puzzle)
        print "Answer (took %f seconds):\n%s" % (duration, puzzle)

if __name__ == '__main__':
  main()
