class T:
    x = 30


A = T()
B = T()

A.x = 10
B.x = 20


print(A.x, B.x)

C = T()
print(C.x, T.x)
