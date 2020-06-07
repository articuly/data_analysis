import random

num1 = 0
num2 = 0

num1 += 10
num2 += -10

num = num1 + num2


def my_sum(num1, num2):
    num2 = num2 - random.randint(0, 10)
    if num1 > num2:
        return num1 + num2
    elif num1 == num2:
        return num1 - num2
    else:
        return num1 / num2


num = my_sum(num1, num2)

num = my_sum(2, num2)
