print('Программа позволяет узнать, сколько раз \nв заданном диапазоне встречается выбранное число.\n')

num_start = int(input('Введите начальное число диапазона: '))
num_finish = int(input('Введите конечное число диапазона (не более 1 миллиона): '))
num_look = input('Задайте однозначное число, которое необходимо посчитать: ')

if len(num_look) == 1:
    x = str(list(range(num_start, num_finish + 1))).count(str(num_look))
else:
    x = 0
    range_in_str = str(list(range(num_start, num_finish + 1)))  # строка поиска из заданного диапазона
    len_slice = len(num_look)                                   # длина среза для поиска

    for i in range(len(range_in_str)):
        print(f'num_look = {num_look}, slice = {range_in_str[i:i + len_slice]}')
        if range_in_str[i:i + len_slice] in num_look:
            x += 1

print('В последовательности чисел от ', num_start, ' до ', num_finish, ' цифра: ', num_look, 'встречается ', x,
      " раз(а)")
