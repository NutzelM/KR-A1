from io import DEFAULT_BUFFER_SIZE
from math import e
import random
import copy
from operator import eq, itemgetter
backtrack = 0 
split = 0

def dpll(equation, p):
    global backtrack
    global split
    # returns dictionary of all literals with the amount of times they appear
    def all_literals(equation):
        dict_literals = {}
        for clause in equation:
            for literal in clause:
                if literal in dict_literals:
                    dict_literals[literal] += 1
                else:
                    dict_literals[literal] = 1
        return dict_literals

    # produce a random literal from the all_literals list
    def random_literal(equation):
        dict_literals = all_literals(equation)
        return random.choice(list(dict_literals.keys()))

    # checks if there is a empty clause or a unit clause
    def check_empty_unit(equation) : 
        unit_clause = []
        empty_clause = False
        for clause in equation:
            if len(clause) == 0 :
                empty_clause = True
            if len(clause) == 1 : 
                unit_clause = clause[0]
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
        [empty_clause, unit_clause] = check_empty_unit(equation)
            
        # break while loop if empty clause is found or no unit clause left 
        if empty_clause == True or not unit_clause : 
            return equation, p 
        
        # simplify equation with with unit clause = True 
        new_eq = simplify(equation, unit_clause)
        new_p = p + [unit_clause]
        return unit_prop(new_eq, new_p)
    
    equation, p  = unit_prop(equation, p)
    
    #if clause is empty unSAT
    for clause in equation :
        if len(clause) == 0: 
            return p, False
    
    # if equation is empty SAT
    if len(equation) == 0: return p, True 
    
    # make list of unassigned literals
    
    # random choice of literal, branching step
    l = random_literal(equation)

    # make deep copies of equation and p for backtracking
    equation_copy = copy.deepcopy(equation)
    p_copy = copy.deepcopy(p)
    
    split += 1 
    new_sol, assign = dpll(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    
    #backtracking
    backtrack += 1
    return dpll(simplify(equation_copy, -l), p_copy + [-l])

def dpll_MV(equation, p):
    # return list of JW2 score of each literal
    global split
    global backtrack

    def most_var(equation):
        dict_variables = {}
        which_literal = {}
        for clause in equation:
            for literal in clause:
                variable = abs(literal)
                if literal in dict_variables:
                    dict_variables[variable] += 1
                    if literal > 0:
                        which_literal[variable] += 1
                    else:
                        which_literal[variable] -= 1
                else:
                    dict_variables[variable] = 1
                    if literal > 0:
                        which_literal[variable] = 1
                    else:
                        which_literal[variable] = - 1
        return dict_variables, which_literal
    
    def select_most_var(equation):
        dict_variables, which_literal = most_var(equation)
        max_variable = max(dict_variables, key = dict_variables.get)
        select_literal = (which_literal[max_variable] >= 0)
        return max_variable, select_literal

    
    # checks if there is a empty clause or a unit clause
    def check_empty_unit(equation) : 
        unit_clause = []
        empty_clause = False
        for clause in equation:
            if len(clause) == 0 :
                empty_clause = True
            if len(clause) == 1 : 
                unit_clause = clause[0]
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
        [empty_clause, unit_clause] = check_empty_unit(equation)
            
        # break while loop if empty clause is found or no unit clause left 
        if empty_clause == True or not unit_clause : 
            return equation, p 
        
        # simplify equation with with unit clause = True 
        new_eq = simplify(equation, unit_clause)
        new_p = p + [unit_clause]
        return unit_prop(new_eq, new_p)
    
    equation, p  = unit_prop(equation, p)
    
    #if clause is empty unSAT
    for clause in equation :
        if len(clause) == 0: 
            return p, False
    
    # if equation is empty SAT
    if len(equation) == 0: return p, True 
    
    # chose variable that occurs most, if -l occurs more than l, then -l = true
    l, select_literal = select_most_var(equation)
    if not select_literal :
        l = -l

    # make deep copies of equation and p for backtracking
    equation_copy = copy.deepcopy(equation)
    p_copy = copy.deepcopy(p)
    l_copy = copy.deepcopy(l)
    split += 1 
    new_sol, assign = dpll_MV(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    
    #backtracking
    backtrack += 1
    return dpll_MV(simplify(equation_copy, -l_copy), p_copy + [-l_copy])
def dpll_MOM(equation, p):
    global split
    global backtrack
    # returns dictionary of all literals with the amount of times they appear
    def all_literals(equation):
        dict_literals = {}
        for clause in equation:
            for literal in clause:
                if literal in dict_literals:
                    dict_literals[literal] += 1
                else:
                    dict_literals[literal] = 1
        return dict_literals

    # MOM Heuristic
    def mom(equation, k = 1):
        s = []
        min_clause = len(min(equation, key=len))
        # equation with only the minimum length clauses
        min_len_equation = [x for x in equation if len(x)== min_clause]
        # occurences of all literals
        all_lit = all_literals(min_len_equation)
        for clauses in min_len_equation:    
            for literal in clauses:
                # if -lit does not occur in min_len_equation, occurence = 0 
                if str(-literal) in all_lit:
                    occ_min_lit = all_lit[-literal]
                else:
                    occ_min_lit = 0
                occ_lit = all_lit[literal] 
                z = (occ_lit + occ_min_lit)*2**k + occ_min_lit*occ_lit
                s.append((literal, z)) 
            return max(s, key=itemgetter(1))[0]

    # checks if there is a empty clause or a unit clause
    def check_empty_unit(equation) : 
        unit_clause = []
        empty_clause = False
        for clause in equation:
            if len(clause) == 0 :
                empty_clause = True
            if len(clause) == 1 : 
                unit_clause = clause[0]
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
        [empty_clause, unit_clause] = check_empty_unit(equation)
            
        # break while loop if empty clause is found or no unit clause left 
        if empty_clause == True or not unit_clause : 
            return equation, p 
        
        # simplify equation with with unit clause = True 
        new_eq = simplify(equation, unit_clause)
        new_p = p + [unit_clause]
        return unit_prop(new_eq, new_p)
    
    equation, p  = unit_prop(equation, p)
    
    #if clause is empty unSAT
    for clause in equation :
        if len(clause) == 0: 
            return p, False
    
    # if equation is empty SAT
    if len(equation) == 0: return p, True 
    
    # make list of unassigned literals
    
    # MAX : IPV random moet dit dus MOM zijn! 
    l = mom(equation)

    # make deep copies of equation and p for backtracking
    equation_copy = copy.deepcopy(equation)
    p_copy = copy.deepcopy(p)
    split +=1
    new_sol, assign = dpll_MOM(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    backtrack += 1
    #backtracking
    return dpll_MOM(simplify(equation_copy, -l), p_copy + [-l])

def solve_equation(formula, choice):
    only_truth_solution = []
    if choice == 1 :
        solution, feasible = dpll(formula, [])
    if choice == 2 :
        solution, feasible = dpll_MV(formula, [])
    if choice == 3 :
        solution, feasible = dpll_MOM(formula, [])
    if feasible :
        only_truth_solution = []
        for s in solution : 
            if s > 0 : 
                only_truth_solution.append(s)
    if len(only_truth_solution) != 9*9:
        print("not big enough solution")
        return False
    return only_truth_solution, backtrack, split
    