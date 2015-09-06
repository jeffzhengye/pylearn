#import pyximport; pyximport.install(reload_support=True)
import numpy as np
from numpy_array_sum import sum_0, sum_01, sum_1, sum_2,sum_3, sum_4, sum_5, sum_6, sum_7
from profilehooks import profile
# import pyximport; pyximport.install(reload_support=True)

input = np.random.ranf((2001, 200)).astype(np.float32)

def sum_np(vecs):
	"""
	numpy baseline
	"""
	return np.sum(vecs, axis=0)


@profile
def test():
	for i in range(10):
		sum_np(input)
		sum_0(input)
		sum_01(input)
		sum_1(input)
		sum_2(input)
		# sum_3(input)
		# sum_4(input)
		# sum_5(input)
		# sum_7(input)
		# sum_6(input)

test()
