import sys

def execute_main(args):
    num_heuristic, input_file = input_parameters(args)
    
    # make .out file 
    solution_file = "./" + input_file[input_file.rfind("/"):input_file.rfind(".")] + ".out"

    from SAT.decoder import make_equation
    equation = make_equation(input_file)[2]
    from SAT.dpll import solve_equation
    solver, backtrack, split = solve_equation(equation, num_heuristic)
    print("Your solved sudoku is: " + str(solver))
    print("The solution has been written to a .out file of the same name in DIMACS form.")
    with open(solution_file, "w") as f:
        f.write(f'p cnf {len(solver)} {len(solver)}')
        for literal in solver:
            f.write(f'{literal} 0\n')

def input_parameters(args: list):
    num = None
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

if __name__ == "__main__":
    execute_main(sys.argv)
    exit()
