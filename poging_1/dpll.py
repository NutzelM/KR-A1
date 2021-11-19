from io import DEFAULT_BUFFER_SIZE
from os import read, remove
import random
import os
import math

def read_file (file_name):
    with open(file_name) as f:
        contents = f.readlines()
    return [x.strip() for x in  contents] 

def read_DIMACS (file_name):
    suduku_DIMACS = read_file(file_name)
    first_line = suduku_DIMACS[0].split(" ")
    # checks DIMAC format
    assert first_line[0] == "p" and first_line[1]=="cnf", "incorrect DIMACS format"
    # n: total amount of variables, m: amount of clauses
    n, m = int(first_line[2]), int(first_line[3])
    clauses = []
    for line in suduku_DIMACS[1:]:
        # skip lines that start with c
        if line[0] == 'c':
            continue
        clause = []
        line_list = line.split(" ")
        for c in line_list:
            var = int(c)
            if var!=0:
                clause.append(var)
        clauses.append(clause)
    return [n, m, clauses]

def encode_DIMACS(suduku, num, size):
    m  = len(suduku)
    n = m
    suduku.insert(0,f'p cnf {n} {m}')
    # saves it in folder under size 
    file_name = f"{size}x{size}/suduku_{size}x{size}_{num}_in_DIMACS.txt"
    textfile = open(file_name, "w")
    for element in suduku:
        textfile.write(str(element) + "\n")
    textfile.close()


def make_equation(suduku_file, rules_file):
    suduku_list = read_DIMACS(suduku_file)[2]
    rules_list = read_DIMACS(rules_file)[2]
    amount_variables = read_DIMACS(suduku_file)[0] + read_DIMACS(rules_file)[0]
    amount_clauses = read_DIMACS(suduku_file)[1] + read_DIMACS(rules_file)[1]
    equation = suduku_list + rules_list
    return [amount_variables, amount_clauses, equation]

# makes all the DIMAC txt file of all the sudukus from suduku file 
def make_suduku_files(all_sudukus_file):
    all_sudukus = read_file(all_sudukus_file)
    num = 1
    current_directory = os.getcwd()
    for line in all_sudukus:
        suduku = []
        i = 1
        j = 0
        size_suduku = int(math.sqrt(len(line)))
        # creates a folder for the size of the suduku
        final_directory = os.path.join(current_directory, rf'{size_suduku}x{size_suduku}')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        for c in line:
            if c != '.':
                num_1 = j + 1
                num_2 = i - size_suduku * j
                num_3 = int(c)
                suduku.append(int(num_1*100 + num_2*10 + num_3))
            if ( i  % size_suduku == 0 ) : j += 1
            i += 1
        encode_DIMACS(suduku, num, size_suduku)
        num += 1
        break
                
# DPLL ALGORITHM
def dpll(equation, p):

    # returns a list of the literals which have not been assigned yet (not in p)
    def unassigned_literals(equation, p) :
        u_l = []
        for clauses in equation:
            for clause in clauses:
                if abs(clause) not in u_l and abs(clause) not in p: u_l.append(abs(clause))
        return u_l

    # checks if there is a empty clause or a unit clause
    def check_empty_unit(equation) : 
        unit_clause = []
        empty_clause = False
        for clauses in equation:
            if len(clauses) == 0 :
                empty_clause = True
            if len(clauses) == 1 : 
                unit_clause = clauses[0]
        return [empty_clause, unit_clause]

    # simplifies the equation given a literal : removes clause containing literal and removes not-literal from clause
    def simplify(equation, literal):
        new_eq = []
        for clause in equation:
            
            # remove clauses containing literal
            if literal not in clause:
                new_eq.append(clause)
               
                # shorten clauses containg -literal (reversed to not shift indices)
                for i in reversed(range(len(clause))):
                    if clause[i] == -literal:
                        del new_eq[new_eq.index(clause)][i]
        return new_eq
    
    # unit propogation: not an empty clause but there is a unit clause: simplify with that unit clause = True
    def unit_prop(equation, p):
        while 1:
            [empty_clause, unit_clause] = check_empty_unit(equation)
            
            # break while loop if empty clause is found or no unit clause left 
            if empty_clause == True or not unit_clause : 
                return equation, p 
            
            # simplify equation with with unit clause = True 
            equation = simplify(equation, unit_clause)
            p.append(unit_clause)
    
    equation, p  = unit_prop(equation, p)
    
    #if clause is empty unSAT
    for clauses in equation :
        if len(clauses) == 0: 
            return p, False
    
    # if equation is empty SAT
    if len(equation) == 0: return p, True 
    
    # make list of unassigned literals
    u_l = unassigned_literals(equation, p)
    
    # random choice of literal, branching step
    l = random.choice(u_l)
    if dpll(simplify(equation, l), p + [l]) : return p, True
    else : dpll(simplify(equation, -l), p + [-l])

def solve_sudoku(suduku_file, rules_file):
    equation = make_equation(suduku_file, rules_file)
    amount_variables = equation[0]
    amount_of_clauses = equation[1]
    print('..............................')
    print(equation[2])
    print('..............................')
    solution, feasible = dpll(equation[2], [])
    if feasible :
        only_truth_solution = []
        for s in solution : 
            if s > 0 : 
                only_truth_solution.append(s)
    return only_truth_solution

# for 4x4
make_suduku_files("4x4.txt")
make_suduku_files("1000 sudokus.txt")
print(os.getcwd())
main_dir = str(os.getcwd())
sizes = [4]
for size in sizes:
    rules_file = f"sudoku-rules-{size}x{size}.txt"
        # creates a folder for the size of the suduku
    for num in range(1000):
        suduku_file = f"{size}x{size}/suduku_{size}x{size}_{num + 1}_in_DIMACS.txt"
        file_path = os.path.join(main_dir, suduku_file)
        if os.path.isfile(file_path):
            solution = solve_sudoku(suduku_file, rules_file)
            print(solution)


            
            
