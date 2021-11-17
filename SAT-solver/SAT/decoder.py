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

# encode a suduku with the rules in one text file 
def encode_DIMACS(suduku, num, size):
    rules_file = read_file(f"sudoku-rules-{size}x{size}.txt")
    # saves it in folder under size 
    file_name = f"tests/{size}x{size}/sudoku_nr_{num}.txt"
    textfile = open(file_name, "w")
    for line in rules_file:
        textfile.write(line + "\n")
    for element in suduku:
        textfile.write(str(element) + "\n")
    textfile.close()


def make_equation(input_file):
    equation = read_DIMACS(input_file)[2]
    amount_variables = read_DIMACS(input_file)[0] 
    amount_clauses = read_DIMACS(input_file)[1] 
    return [amount_variables, amount_clauses, equation]


   


            
            
