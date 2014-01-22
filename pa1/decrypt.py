#! /usr/bin/python2.7

from ct import *

import operator
from functools import reduce
from functools import partial

def compose(f, g):
    def composition(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composition

def xor_could_be_space(ch):
    #return ord(ch[1]) == 0 or ord(ch[1]) >= 65
    return ord(ch[1]) >= 65

def do_decrypt():
    keyLen = max(len(a) for a in cts)
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

    key = ["\x00" for i in xrange(keyLen)]

    for (ct, indices) in zip(cts, spaceIndices):
        print("KEY: " + "".join(key).encode('hex'))
        for i in indices:
            key[i] = strxor(" ", ct[i])

    targetStr = cts[-1]
    targetPT = encrypt("".join(key)[0:len(targetStr)], targetStr)

    print("".join(targetPT[i] if key[i] else "_" for i in xrange(len(targetPT))))
   

if __name__ == "__main__":
    do_decrypt()
