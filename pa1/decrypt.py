#! /usr/bin/python

from ct import *

import operator
from functools import reduce
from functools import partial

def compose(f, g):
    def composition(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composition

def xor_could_be_space(ch):
    return ord(ch[1]) == 0 or ord(ch[1]) >= 65

def do_decrypt():
    crossXors = [[strxor(a,b) for b in cts] for a in cts]

    spaceIndices = map(
        compose(
            partial(reduce, set.intersection),
            partial(map, compose(
                set,
                    compose(
                        compose(
                            partial(map, operator.itemgetter(0)),
                            partial(filter, xor_could_be_space)),
                        enumerate)))),
        crossXors)
   
    print([indices for indices in spaceIndices])

if __name__ == "__main__":
    do_decrypt()
