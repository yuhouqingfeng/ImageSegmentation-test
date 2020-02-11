# 一到一百相加的和：
def sum():
    sum = 0
    for n in range(1, 101):
        sum = sum + n
    return sum


print('一到一百相加的和是:', sum())