#!/usr/bin/python3

import Crypto.Cipher.AES as AES

from itertools import islice
from itertools import chain
from itertools import repeat
from itertools import starmap

from functools import partial

import operator

def compose(f, g):
    def composition(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composition

def xor_block(left, right):
    return map(operator.xor, left, right)

def to_bytes(cnt, val):
    return bytes((val & (0xFF << pos*8)) >> pos*8 for pos in range(cnt))

def from_bytes(val):
    if val is None:
        return None

    try:
        return int(val)
    except:
        pass

    result = 0
    m = 1
    for b in val:
        result += m*b
        m *= 256

    return result

class CBCCipher(object):
    def __init__(self, blockCipher, key):
        self._cipher = blockCipher.new(key)

    def get_block_size(self):
        return self._cipher.block_size

    def encrypt(self, plainText, IV):
        blockSZ = self.get_block_size()

        IV = bytes(IV)
        if len(IV) != blockSZ:
            raise ValueError("Bad IV")

        if not plainText:
            return bytes()

        plainText = bytes(plainText)
        padLen = (blockSZ - len(plainText) % blockSZ)
        plainText = plainText + bytes([padLen]*padLen)

        cipherText = bytearray(blockSZ + len(plainText))
        cipherText[0:blockSZ] = IV

        for start in range(blockSZ, len(cipherText), blockSZ):
            end = start + blockSZ
            cipherText[start:end] = self._cipher.encrypt(
                    bytes(xor_block(
                        islice(plainText, start-blockSZ, start), islice(cipherText, start-blockSZ, start))))
       
        return cipherText

    def decrypt(self, cipherText):
        blockSZ = self.get_block_size()

        if not cipherText:
            return bytes()

        cipherText = bytes(cipherText)
        IV = islice(cipherText, blockSZ)

        ctWithPad = bytearray(chain.from_iterable(
            starmap(partial(map, operator.xor), (
                (islice(cipherText, start-blockSZ, start),
                self._cipher.decrypt(cipherText[start:start+blockSZ]))
                    for start in range(blockSZ, len(cipherText), blockSZ)))))

        ct = ctWithPad[0:-ctWithPad[-1]]
        return ct

class CTRCipher(object):
    def __init__(self, blockCipher, key):
        self._cipher = blockCipher.new(key)

    def get_block_size(self):
        return self._cipher.block_size

    def encrypt(self, plainText, IV, catIV=True):
        blockSZ = self.get_block_size()

        IV = bytes(IV)
        if len(IV) != blockSZ:
            raise ValueError("Bad IV")

        if not plainText:
            return bytes()

        cipherIn = (bytes(b) for b in self._get_cipher_input_add(IV, len(plainText)))

        blocks = map(xor_block,
                map(self._cipher.encrypt, cipherIn),
                (islice(plainText, start, start+blockSZ)
                    for start in range(0, len(plainText), blockSZ)))

        ct = bytes(chain.from_iterable(blocks))
        
        if catIV:
            return IV + ct[:len(plainText)]
        else:
            return (IV, ct[:len(plainText)])

    def decrypt(self, cipherText):
        blockSZ = self.get_block_size()
        IV, pt = self.encrypt(cipherText[blockSZ:], cipherText[:blockSZ], False)
        return pt

    def _combine_iv_ctr(self, IV, ctr):
        return map(operator.add, left, right)

    def _get_cipher_input_add(self, IV, msgLen):
        blockSZ = self.get_block_size()
        blocks = int((msgLen + blockSZ - 1)/blockSZ)
        return map(compose(reversed, partial(to_bytes, blockSZ)),
                starmap(operator.add, enumerate(repeat(from_bytes(reversed(IV)), blocks))))

    # Looks like IV is used with add, not xor
    #def _get_cipher_input_xor(self, IV, msgLen):
        #blockSZ = self.get_block_size()
        #blocks = int((msgLen + blockSZ - 1)/blockSZ)
        #return map(bytes,
                #map(partial(map, operator.xor),
                    #repeat(IV), (reversed(to_bytes(blockSZ, i)) for i in range(0, blocks))))

def self_test():
    from binascii import unhexlify
    from binascii import hexlify
    tests = (
            {
                "key": unhexlify("140b41b22a29beb4061bda66b6747e14"),
                "cipher": partial(CBCCipher, AES),
                "ciphertexts": map(unhexlify, ("4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81", "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"))
            },
            {
                "key": unhexlify("36f18357be4dbd77f050515c73fcf9f2"),
                "cipher": partial(CTRCipher, AES),
                "ciphertexts": map(unhexlify, ("69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329", "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"))
            }
    )

    for test in tests:
        cipher = test["cipher"](test["key"])
        for ct in test["ciphertexts"]:
            pt = cipher.decrypt(ct)
            ctFromPt = cipher.encrypt(pt, ct[:cipher.get_block_size()])

            try:
                print("Decrypted {} -> {}".format(hexlify(ct[:5]), pt.decode('utf-8')))
            except UnicodeDecodeError as e:
                print("ERROR: Bad decrypt. {}".format(e)) 

            if ctFromPt != ct:
                print("ERROR: Round trip ciphertext -> plaintext -> re-ciphertext failed.")
                print("CT = {}".format(ct))
                print("PT = {}".format(pt))
                print("RT = {}".format(ctFromPt))

            

if __name__ == "__main__":
    self_test()
