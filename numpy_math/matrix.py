import numpy as np
from numpy import linalg as LA

# 1 Определитель матрицы или детерминант
# это объём N-мерного параллелепипеда, который образуется,
# если рассмотреть строки матрицы в качестве векторов,
# образующих рёбра этого параллелепипеда.
# np.linalg.det(M) == 0 матрица называется вырожденной
# и не вырожденной при != 0
M = np.array([[3, 5, 7, 8], [-1, 7, 0, 1], [0, 5, 3, 2], [1, -1, 7, 4]])
print(np.linalg.det(M))
# 2. Обратная матрица
M = np.array([[3, -3, 1], [-3, 5, -2], [1, -2, 1]])
inv = np.linalg.inv(M)
print(inv)
print(np.dot(inv, M))  # проверка при умножении матрицы на обратную получим единичную
# 3. Ранг матрицы
# Если ранг матрицы 3 x 3 равен 1, то матрицу можно свести к одному вектору и
# мы вообще не потеряем информацию, так как все остальные вектора матрицы
# выводятся из оставшегося вектора.
M = np.array([[3, 5, 7, 8], [-1, 7, 0, 1], [0, 5, 3, 2], [1, -1, 7, 4]])
print(np.linalg.matrix_rank(M))
# 4. СЛАУ
# Смысл:
# Есть система двух уравнений прямых Ax1+By1+C=0 и Gx1+Jy1+K=0
# 1) прямые пересекаются, и система имеет единственное решение (совместна и определенна);
# 2) прямые параллельны, и система не имеет решения (несовместна);
# 3) прямые совпадают, т.с. ранг системы равен единице, и система имеет бесчисленное множество решений (неопределенна).

# Хорошее объяснение СЛАУ http://spacemath.xyz/sistemy-linejnyh-uravnenij/

# x0+2x1−3x2=4
# 2x0+x1+2x2=3
# 3x0−2x1−x2=9

a = [[1, 2, -3],
     [2, 1, 2],
     [3, -2, -1]]

b = [4, 3, 9]

x = LA.solve(a, b)

print(x)
print(np.dot(a, x)) # проверка должно быть [4,3,9]


if __name__ == '__main__':
    pass