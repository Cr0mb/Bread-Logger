![image](https://github.com/Cr0mb/Bread-Logger/assets/137664526/0def9d87-f762-4bd4-9062-10425dfc0585)


# Bread Logger
Bread Logger is a Python script that serves as a password manager and generator. 
It encrypts and stores passwords in a file on your system, allowing you to manage them securely from your terminal. 
You can also generate random passwords using the script.

### Features
- Encryption: Passwords are encrypted using AES encryption with a master password.
- Password Generation: Generate random passwords of desired length.
- Password Management: Add, update, delete, and list stored passwords.
- Terminal Interface: User-friendly terminal-based interface.
### Prerequisites
Before running the script, ensure you have the following dependencies installed:

-Python 3.x
-pyfiglet
-colorama
-pycrypto
You can install the dependencies using pip:
```
pip install pyfiglet colorama pycrypto
```
### Usage
1. Clone this repository to your local machine:
```
git clone https://github.com/Cr0mb/Bread-Logger.git
```
2. Navigate to the directory where you cloned the repository:
```
cd Bread-Logger
```
3. Run the script:
```
python BreadLog.py
```
4. Follow the on-screen instructions to manage your passwords.
### Security
- Master Password: You will be prompted to set a master password when running the script for the first time. This password is used for encryption and decryption of stored passwords.
- Encryption: Passwords are encrypted using AES encryption with a generated key derived from the master password and a secret salt.

This script was created by Cr0mb.
