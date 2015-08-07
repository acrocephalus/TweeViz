import itertools
from itertools import izip_longest

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return list(list(n for n in t if n)
       for t in itertools.izip_longest(*args))