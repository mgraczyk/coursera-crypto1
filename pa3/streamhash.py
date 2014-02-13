#! /usr/bin/python
import os
import mmap
import binascii

from Crypto.Hash.SHA256 import SHA256Hash

class StreamHash(object):
    def __init__(self, hashClass=None):
        if not hashClass:
            hashClass = SHA256Hash

        self._hashClass = hashClass
        self._blockSZ = 1024

    def hash(self, filePath):
        with open(filePath, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                return self._hash_bytes(mm)

    def _hash_bytes(self, fileBytes):
        blocks, lastSZ = divmod(len(fileBytes), self._blockSZ)
        
        start = len(fileBytes) - lastSZ
        end = len(fileBytes)

        currHash = bytes()
        while start >= 0:
            block = fileBytes[start:end] + currHash
            hashObj = self._hashClass()
            hashObj.update(block)
            currHash = hashObj.digest()

            end = start
            start -= self._blockSZ

        return currHash


def self_test(testsPath):
    from os import listdir
    for f in listdir(testsPath):
        # Verify that the name matches the hash
        try:
            sh = StreamHash()
            hashVal = sh.hash(os.path.join(testsPath, f)) 
            hashHex = binascii.hexlify(hashVal).decode()
            if hashHex == f:
                print("MATCH {}".format(f))
            else:
                print("NO MATCH {} != {}".format(f, hashHex))
        except Exception as e:
            print("ERROR {} -> {}".format(f, e))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sh = StreamHash()
        print(binascii.hexlify(sh.hash(sys.argv[1])).decode())
    else:
        self_test("files")

