#! /usr/bin/python2.7

from __future__ import print_function
from ct import *

import operator
from functools import reduce
from functools import partial

def compose(f, g):
    def composition(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composition

def guessed_key(guesses):
    key = {}
    for msgNum, letters in guesses.viewitems():
        for pos, letter in letters.viewitems():
            keyVal = ord(letter) ^ cts[msgNum][pos]
            value = key.get(pos)
            if value is not None:
                if value != keyVal:
                    print("WRONG GUESS at message {}, letter {}".format(msgNum, pos))
                    print("---> {} != {}.".format(chr(keyVal), chr(value)))
            else:
                key[pos] = keyVal

    return key


def xor_is_space(ch):
    c = ch[1]
    return (65 <= c and c <= 90) or (97 <= c and c <= 122)

get_0th_for_each = partial(map, operator.itemgetter(0))
filter_spaces = partial(filter, xor_is_space)

space_positions = compose(set, compose(compose(get_0th_for_each, filter_spaces), enumerate))

def do_decrypt():
    crossXors = [[strxornums(a,b) for b in cts if b is not a] for a in cts]
    spaceSets = map(partial(map, space_positions), crossXors)

    spaceIndices = map(partial(reduce, set.intersection), spaceSets)

    [print(s) for s in spaceIndices]

    key = guessed_key(guesses)

    for (ct, indices) in zip(cts, spaceIndices):
        for i in indices:
            keyVal = ord(" ") ^ ct[i]
            value = key.get(i)
            if value is not None:
                if value != keyVal:
                    print("Mismatch! {} != {}.".format(keyVal, value))
            else:
                key[i] = keyVal
        print("KEY: " + str(key))

    targetPTs = [["*" for i in xrange(len(ct))] for ct in cts]
  
    for i, targetStr in enumerate(cts):
        for idx,v in key.viewitems():
            targetPTs[i][idx] = chr(targetStr[idx] ^ v)

    messages = ["".join(targetPT) for targetPT in targetPTs]

    for i, msg in enumerate(messages):
        print("Messages[{}] = \n{}\n".format(i,msg))
   

if __name__ == "__main__":
    do_decrypt()
