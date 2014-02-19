#!/usr/bin/python

import sys
import math
import gmpy2

from gmpy2 import mpz
from gmpy2 import invert
from gmpy2 import powmod
from gmpy2 import divm

def compute_x0s(p,h,g,B):
   return ((i, powmod(g, B*i, p)) for i in range(B))

def discrete_log(p, h, g, maxExp=40):
   """ Computes x such that h = g^x mod p 
   """

   B = mpz(2**(int(maxExp/2)))
   
   g = mpz(g)
   h = mpz(h)
   p = mpz(p)

   print("Computing x1s...")
   x1s = { divm(h, powmod(g,i,p), p) : i for i in range(B) }

   print("Checking for equality...")
   for x0, exprR in compute_x0s(p,h,g,B):
       x1 = x1s.get(exprR)
       if x1 is not None:
           print("Found values!")
           print("x0 = {}".format(x0))
           print("x1 = {}".format(x1))
           return mpz(x0)*B+mpz(x1)

   raise ValueError("No suitable x0, x1 found!")

def self_test():
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171

    g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568

    h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
  
    print("Running tiny test")
    xTiny = 3
    x = discrete_log(97, 20, 57, 6)
    print("x == {}".format(x))
    assert(xTiny == x)
    print("Tiny test passed!")
    print("")

    print("Running short test")
    xShort = 23232
    x = discrete_log(1938281, 190942, 1737373, 16)
    print("x == {}".format(x))
    assert(xShort == x)
    print("Short test passed!")
    print("")
    
    print("Running long test")
    x = discrete_log(p, h, g, 40)
    assert(h == powmod(g,x,p))
    print("x == {}".format(x))
    print("Long test passed!")
    print("")

if __name__ == "__main__":
    self_test()

