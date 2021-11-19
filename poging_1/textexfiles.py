import math, os
def encode_DIMACS(suduku, num, size):
    m  = len(suduku)
    n = m
    suduku.insert(0,f'p cnf {n} {m}')
    # saves it in folder under size 
    textfile = open(f"{size}x{size}/suduku_{size}x{size}_{num}_in_DIMACS.txt", "w")
    for element in suduku:
        textfile.write(str(element) + "\n")
    textfile.close()

def read_file (file_name):
    with open(file_name) as f:
        contents = f.readlines()
    return [x.strip() for x in  contents] 

def make_example_files(all_sudukus_file):
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
                print(i)
                print(j)
                num_1 = j + 1
                num_2 = i - size_suduku * j
                num_3 = int(c)
                suduku.append(int(num_1*100 + num_2*10 + num_3))
            if ( i  % size_suduku == 0 ) : j += 1
            i += 1
        print(suduku)
        encode_DIMACS(suduku, num, size_suduku)
        num += 1
        break
all_sudukus_file = '4x4.txt'
make_example_files(all_sudukus_file)