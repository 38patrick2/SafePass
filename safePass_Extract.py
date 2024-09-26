import os
import csv
import hashlib
from cryptography.fernet import Fernet

KEY_FILE = 'secret.key'
DATA_FILE = 'Decrypted_PW.txt'
CSV_FILE = 'Storage.csv'

def load_key():
    # Load the encryption key from a file
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        raise FileNotFoundError("Key file does not exist.")

def decrypt(encrypted_data, key):
    # Decrypt data using Fernet with the given key
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

def compute_checksum(data):
    # Compute the SHA-256 checksum of the given data
    return hashlib.sha256(data.encode()).hexdigest()

def main():
    key = load_key()

    # Read email from Decrypted_PW.txt
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} does not exist.")

    with open(DATA_FILE, 'r') as file:
        lines = file.readlines()
        email_line = next((line for line in lines if line.startswith('Email:')), None)
        password_line = next((line for line in lines if line.startswith('Password:')), None)
        
        if not email_line or not password_line:
            raise ValueError("Decrypted_PW.txt must contain both 'Email:' and 'Password:' lines.")
        
        email = email_line.split(':', 1)[1].strip()
        password_placeholder = password_line.strip()  # Password is to be filled in

        # Compute checksum of the provided email
        checksum = compute_checksum(email)
        print(f"Extracted email: '{email}'")
        print(f"Computed checksum: '{checksum}'")

        # Load and search CSV file for the matching checksum
        found = False
        with open(CSV_FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)  # Skip header row
            for row in csv_reader:
                if len(row) != 4:
                    continue
                
                stored_checksum = row[3]
                if stored_checksum == checksum:
                    encrypted_password = row[2]
                    decrypted_password = decrypt(encrypted_password.encode(), key)
                    
                    # Write decrypted password to Decrypted_PW.txt
                    with open(DATA_FILE, 'w') as file:
                        file.write(f"Email: {email}\nPassword: {decrypted_password}")
                    
                    found = True
                    break
        
        if not found:
            raise ValueError("No matching checksum found in Storage.csv.")

if __name__ == "__main__":
    main()
