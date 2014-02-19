#!/usr/bin/python3

import math

def discrete_log(p, h, g, maxExp=40):
   """ Computes x such that h = g^x mod p 
   """

   B = 2**(int(maxExp/2))

   print("Computing x0s...")
   x0s = tuple(enumerate(tuple((((g**B)**i) % p) for i in range(B))))
   print("Computing x1s...")
   x1s = tuple(enumerate(tuple((h/(g**i) % p) for i in range(B))))

   print("Checking for equality...")
   for x1, exprL in x1s:
       print("Checking x1=={}".format(x1))
       for x0, exprR in x0s:
           if exprL == exprR:
               return x0*B+x1

   raise ValueError("No suitable x0, x1 found!")

def self_test():
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171

    g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568

    h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
  
    xShort = 23232
    x = discrete_log(1938281, 190942, 1737373, 20)
    print("x == {}".format(x))
    assert(xShort == x)
    print("Short test passed!")
    
    x = discrete_log(p, h, g)
    assert(h == (g**x) % p)
    print("x == {}".format(x))
    print("Long test passed!")

if __name__ == "__main__":
    self_test()

