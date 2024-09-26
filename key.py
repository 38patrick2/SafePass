# Simple Key generation and management script EZPEZ Fernet
# More comments?


import os
from cryptography.fernet import Fernet
import logging 

KEY_FILE = 'secret.key'

# Configure logging
logging.basicConfig(filename='key_management.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key():
    #Generate a new encryption key.
    return Fernet.generate_key()

def save_key(key):
    #Save the encryption key to a file with appropriate permissions.
    try:
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        # Set file permissions to read/write for the owner only (UNIX)
        os.chmod(KEY_FILE, 0o600)
    except IOError as e:
        logging.error(f"Failed to save key: {e}")
        print("Error saving key. Check logs for details.")

def load_key():
    #Load the encryption key from a file.
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, 'rb') as key_file:
                return key_file.read()
        except IOError as e:
            logging.error(f"Failed to load key: {e}")
            print("Error loading key. Check logs for details.")
            return None
    else:
        key = generate_key()
        save_key(key)
        return key

def rotate_key():
    #Rotate the encryption key.
    new_key = generate_key()
    save_key(new_key)
    logging.info("Key rotated successfully.")
    print("Key rotated successfully.")

def main():
    while True:
        print("\nKey Management")
        print("1. Generate Key")
        print("2. Load Key")
        print("3. Rotate Key")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            key = generate_key()
            save_key(key)
            print("New key generated and saved.")
            logging.info("New key generated and saved.")
        elif choice == "2":
            key = load_key()
            if key:
                print(f"Loaded key (hex): {key.decode()}")
                logging.info("Key loaded successfully.")
        elif choice == "3":
            rotate_key()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
