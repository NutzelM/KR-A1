import sys
from typing import SupportsComplex
def execute_main(args: list):
    num_heuristic, input_file = input_parameters(args)
    from SAT.decoder import make_equation
    equation = make_equation(input_file)[2]
    from SAT.dpll import solve_equation
    solver = solve_equation(equation, num_heuristic)
    print(solver)

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