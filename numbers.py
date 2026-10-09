n = int(input('Введите количество элементов: '))
count = 0
number = 1

while count < n:
    for i in range(number):
        if count < n:
            print(number, end='')
            count += 1
    number += 1

print()
