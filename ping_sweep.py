import subprocess
import threading
import ipaddress
import sys
from colorama import Fore, Style, init

init(autoreset=True)

# Παγκόσμια λίστα για τις ενεργές IP
live_hosts = []

# Συνάρτηση που εκτελεί το ping
def ping_host(ip):
    # -c 1: Στέλνει 1 πακέτο
    # -w 1: Περιμένει 1 δευτερόλεπτο για απάντηση
    command = ['ping', '-c', '1', '-w', '1', str(ip)]

    # Εκτέλεση της εντολής ping
    # suppress output (stdout)
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Ο κωδικός εξόδου 0 σημαίνει επιτυχία (δηλαδή, η IP απάντησε)
    if result.returncode == 0:
        print(f"{Fore.GREEN}✅ Host Active: {ip}")
        live_hosts.append(str(ip))
    else:
        # print(f"{Fore.RED}❌ Host Down: {ip}") # (Πολύ θόρυβος, το αφήνουμε έξω)
        pass

# Συνάρτηση που διαβάζει το εύρος και εκκινεί τα νήματα
def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <CIDR_Range>")
        print(f"Example: python3 {sys.argv[0]} 192.168.1.0/24")
        sys.exit(1)

    cidr_range = sys.argv[1]
    threads = []

    print(f"{Fore.CYAN}--- Starting Ping Sweep on {cidr_range} ---")

    try:
        # Δημιουργούμε το δίκτυο από το CIDR range (π.χ. 192.168.1.0/24)
        network = ipaddress.ip_network(cidr_range)
    except ValueError:
        print(f"{Fore.RED}🚨 Error: Invalid CIDR range provided.")
        sys.exit(1)

    # Περνάμε από όλες τις IP στο δίκτυο (αγνοούμε την IP του δικτύου και του broadcast)
    for ip in network.hosts():
        # Δημιουργούμε ένα νέο νήμα για κάθε IP
        thread = threading.Thread(target=ping_host, args=(ip,))
        threads.append(thread)
        thread.start()

    # Περιμένουμε να τελειώσουν όλα τα νήματα πριν τερματίσει το main
    for thread in threads:
        thread.join()

    print(f"\n{Fore.CYAN}--- Scan Finished ---")
    print(f"{Fore.GREEN}Total Active Hosts Found: {len(live_hosts)}")
    print(f"Active Hosts: {live_hosts}")

    with open("live_hosts.txt", "w") as f:
       for host in live_hosts:
           f.write(host + "\n")
    
    print(f"{Fore.YELLOW}Saved live hosts to live_hosts.txt")

if __name__ == "__main__":
    main()
