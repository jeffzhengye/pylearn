import psutil
import ray
import time
import numpy as np

num_cpus = psutil.cpu_count(logical=False)

print('num_cpus (not logical)', num_cpus)

ray.init(num_cpus=2)

# A regular Python function.
def my_function():
    return 1

# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def my_function():
    return 1

# To invoke this remote function, use the `remote` method.
# This will immediately return an object ref (a future) and then create
# a task that will be executed on a worker process.
obj_ref = my_function.remote()

# The result can be retrieved with ``ray.get``.
assert ray.get(obj_ref) == 1

@ray.remote
def slow_function():
    t = np.random.randint(10, size=1)[0]
    print('going to sleep {}s'.format(t))
    time.sleep(t)
    return t

# Invocations of Ray remote functions happen in parallel.
# All computation is performed in the background, driven by Ray's internal event loop.
ret_list = []
for _ in range(4):
    # This doesn't block.
    ret_list.append(slow_function.remote())

print('return 0')

for _ in range(4):
    # This doesn't block.
    ret_list.append(slow_function.remote())

print('return 1')

for task in ret_list:
    r = ray.get(task)
    print('get results', r)

rs = ray.get(ret_list)
print(rs)