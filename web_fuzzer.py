import requests
import threading
import argparse
from colorama import Fore, Style, init
import sys
import time

init(autoreset=True)

found_items = 0
threads_list = []

def fuzz_url(base_url, word):
    """Δοκιμάζει μία λέξη στο βασικό URL και ελέγχει τον κωδικό απάντησης."""
    global found_items
    
    # Διαμόρφωση του πλήρους URL (π.χ., http://target.com/admin)
    url = f"{base_url.rstrip('/')}/{word.strip()}"
    
    try:
        # 1. Εκτέλεση του HTTP GET request
        response = requests.get(url, timeout=3, allow_redirects=False)
        status_code = response.status_code

        # 2. Έλεγχος των κωδικών απάντησης (HTTP Status Codes)
        if status_code in [200, 204, 301, 302, 307]:
            print(f"{Fore.GREEN}✅ [{status_code}] Found: {url}")
            found_items += 1
        elif status_code == 403:
            print(f"{Fore.YELLOW}⚠️ [{status_code}] Forbidden: {url}")
            found_items += 1
        # 401 Unauthorized (Χρειάζεται Login)
        elif status_code == 401:
            print(f"{Fore.YELLOW}🔑 [{status_code}] Unauthorized: {url}")
            found_items += 1
        # 404 (Not Found) και 5xx (Server Error) τα αγνοούμε
        # else:
            # pass

    except requests.exceptions.RequestException:
        # Αγνοούμε σφάλματα δικτύου ή timeouts για να συνεχίσει η σάρωση
        pass

def main():
    parser = argparse.ArgumentParser(description="Python Web Directory Fuzzer using Threading.")
    parser.add_argument('-t', '--target', required=True, help='Target URL (e.g., http://10.0.0.1/)')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to the wordlist file.')
    parser.add_argument('-th', '--threads', type=int, default=30, help='Number of concurrent threads (Default: 30).')
    args = parser.parse_args()

    print(f"{Fore.CYAN}--- Starting Web Fuzzer on {args.target} ---")
    
    try:
        with open(args.wordlist, 'r') as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}🚨 Error: Wordlist file not found.")
        sys.exit(1)

    print(f"{Fore.CYAN}Total words to test: {len(words)}")

    # Εκτέλεση της σάρωσης με χρήση πολυνηματικότητας
    for i, word in enumerate(words):
        if word.strip():
            thread = threading.Thread(target=fuzz_url, args=(args.target, word.strip()))
            threads_list.append(thread)
            thread.start()
        
        # Περιορισμός του αριθμού των ταυτόχρονα ενεργών νημάτων
        if len(threads_list) >= args.threads:
            # Περιμένουμε τα νήματα που τελειώνουν
            for t in threads_list:
                t.join(timeout=0.1)
            # Φιλτράρουμε τα νήματα που ακόμα τρέχουν
            threads_list[:] = [t for t in threads_list if t.is_alive()]
            
            # Δίνουμε μια μικρή ανάσα
            if len(threads_list) >= args.threads:
                time.sleep(0.1) # Για να μην υπερφορτώσουμε το δίκτυο

    # Περιμένουμε όλα τα νήματα να τελειώσουν στο τέλος
    for thread in threads_list:
        thread.join()

    print(f"\n{Fore.CYAN}--- Fuzzing Finished ---")
    print(f"{Fore.GREEN}Total items found: {found_items}")


if __name__ == "__main__":
    main()
