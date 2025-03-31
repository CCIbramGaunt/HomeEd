n = 7
for i in range(0, n):
    for j in range(0, n):
        if (i == 0 or i == n-1 or j == i or j == n-1-i): print('*', end='')
        else: print(' ', end='')
    print()