#!/usr/bin/env python3

## find your curve
# openssl ecparam -list_curves
#
## generate a private key for a curve
# openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
#
## generate corresponding public key
# openssl ec -in private-key.pem -pubout -out public-key.pem
##

import sys

from base64 import (
        b64encode,
        b64decode,
        )

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS



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

class provSignerECC():
    def provSign(this, fileName, keyFile):
        print ("fileName: "+fileName)
        print ("keyFile: "+keyFile)
        key = ECC.import_key(open(keyFile).read())
        digest = SHA256.new(open(fileName).read().encode('utf-8'))
        signer = DSS.new(key, 'fips-186-3')
        this.sig = signer.sign(digest)
        return (digest, this.sig)

    def saveSignature(this, filename):
        f = open (filename, "wb")
        f.write(this.sig)
        f.close()

    def provVerify(this, fileName, sigFile, keyFile):
        print ("fileName: "+fileName)
        print ("sigFile: "+sigFile)
        print ("keyFile: "+keyFile)
        key = ECC.import_key(open(keyFile).read())
        digest = SHA256.new(open(fileName).read().encode('utf-8'))
        verifier = DSS.new(key, 'fips-186-3')
        try:
            verifier.verify(digest, open(sigFile, "rb").read())
            print ("True")
            return True
        except ValueError:
            print ("False")
            return False

t=provSignerECC()

if (len(sys.argv)<=5 and len(sys.argv)>2):
    if (sys.argv[1]=='sig'):
        (dig, sig) = t.provSign(sys.argv[2], sys.argv[3])
        t.saveSignature("signature")
    elif (sys.argv[1]=='ver'):
        t.provVerify(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("Usage:")
    print("sing.py sig fname keyfile")
    print("sing.py ver fname signature keyfile")


#t=provSigner()
#if (len(sys.argv)<=4 and len(sys.argv)>2):
#    if (sys.argv[1]=='sig'):
#       (dig, sig) = t.provSign(sys.argv[2])
#       t.saveSignature("signature")
#    elif (sys.argv[1]=='ver'):
#        digest = SHA256.new()
#        with open(sys.argv[2], "r") as provfile:
#            digest.update(provfile.read().encode('utf-8'))
#        with open(sys.argv[3], "rb") as sigfile:
#            t.provVerify(digest, sigfile.read())
#else:
#    print("Usage:")
#    print("sing.py sig fname")
#    print("sing.py ver fname signature")

