import os
import random
from pyfiglet import Figlet
import base64
import hashlib
import string
import time
import sys
from Crypto.Cipher import AES
from colorama import init, Fore, Style
import subprocess

init(autoreset=True)

def print_menu_title():
    f = Figlet(font='slant')
    print(Fore.CYAN + Style.BRIGHT + f.renderText('Bread Logger'))
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return nonce, ciphertext, tag
def decrypt_data(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode()
def obfuscate(data, key):
    encrypted_data = encrypt_data(data, key)
    encoded_data = base64.b64encode(encrypted_data[0] + encrypted_data[1] + encrypted_data[2]).decode()
    return encoded_data
def deobfuscate(data, key):
    decoded_data = base64.b64decode(data.encode())
    nonce, ciphertext, tag = decoded_data[:16], decoded_data[16:-16], decoded_data[-16:]
    decrypted_data = decrypt_data(nonce, ciphertext, tag, key)
    return decrypted_data
def save_master_password(master_password, filename, key):
    with open(filename, 'r') as file:
        data = file.read()
        
    with open(filename, 'w') as file:
        obfuscated_master_password = obfuscate(master_password, key)
        file.write(f"{obfuscated_master_password}\n{data}")
def check_master_password(master_password, filename, key):
    with open(filename, 'r') as file:
        obfuscated_stored_master_password = file.readline().strip()

    stored_master_password = deobfuscate(obfuscated_stored_master_password, key)
    return master_password == stored_master_password
def save_password(title, username, password, filename, key):
    with open(filename, 'a') as file:
        obfuscated_title = obfuscate(title, key)
        obfuscated_username = obfuscate(username, key)
        obfuscated_password = obfuscate(password, key)
        file.write(f"{obfuscated_title}:{obfuscated_username}:{obfuscated_password}\n")
def list_passwords(filename, key):
    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                obfuscated_title, obfuscated_username, obfuscated_password = line.strip().split(':')
                title = deobfuscate(obfuscated_title, key)
                username = deobfuscate(obfuscated_username, key)
                password = deobfuscate(obfuscated_password, key)
                print(f"Title: {title}, Username: {username}, Password: {password}")
def generate_random_password(length=14):  
    if length < 14:
        print("Error: Password length increased to a minimum of 14 characters.")
        length = 14

    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_generated_password(filename, key, generated_password):
    title = input("Enter the title for the password: ")
    username = input("Enter the username: ")
    save_password(title, username, generated_password, filename, key)
    print(f"Generated Password: {generated_password}")
    print("Password saved successfully!")
    input("Press Enter to continue...")
def update_password(filename, key):
    clear_screen()
    print(f"-=-=-PASSWORD LIST-=-=-")
    list_passwords(filename, key)
    title_to_update = input("Enter the title for which password to update: ")

    with open(filename, 'r') as file:
        lines = file.readlines()
    password_found = False
    for i, line in enumerate(lines):
        if ':' in line:
            obfuscated_title, obfuscated_username, obfuscated_password = line.strip().split(':')
            title = deobfuscate(obfuscated_title, key)
            if title == title_to_update:
                password_found = True
                username = deobfuscate(obfuscated_username, key)
                password = deobfuscate(obfuscated_password, key)
                clear_screen()
                print(f"-=-=-UPDATING PASSWORD-=-=-")
                print(f"\nUpdating Password\nTitle: {title}, Username: {username}, Password: {password}\n")
                new_title = input("Enter a new title or press enter to continue: ") or title
                new_username = input("Enter a new username or press enter to continue: ") or username
                generate_new_password = input("Do you want to generate a random password? (yes/no): ")
                if generate_new_password.lower() == 'yes':
                    length = int(input("Enter the length of the new password: "))
                    new_password = generate_random_password(length)
                    print("Password updated successfully!")
                    time.sleep(2)
                else:
                    new_password = input("Enter the new password (press Enter to keep the same): ") or password
                    print("Password updated successfully!")
                    time.sleep(2)
                lines[i] = f"{obfuscate(new_title, key)}:{obfuscate(new_username, key)}:{obfuscate(new_password, key)}\n"
                with open(filename, 'w') as file:
                    file.writelines(lines)
                break

    if not password_found:
        print(f"No password found for title '{title_to_update}'. No password updated.")
def delete_password(filename, key):
    list_passwords(filename, key)
    title_to_delete = input("Enter the title for which password to delete: ")
    with open(filename, 'r') as file:
        lines = file.readlines()
    password_found = False
    for i, line in enumerate(lines):
        if ':' in line:
            obfuscated_title, _, _ = line.strip().split(':')
            title = deobfuscate(obfuscated_title, key)
            if title == title_to_delete:
                password_found = True
                confirmation = input(f"Are you sure you want to delete the password for '{title}'? (yes/no): ")
                if confirmation.lower() == 'yes':
                    del lines[i]
                    with open(filename, 'w') as file:
                        file.writelines(lines)
                    print("Password deleted successfully!")
                else:
                    print("Password not deleted.")
                break

    if not password_found:
        print(f"No password found for title '{title_to_delete}'. No password deleted.")
def restart_script():
    python = sys.executable
    script = os.path.abspath(__file__)
    args = [python, script] + sys.argv[1:]
    subprocess.run(args)
    sys.exit()

def delete_password_file(filename):
    os.remove(filename)
    print("Password file deleted successfully!")
    time.sleep(2)

def main():
    from Crypto.Cipher import AES

    filename = "passwords.txt"
    key = hashlib.sha256("your_secret_salt".encode()).digest()

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            print_menu_title()
            master_password = input(Fore.GREEN + "Set a master password: ")
            save_master_password(master_password, filename, key)

    clear_screen()
    print_menu_title()
    master_password = input(Fore.GREEN + "Enter your master password: ")
    if not check_master_password(master_password, filename, key):
        print(Fore.RED + "Incorrect master password. Exiting...")
        return
    while True:
        clear_screen()
        print_menu_title()
        print(Fore.YELLOW + "1. List all passwords")
        print(Fore.YELLOW + "2. Add a new password")
        print(Fore.YELLOW + "3. Generate and save a new password")
        print(Fore.YELLOW + "4. Update an existing password")
        print(Fore.YELLOW + "5. Delete a password")
        print(Fore.YELLOW + "6. Delete password file and restart")
        print(Fore.YELLOW + "7. Exit")
        choice = input(Fore.GREEN + "Enter your choice: ")
        if choice == '1':
            clear_screen()
            print(f"-=-=-PASSWORD LIST-=-=-")
            list_passwords(filename, key)
            input("\nPress Enter to continue...")
        elif choice == '2':
            title = input("Enter the title for the password: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(title, username, password, filename, key)
            print("Password saved successfully!")
            time.sleep(2)
        elif choice == '3':
            generated_password = generate_random_password()
            save_generated_password(filename, key, generated_password)
            time.sleep(2)
        elif choice == '4':
            update_password(filename, key)
        elif choice == '5':
            delete_password(filename, key)
            time.sleep(2)
        elif choice == '6':
            confirmation = input("Are you sure you want to delete the password file and restart? (yes/no): ")
            if confirmation.lower() == 'yes':
                delete_password_file(filename)
                restart_script()
            else:
                print("Operation canceled.")
                time.sleep(2)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    main()
