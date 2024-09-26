import os
import csv
import hashlib
from cryptography.fernet import Fernet

KEY_FILE = 'secret.key'
DATA_FILE = 'Encrypt_PW.txt'
CSV_FILE = 'Storage.csv'

def load_key():
    """Load the encryption key from a file."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        raise FileNotFoundError("Key file does not exist.")

def encrypt(data, key):
    """Encrypt data using Fernet with the given key."""
    fernet = Fernet(key)
    return fernet.encrypt(data)

def compute_checksum(data):
    """Compute the SHA-256 checksum of the given data."""
    return hashlib.sha256(data.encode()).hexdigest()

def get_next_id():
    """Determine the next available ID."""
    if not os.path.exists(CSV_FILE):
        return 1  # Start with ID 1 if the file does not exist

    with open(CSV_FILE, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader, None)  # Read the header if present
        next_id = 1
        
        for row in csv_reader:
            if row and row[0].isdigit():
                current_id = int(row[0])
                if current_id >= next_id:
                    next_id = current_id + 1
                    
    return next_id

def main():
    """Main function to handle encryption and CSV file updating."""
    # Load encryption key
    key = load_key()
    
    # Determine the next ID
    next_id = get_next_id()

    # Read the data file and write to CSV
    with open(DATA_FILE, 'r') as data_file, open(CSV_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        lines = data_file.readlines()
        
        for line in lines:
            # Parse email and password
            try:
                email, password = line.strip().split(' ', 1)
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            
            # Encrypt email and password
            encrypted_email = encrypt(email.encode(), key)
            encrypted_password = encrypt(password.encode(), key)
            
            # Compute checksum
            checksum = compute_checksum(email)
            
            # Write to CSV with updated ID
            csv_writer.writerow([next_id, encrypted_email.decode(), encrypted_password.decode(), checksum])
            
            # Increment ID for the next entry
            next_id += 1
        
        # Clear the Encrypt_PW.txt file
        with open(DATA_FILE, 'w') as file:
            file.truncate()

if __name__ == "__main__":
    main()
