import matplotlib.pyplot as plt
backtrack_h1 = [4.886666666666667, 3.88, 55.22666666666667, 6.823333333333333, 2.17]
backtrack_h2 =[0.6, 0.5333333333333333, 0.3, 0.43333333333333335, 0.3333333333333333]
backtrack_h3 =[0.7666666666666667, 0.4666666666666667, 2.3333333333333335, 0.3333333333333333, 0.6666666666666666]
runtime_h1= [1.9710163831710816, 1.9476476669311524, 2.0136054118474322, 2.0881924867630004, 1.9643747886021932]
runtime_h2= [1.9925806681315104, 2.0067280610402425, 1.991091513633728, 1.9620360612869263, 1.9912878433863321]
runtime_h3= [2.0173993349075316, 2.0316213528315226, 2.043868414560954, 1.9864044348398844, 2.024614755312602]
amount_of_clues = [17,18,19,20,21]

plt.plot(amount_of_clues, backtrack_h2, color='blue', marker='o')
plt.plot(amount_of_clues, backtrack_h3, color='green', marker='o')
plt.title('number of backtracks per amount of clues', fontsize=14)
plt.xlabel('number of clues', fontsize=14)
plt.ylabel('number of backtracks', fontsize=14)
plt.legend(['DPLL + MOV', 'DPLL + MOM'])
plt.grid(True)
plt.show()

plt.plot(amount_of_clues, runtime_h1, color='red', marker='o')
plt.plot(amount_of_clues, runtime_h2, color='blue', marker='o')
plt.plot(amount_of_clues, runtime_h3, color='green', marker='o')
plt.title('runtime per amount of clues', fontsize=14)
plt.xlabel('number of clues', fontsize=14)
plt.ylabel('runtime (in s)', fontsize=14)
plt.legend(['DPLL', 'DPLL + MOV', 'DPLL + MOM'])
plt.grid(True)
plt.show()