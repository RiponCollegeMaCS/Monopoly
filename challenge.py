# 5 = buzz
# 3 = fizz

numbers = []

for i in range(1, 100 + 1):
    if i % 15 == 0:
        numbers.append('fizz buzz')
    elif i % 3 == 0:
        numbers.append('fizz')
    elif i % 5 == 0:
        numbers.append('buzz')
    else:
        numbers.append(i)

for element in numbers:
    print(element)


