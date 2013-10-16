import multiprocessing

def is_divisible(n):
    if n % 3 == 0 or n % 5 == 0:
        return True
    else:
        return False

def sum_divisibles(ns):
    return sum(filter(is_divisible, ns))

pool = multiprocessing.Pool() # Create a group of CPUs to run on
partial_sums = pool.map(sum_divisibles, [range(1, 501), range(501, 1001)])
print sum(partial_sums)
