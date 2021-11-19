from io import DEFAULT_BUFFER_SIZE
import random
import copy
import numpy as np

def dpll(equation, p):
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

    new_sol, assign = dpll(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    
    #backtracking
    return dpll(simplify(equation_copy, -l), p_copy + [-l])
def dpll_JW_TS(equation, p):
    # return list of JW2 score of each literal
    def JW2(formula):
        variable_list = {}
        bigger_than_list = {}
        for clause in formula:
            for literal in clause:
                variable = abs(literal)
                if variable in variable_list:
                    if literal > 0 : 
                        bigger_than_list[literal] += 2 ** -len(clause)
                    else :
                        bigger_than_list[literal] -= 2 ** -len(clause)
                    variable_list[literal] += 2 ** -len(clause)
                else:
                    if literal > 0 : 
                        bigger_than_list[literal] = 2 ** -len(clause)
                    else :
                        bigger_than_list[literal] - 2 ** -len(clause)
                    variable_list[literal] = 2 ** -len(clause)
        return variable_list, bigger_than_list
    
    def max_score_JW2(equation):
        variable_list, bigger_than_list = JW2(equation)
        max_score = max(variable_list, key=variable_list.get)
        return max_score, bigger_than_list[max_score]
    
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
    
    # random choice of literal, branching step
    l, bigger_than = max_score_JW2(equation)

    # if J(I) < J(not I) then assign False 
    if not bigger_than : 
        l = -l

    # make deep copies of equation and p for backtracking
    equation_copy = copy.deepcopy(equation)
    p_copy = copy.deepcopy(p)

    new_sol, assign = dpll_JW_TS(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    
    #backtracking
    return dpll_JW_TS(simplify(equation_copy, -l), p_copy + [-l])
def dpll_MOM(equation, p):
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
    
    # MAX : IPV random moet dit dus MOM zijn! 
    l = random_literal(equation)

    # make deep copies of equation and p for backtracking
    equation_copy = copy.deepcopy(equation)
    p_copy = copy.deepcopy(p)

    new_sol, assign = dpll_MOM(simplify(equation, l), p + [l])
    if assign: 
        return new_sol, True
    
    #backtracking
    return dpll_MOM(simplify(equation_copy, -l), p_copy + [-l])

def solve_equation(formula, choice):
    only_truth_solution = []
    if choice == 1 :
        solution, feasible = dpll(formula, [])
    if choice == 2 :
        solution, feasible = dpll_JW_TS(formula, [])
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
    return only_truth_solution
    

