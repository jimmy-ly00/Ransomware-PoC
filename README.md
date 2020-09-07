# Ransomware-PoC
A simple python ransomware PoC that can be used for Atomic Red Team testing for **ATT&CK Technique: Data Encrypted for Impact (T1486)**. The updated code demonstrates a typical ransomware flow. It uses AES encryption to encrypt the local files for speed reasons. The AES key is then encrypted with RSA asymmetric encryption using the RSA's public key. The RSA's private key and/or encrypted AES key is then sent to the C2. If the encrypted AES is not sent, then the victim will have to provide it. When the ransom is paid, the attacker will then provide the private key to decrypt the AES key and thus decrypt the encrypted files. More simply, a decryptor is sent to the victims which will perform those actions automatically. 

**Warning**: Be extra careful of running the program as it will modify files. Ensure the path is correct and be wary in running with administrative privileges.

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

Linux / MacOS with specific path:
```
Encrypt: python3 main.py -p "/home/jimmy/test_ransomware" -e
Decrypt: python3 main.py -p "/home/jimmy/test_ransomware" -d
```

Variables to change:
* Ransomware Extension [default: .wasted for WastedLocker]

NB: As this is simply a PoC for Atomic Red Team, there is no real need to change the keys or other variables.

# Standalone Executable
Use pyinstaller:
```bash
pip3 install pyinstaller
pyinstaller --onefile main.py or py -m PyInstaller --onefile main.py
```
See `/bin` folder for binaries.

# Additional Features
* RSA asymmetric encryption of the AES keyif s
* Autodetects Windows, Linux or MacOS
* Fixed handling of renaming files with a ransomware extension

# Credit
Credit goes to deadPix3l (https://github.com/deadPix3l/CryptSky) and contributers.
