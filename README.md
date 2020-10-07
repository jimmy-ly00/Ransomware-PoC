# Ransomware-PoC
A simple python ransomware PoC that can be used for Atomic Red Team testing for **ATT&CK Technique: Data Encrypted for Impact (T1486)**. The project is built off [CryptSky](https://github.com/deadPix3l/CryptSky) and full credits goes to deadPix3l for his code. The updated code demonstrates a typical ransomware flow and it is just one of many ways to perform ransomware encryption.

 TLDR:
 1. Generates AES key to encrypt local file (hardcoded in PoC).
 2. The attacker's embedded RSA public key (intentionally hardcoded in PoC) is used to encrypt the AES key. The private key is already stored in the attacker's C2 server. The encrypted text is sent to the C2 server and displayed for the victim.
 3. Ransom note is shown. When the ransom is paid, a decryptor is provided. 
 
**Warning**: Be extra careful of running the program as it will modify files. Ensure the path is correct and be wary in running with administrative privileges.

# Supported
* python3 (python2 for Linux/macOS should work)
* Windows, Linux and macOS

# How to run
Install dependencies:
```bash
pip3 install pycryptodome
```

Default:
```
Encrypt: python3 main.py -e
Decrypt: python3 main.py -d
```

Windows with specific path:
```
Encrypt: python3 main.py -p "C:\users\jimmy\desktop\test_ransomware" -e
Decrypt: python3 main.py -p "C:\users\jimmy\desktop\test_ransomware" -d
```

Linux / macOS with specific path:
```
Encrypt: python3 main.py -p "/home/jimmy/test_ransomware" -e
Decrypt: python3 main.py -p "/home/jimmy/test_ransomware" -d
```

Variables to change:
* Ransomware Extension [default: .wasted for WastedLocker]

NB: As this is simply a PoC for Atomic Red Team, there is no real need to change the keys or other variables.

# Standalone Executable
Tested with python 2.7 with pyinstaller 3.6 and python 3.7 with pyinstaller 4.0. Please note that python 3.8 with pyinstaller 4.0 have known issues as this was incompatible with macOS.

Windows and Linux:
```bash
pip3 install pyinstaller
pyinstaller --onefile main.py or py -m PyInstaller --onefile main.py
```

macOS:
```
(python 3.7)
python3 -m pip install  pyinstaller
pyinstaller --onefile main.py

(python 2.7)
pip install -I pyinstaller==3.6
python -m PyInstaller --onefile main.py
```

See `/bin` folder for binaries.

Windows with specific path:
```
Encrypt: main.exe -p "C:\users\jimmy\desktop\test_ransomware" -e
Decrypt: main.exe -p "C:\users\jimmy\desktop\test_ransomware" -d
```

Linux with specific path:
```
Encrypt: ./main -p "/home/jimmy/test_ransomware" -e
Decrypt: ./main -p "/home/jimmy/test_ransomware" -d
```

macOS with specific path:
```
Encrypt: ./main_macos_py2 -p "/Users/jimmy/test_ransomware" -e
Decrypt: ./main_macos_py2 -p "/Users/jimmy/test_ransomware" -d
```

# Demo
![Ransomware-PoC](/demo/download.gif)

# Additional Features
* Added RSA asymmetric encryption of the AES key.
* Added autodetection on Windows, Linux or macOS.
* Added path argument to specify a directory.
* Fixed handling of renaming files with adding/removing of the ransomware extension.

# Credit
Credit goes to deadPix3l (https://github.com/deadPix3l/CryptSky) and contributers.
