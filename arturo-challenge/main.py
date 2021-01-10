from typing import List
from itertools import count, filterfalse

def return_smallest_positive(l: List) -> int:
	return next(filterfalse(set(l).__contains__, count(1)))

if __name__ == "__main__":
	l = [0,1,14,2,5,3,7,8,12]
	r = return_smallest_positive(l)
	print(r)