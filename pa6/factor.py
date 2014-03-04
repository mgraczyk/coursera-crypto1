#!/usr/bin/python

import gmpy2

from gmpy2 import mpz
from gmpy2 import powmod
from gmpy2 import isqrt
from gmpy2 import isqrt_rem
from gmpy2 import div
from gmpy2 import invert

from math import ceil
from binascii import unhexlify

import challenges

def ceil_sqrt(x):
    s,t = isqrt_rem(x)
    return s + (1 if t else 0)

def check_factors(p,q,N):
    return p*q == N

def factor_with_average(A, N):
    x = isqrt(A**2 - N)
    return (A - x, A + x)

def check_ch3(i,A,N):
    p,q = (div(A + i - 1,3), div(A - i,2))
    if check_factors(p,q,N):
        return p,q

    p,q = (div(A - i,3), div(A + i - 1,2))
    if check_factors(p,q,N):
        return p,q

    return None
    

def ch3_factor(N):
    """ Valid when |3p - 2q| < N^(1/4)
    """

    A = ceil_sqrt(6*N)

    # let M = (3p+2q)/2
    # M is not an integer since 3p + 2q is odd
    # So there is some integer A = M + 0.5 and some integer i such that
    # 3p = M + i - 0.5 = A + i - 1
    # and
    # 2q = M - i + 0.5 = A - i
    #
    # N = pq = (A-i)(A+i-1)/6 = (A^2 - i^2 - A + i)/6
    # So 6N = A^2 - i^2 - A + i
    # i^2 - i = A^2 - A - 6N 

    # Solve using the quadratic equation!
    a = mpz(1)
    b = mpz(-1)
    c = -(A**2 - A - 6*N)

    det = b**2 - 4*a*c

    roots = (div(-b + isqrt(b**2 - 4*a*c), 2*a),
         div(-b - isqrt(b**2 - 4*a*c), 2*a))


    for i in roots:
        if i >= 0:
            f = check_ch3(i,A,N)
            if f:
                return f

    # We should have found the root
    assert(False)

def factor(N):
    N = mpz(N)

    # Valid when |p-q| < 2N^(1/4)
    A = ceil_sqrt(N)
    p,q = factor_with_average(A, N)
    if check_factors(p,q,N):
        return (p,q)

    # Valid when |p-q| < 2^11 * N^(1/4)
    for i in range(2**20):
        A += 1
        p,q = factor_with_average(A, N)
        if check_factors(p,q,N):
            return (p,q)

    return ch3_factor(N)

def decrypt_RSA(ciphertext, pk):
    N, e = pk

    p,q = factor(N)
    phiN = N - p - q + 1

    d = invert(e, phiN)

    return powmod(ciphertext, d, N)


def self_test():
    Ns = challenges.Ns

    for num,N in enumerate(Ns):
        p,q = factor(N)

        if check_factors(p,q,N):
            print("N[{}]: Found p = \n{}\n".format(num, min(p,q)))
        else:
            print("ERROR: Incorrectly factored N[{}]!".format(num))

    # Find the plaintext
    pt = decrypt_RSA(challenges.ciphertext_1, (challenges.N_1, challenges.e_1))
    ptHex = hex(pt)
    pos = ptHex.find("00")
    print("Plaintext:")
    print(ptHex)
    print("Message:")
    print(unhexlify(ptHex[pos+2:]))

if __name__ == "__main__":
    self_test()


