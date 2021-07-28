import argparse
import os
from sudoku import Sudoku
import time
import sys
import os
from solutions import arc_cons, forward_checking, no_inference, lcv, mrv, first_unassigned_variable, unordered_domain_values, \
    backtracking_search
dir_path = os.path.dirname(os.path.realpath(__file__))

begin = time.time()

def board_file(path):
    with open(path) as f:
        board = f.readline()
    return board


arg_to_function = {
    # Inference
    'no_inference': no_inference,
    'arc_cons': arc_cons,
    'forward_checking': forward_checking,
    # Value ordering
    'unordered_domain_values': unordered_domain_values,
    'lcv': lcv,
    # Variable ordering
    'first_unassigned_variable': first_unassigned_variable,
    'mrv': mrv,
}

# parse args
parser = argparse.ArgumentParser(description='sudoku')
parser.add_argument('-b', '--board', help='board')
parser.add_argument('-valo', '--valordering', help='value ordering')
parser.add_argument('-varo', '--varordering', help='variable ordering')
parser.add_argument('-inf', '--inference', help='inference')
args = parser.parse_args()

# default values
board = board_file(os.path.join(dir_path, 'boards/example.txt'))
valordering = unordered_domain_values
varordering = first_unassigned_variable
inference = no_inference

# replace defaults
if args.board:
    board = board_file(os.path.join(dir_path, 'boards/{}.txt'.format(args.board)))
if args.valordering:
    valordering = arg_to_function[args.valordering]
if args.varordering:
    varordering = arg_to_function[args.varordering]
if args.inference:
    inference = arg_to_function[args.inference]

s = Sudoku(board)
s.display(s.infer_assignment())
backtracking_search(s, varordering, valordering, inference)
s.display(s.infer_assignment())

time.sleep(1)
# store end time
end = time.time()
# total time taken
print(f"Total runtime of the program is {end - begin}")
#
# print(f"Total size of the program is {sys.getsizeof(board)}")
# # file_size = os.path.getsize('sudoku.py')
# #
# # print(f"Total size of the program is {file_size}")
