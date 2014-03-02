#!/usr/bin/python

import gmpy2

from gmpy2 import mpz

from math import ceil

import challenges

def sqrt_ceil(x):
    (s,t) = x.isqrt_rem()
    return s + (1 if t else 0)

def factor(N):
    N = mpz(N)

    return (1,2)

def check_factors(p,q,N):
    return p*q == N

def self_test():
    Ns = challenges.Ns

    for num,N in enumerate(Ns):
        (p,q) = factor(N)

        if check_factors(p,q,N):
            print("N[{}]: Found p = \n{}\n".format(num, min(p,q)))
        else:
            print("ERROR: Incorrectly factored N[{}]!".format(num))


if __name__ == "__main__":
    self_test()


