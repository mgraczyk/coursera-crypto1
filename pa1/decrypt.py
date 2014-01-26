#! /usr/bin/python2.7

from __future__ import print_function
from ct import *

import operator
import sys

from functools import reduce
from functools import partial

def compose(f, g):
    def composition(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composition

guesses = {
    0: {
        34:'u',
        44:'p',46:'t',
        68:'o',69:'r',70:' ',71:'t',
        78:'b',79:'e'
    },

    1: {
        13:'r',14:'o'
    },
    2: {
        17:'o',19:'t',
        9:'t',10:'h'
    },
    3: {
        20:'c',21:'e',
        35:'n',36:'c',38:'y',39:'p',40:'t',41:'i',42:'o',43:'n',
        49:'r',50:'i',51:'t',53:'m',
        66:'o',
        73:'i',74:'p',81:'t'
    },
    5: {
        30:'r',31:'a',32:'p',33:'h'
    },
    6: {
        82:'r',83:'c',84:'e'
    },
    8: {
        60:'l'
    },
    9: {
        2:'h',3:'e',
        5:'C',6:'o',7:'n',
        22:'t',23:'i',25:'n',
        26:'a',27:'r',28:'y',
        54:'s',55:' ',56:'t',57:'h',58:'e',
        63:' ',64:'o'
    },

    # Don't trust these...
    10: {}
}

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
    return (ord('a') <= c and c <= ord('z')) or (ord('A') <= c and c <= ord('Z'))

get_0th_for_each = partial(map, operator.itemgetter(0))
filter_spaces = partial(filter, xor_is_space)

space_positions = compose(set, compose(compose(get_0th_for_each, filter_spaces), enumerate))

def make_vertical(msg):
    return "\n".join("{} {}".format(l,i) for i,l in enumerate(msg))

def print_msgs(msgs, vertical):
    if vertical:
        msgs = map(make_vertical, msgs)

    for i, msg in enumerate(msgs):
        print("Messages[{}] = \n{}\n".format(i,msg))
  
def decrypt_messages(msgs, key):
    targetPTs = [["*" for i in xrange(len(ct))] for ct in msgs]

    for i, targetStr in enumerate(msgs):
        for idx,v in key.viewitems():
            if idx < len(targetPTs[i]):
                targetPTs[i][idx] = chr(targetStr[idx] ^ v)

    return ["".join(targetPT) for targetPT in targetPTs]

def do_decrypt(msgNum):
    crossXors = [[strxornums(a,b) for b in cts if b is not a] for a in cts]
    spaceSets = map(partial(map, space_positions), crossXors)
    spaceIndices = map(partial(reduce, set.intersection), spaceSets)
    spaceIndices = [reduce(set.intersection, s) for s in spaceSets]

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

    cts_short = cts #[ct[:len(cts[-1])] for ct in cts]

    if msgNum is None:
        toDecrypt = cts_short
    else:
        toDecrypt = (cts_short[int(msgNum)],) 


    messages = decrypt_messages(toDecrypt, key)

    # Print single messages vertically
    print_msgs(messages, len(messages) == 1)


if __name__ == "__main__":
    do_decrypt(sys.argv[1] if len(sys.argv) > 1 else None)
