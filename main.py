
# разбивает число и умножает числа пока не останет ся один, пример - 39 ( 3 * 9 = 27, 2 * 7 = 14 , 1 * 4 = 5 ) , ответ - 3
# посчитать количество циклов


import math

count = 0
num = int(input())
while len(str(num)) > 1:
    count += 1
    x = math.prod([int(i) for i in list(str(num))])
    num = x
print(count)