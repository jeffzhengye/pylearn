from functools import lru_cache

@lru_cache()
def josephus(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2 * josephus(int(n/2)) - 1
    elif n % 2 == 1:
        return 2 * josephus(int(n/2)) + 1


print(josephus(80))