def is_divisible(n):
    if n % 3 == 0 or n % 5 == 0:
        return True
    else:
        return False

print sum(filter(is_divisible, range(1, 1001)))
