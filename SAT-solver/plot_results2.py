import matplotlib.pyplot as plt
backtrack_h1 = [4.886666666666667,0.7866666666666666, 0.15, 0.04, 0.0]
backtrack_h2= [0.6, 0.8, 0.1, 0, 0]
backtrack_h3 = [0.7666666666666667, 0.2, 0.1, 0.03333333333333333, 0]
runtime_h1 =[1.9710163831710816, 2.0384856780370075, 2.1228087345759072, 2.257316223780314, 2.4329028606414793]
runtime_h2 =[1.9925806681315104, 2.0433329502741495, 2.1252089103062946, 2.2606486876805625, 2.4249506553014117]
runtime_h3 =[2.0173993349075316, 2.021469322840373, 2.1221975088119507, 2.257640250523885, 2.4388726552327475]
amount_of_clues = [17,32,47,62,77]

plt.plot(amount_of_clues, backtrack_h1, color='salmon', marker='o')
plt.plot(amount_of_clues, backtrack_h2, color='darkcyan', marker='o')
plt.plot(amount_of_clues, backtrack_h3, color='cornflowerblue', marker='o')
plt.title('number of backtracks per amount of clues', fontsize=24)
plt.xlabel('number of clues', fontsize=24)
plt.ylabel('number of backtracks', fontsize=24)
plt.legend(['DPLL', 'DPLL + MOV', 'DPLL + MOM'])
plt.grid(True)
plt.show()

plt.plot(amount_of_clues, runtime_h1, color='salmon', marker='o')
plt.plot(amount_of_clues, runtime_h2, color='darkcyan', marker='o')
plt.plot(amount_of_clues, runtime_h3, color='cornflowerblue', marker='o')
plt.title('runtime per amount of clues', fontsize=24)
plt.xlabel('number of clues', fontsize=24)
plt.ylabel('runtime (in s)', fontsize=24)
plt.legend(['DPLL', 'DPLL + MOV', 'DPLL + MOM'])
plt.grid(True)
plt.show()