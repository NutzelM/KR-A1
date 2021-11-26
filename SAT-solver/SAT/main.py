import sys
from typing import SupportsComplex
import time
from SAT import dpll
backtrack_array_h1 = []
backtrack_array_h2 = []
backtrack_array_h3 = []
time_array_h1 = []
time_array_h2 = []
time_array_h3 = []

def execute_main(args: list):
    num_heuristic, input_file = input_parameters(args)
    from SAT.decoder import make_equation
    equation = make_equation(input_file)[2]
    from SAT.dpll import solve_equation
    time_start = time.time()
    solver, backtrack, split = solve_equation(equation, num_heuristic)
    time_taken = (time.time() - time_start)
    if num_heuristic == 1 :
        # since random choice, compute solution 10 times and take average
        b_sum = backtrack
        for _ in range(9):
            dpll.split = 0
            dpll.backtrack = 0
            equation = make_equation(input_file)[2]
            solver, backtrack, split = solve_equation(equation, 1)
            b_sum = b_sum + backtrack
        backtrack_array_h1.append(b_sum/10)
        time_array_h1.append(time_taken)
    if num_heuristic == 2 : 
        backtrack_array_h2.append(backtrack)
        time_array_h2.append(time_taken)
    if num_heuristic == 3 :
        backtrack_array_h3.append(backtrack)
        time_array_h3.append(time_taken)

if __name__ == "__main__":
    execute_main(sys.argv)
    execute_main()
    exit()

def input_parameters(args: list):
    if len(args) >= 3:
        if "-S" in args[1].upper():
            num = args[1].split("S")[1]
        input = args[2]
        try:
            return int(num), input
        except TypeError:
            print("incorrect request")
    else:
        print("there is something not right")
    exit()