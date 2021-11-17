from io import DEFAULT_BUFFER_SIZE
from os import read, remove
import random
import os
import math
                
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

def dpll_MOM(equation, p):
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

def solve_equation(formula, choice):
    if choice == 1 :solution, feasible = dpll(formula, [])
    if choice == 2 :solution, feasible = dpll_MOM(formula, [])
    if feasible :
        only_truth_solution = []
        for s in solution : 
            if s > 0 : 
                only_truth_solution.append(s)
    return only_truth_solution

