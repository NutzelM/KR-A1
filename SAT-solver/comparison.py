import os
from typing_extensions import runtime
from SAT.main import execute_main
import math
from SAT.decoder import encode_DIMACS
from SAT.decoder import read_file
import pandas as pd
import time

# makes all the DIMAC txt file of all the sudukus from suduku file 
def make_suduku_files(all_sudukus_file):
    all_sudukus = read_file(all_sudukus_file)
    num = 1
    current_directory = os.getcwd()
    diversity = []
    for line in all_sudukus:
        values_in_clue = []
        suduku = []
        i = 1
        j = 0
        size_suduku = int(math.sqrt(len(line)))
        # creates a folder for the size of the suduku
        final_directory = os.path.join(f'{current_directory}/tests', rf'{size_suduku}x{size_suduku}')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        for c in line:
            if c != '.':
                num1 = j + 1
                num2 = i - size_suduku * j
                num3 = int(c)
                suduku.append(f'{int(num1*100 + num2*10 + num3)} 0')
                values_in_clue.append(num3)
            if ( i  % size_suduku == 0 ) : j += 1
            i += 1
        encode_DIMACS(suduku, num, size_suduku)
        diversity.append([num, len(values_in_clue), len(values_in_clue) - len(set(values_in_clue))])
        num += 1            

# LOAD SUDUKUS FILES. NOTE: delete 9x9 folder first because 1000 sudokus, damnhard and top91 will overwrite!
#make_suduku_files("4x4.txt")
#make_suduku_files("1000 sudokus.txt")
#make_suduku_files("damnhard.sdk.txt")
#make_suduku_files("top91.sdk.txt")

for num in range(1):
    link_to_suduku = os.path.join(os.getcwd(), f'tests/9x9/sudoku_nr_{num+1}.txt')
    execute_main(['SA','-S3', link_to_suduku])


