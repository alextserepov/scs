#!/usr/bin/env python3

import sys

from base64 import (
        b64encode,
        b64decode,
        )

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

class provSigner():
    def provSign(this, filename):
        digest = SHA256.new()
        with open (filename, "r") as provfile:
            digest.update(provfile.read().encode('utf-8'))

        private_key = False
        with open ("private.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

# This needs to be updated to proper PKCS version. (e.g. 11?)
# For now just using PKCS1_v1_5 as nothing else is supported by Pycryptodome.

        signer = PKCS1_v1_5.new(private_key)
        this.sig = signer.sign(digest)
        return (digest, this.sig)

    def saveSignature(this, filename):
        f = open (filename, "wb")
        f.write(this.sig)

    def provVerify(this, digest, sig):
        with open("public.pem", "r") as pubkeyfile:
            public_key = RSA.importKey(pubkeyfile.read())

        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(digest, sig)
        print(verified)
        return verified


t=provSigner()
if (len(sys.argv)<=4 and len(sys.argv)>2):
    if (sys.argv[1]=='sig'):
       (dig, sig) = t.provSign(sys.argv[2])
       t.saveSignature("signature")
    elif (sys.argv[1]=='ver'):
        digest = SHA256.new()
        with open(sys.argv[2], "r") as provfile:
            digest.update(provfile.read().encode('utf-8'))
        with open(sys.argv[3], "rb") as sigfile:
            t.provVerify(digest, sigfile.read())
else:
    print("Usage:")
    print("sing.py sig fname")
    print("sing.py ver fname signature")

