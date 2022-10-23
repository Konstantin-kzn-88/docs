import numpy as np
import math

vtr1 = np.array([10, 20, 30, 40, 50])
vtr2 = np.array([11, 12, 13, 14, 15])

vctr_add = vtr1 + vtr2
print("Сложение двух векторов: ", vctr_add)

vctr_sub = vtr1 - vtr2
print("Вычитание двух векторов: ", vctr_sub)

vctr_mul = vtr1 * vtr2
print("Умножение двух векторов: ", vctr_mul)

vctr_div = vtr1 / vtr2
print("Деление двух векторов: ", vctr_div)

vctr_scal = vtr1.dot(vtr2)
print("Скалярное произведение двух векторов: ", vctr_scal)

vctr_scal = vtr1.dot(5)
print("Скалярное произведение вектора на число: ", vctr_scal)

# длина вектора равна длине отрезка
print(np.linalg.norm(np.array([-5, 4])))
print(math.sqrt(pow((5-0),2)+pow((4-0),2)))

if __name__ == '__main__':
    pass
