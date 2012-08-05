import sys, time
import numpy as np
from itertools import *
from optparse import OptionParser

class Timer(object):
    def __enter__(self):
        self._start_time = time.time()
        return self
    def __exit__(self, *args):
        self._total_time = time.time()-self._start_time
    def __str__(self):
        return str(self._total_time)

def possible_vals(puzzle, i, j):
    bi,bj = i-(i%3),j-(j%3)
    vals = [x for x in range(1,10) \
               if x not in puzzle[i,:] \
              and x not in puzzle[:,j] \
              and x not in puzzle[bi:bi+3,bj:bj+3]]
    return vals

def solve(puzzle):
    # TODO order by most constrained variable
    for i,j in ifilter(lambda m: not puzzle[m], \
                       product(range(9), range(9))):
       remaining_vals = possible_vals(puzzle, i, j)
       # TODO order by least constrained value
       for val in remaining_vals:
           puzzle[i,j] = val
           if solve(puzzle):
               return True # found a solution
       puzzle[i,j] = 0
       return False # no solution found
    return True # all spaces filled in

def check(answer):
    for k in range(1,10):
        for i in range(9): # rows
            assert k in answer[i,:], \
                   "%d not in row %d\n%s" % (k, i, answer)
        for j in range(9): # columns
            assert k in answer[:,j], \
                   "%d not in col %d\n%s" % (k ,j, answer)
        for i,j in product([0,3,6],[0,3,6]): # blocks
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
    with Timer() as timing:
        solvable = solve(puzzle)

    if not solve(puzzle):
        print "No solution exists (took %s seconds):\n%s" % (timing, puzzle)
    else:
        assert check(puzzle)
        print "Answer (took %s seconds):\n%s" % (timing, puzzle)

if __name__ == '__main__':
  main()
