import os
from SAT.main import execute_main
import math
from SAT.decoder import encode_DIMACS
from SAT.decoder import read_file

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
        final_directory = os.path.join(f'{current_directory}/tests', rf'{size_suduku}x{size_suduku}')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        for c in line:
            if c != '.':
                num_1 = j + 1
                num_2 = i - size_suduku * j
                num_3 = int(c)
                suduku.append(f'{int(num_1*100 + num_2*10 + num_3)} 0')
            if ( i  % size_suduku == 0 ) : j += 1
            i += 1
        encode_DIMACS(suduku, num, size_suduku)
        num += 1             

make_suduku_files("4x4.txt")
print(os.getcwd())
execute_main(['SA','-S1', '/Users/maike/Desktop/SAT-solver/tests/4x4/sudoku_nr_100.txt'])
