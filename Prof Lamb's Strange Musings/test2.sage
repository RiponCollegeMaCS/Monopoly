def is2pow(n):
    while n != 0 and n%2 == 0:
        n = n >> 1
    return n == 1