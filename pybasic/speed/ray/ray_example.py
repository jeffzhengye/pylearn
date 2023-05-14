import numpy as np
import psutil
import ray
import scipy.signal
from yelib.utils.generic_utils import timeit
num_cpus = psutil.cpu_count(logical=False)

# print('num_cpus (not logical)', num_cpus)

# ray.init(num_cpus=num_cpus)

@timeit
@ray.remote
def f(image, random_filter):
    # Do some image processing.
    return scipy.signal.convolve2d(image, random_filter)[::5, ::5]

filters = [np.random.normal(size=(4, 4)) for _ in range(num_cpus)]

# Time the code below.

image = np.zeros((1500, 1500))
image_id = ray.put(image)

for _ in range(20):
    results = ray.get([f.remote(image_id, filters[i]) for i in range(num_cpus)])
    # print([res.shape for res in results])