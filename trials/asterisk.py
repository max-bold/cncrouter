a = [1, 3, 4, 5]

print(a)
print(*a)


def pr(*b):
    print(b)


pr(10, 20, 30, 40)

c = [(1, 2, 5, 7)]
# print(f'{len(c)=}')
pr(c)

n = (10, 20, 30)
a, b, c = n

print(a, b, c)
