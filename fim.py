import hashlib
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Συνάρτηση που υπολογίζει το SHA-256 Hash ενός αρχείου
def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Διαβάζουμε το αρχείο σε κομμάτια (chunks) για ταχύτητα
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def monitor_files(file_list):
    print(f"{Fore.CYAN}--- Starting File Integrity Monitor (FIM) ---")
    print(f"{Fore.CYAN}Calculating initial baselines...")
    
    # 1. Αποθήκευση των αρχικών Hashes (Baseline)
    baseline = {}
    for f in file_list:
        file_hash = calculate_file_hash(f)
        if file_hash:
            baseline[f] = file_hash
            print(f"{Fore.GREEN}✅ Baseline recorded for {f}")
        else:
            print(f"{Fore.RED}⚠️ File not found: {f}")

    print(f"\n{Fore.YELLOW}--- Monitoring started. Press Ctrl+C to stop ---")

    # 2. Συνεχής Έλεγχος (Loop)
    try:
        while True:
            time.sleep(2) # Έλεγχος κάθε 2 δευτερόλεπτα
            
            for filepath, original_hash in list(baseline.items()):
                current_hash = calculate_file_hash(filepath)
                
                # Περίπτωση 1: Το αρχείο διαγράφηκε
                if current_hash is None:
                    print(f"{Fore.RED}🚨 ALERT: File deleted! -> {filepath}")
                    del baseline[filepath] # Σταματάμε να το ελέγχουμε
                
                # Περίπτωση 2: Το Hash άλλαξε (Το αρχείο πειράχτηκε)
                elif current_hash != original_hash:
                    print(f"{Fore.RED}🚨 SECURITY ALERT: File Integrity Compromised! -> {filepath}")
                    print(f"   Original Hash: {original_hash}")
                    print(f"   New Hash:      {current_hash}")
                    
                    # Ενημέρωση του baseline για να μην χτυπάει συνέχεια
                    baseline[filepath] = current_hash 

    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}--- Monitoring stopped ---")

# --- Main ---
if __name__ == "__main__":
    # Δημιούργησε ένα αρχείο για δοκιμή στον ίδιο φάκελο
    # Π.χ. touch secret.txt
    files_to_monitor = ["secret.txt", "passwords.txt"] 
    
    monitor_files(files_to_monitor)
