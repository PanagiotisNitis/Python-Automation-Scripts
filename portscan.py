import socket
import argparse
import sys
import requests

# --- 1. Δημιουργία Argparse Parser ---
def create_parser():
    parser = argparse.ArgumentParser(
        description="A simple Python port scanner tool for network reconnaissance. (TCP Handshake check)",
        epilog="Example: python3 portscan.py -t scanme.nmap.org -p 80,443,22"
    )
    parser.add_argument('-t', '--target', required=True, help='Target IP address or domain name.')
    parser.add_argument('-p', '--ports', required=True, help='Ports to scan (e.g., 80,443 or 21-100).')
    return parser

# --- 2. Λογική Σάρωσης ---
# --- 2. Λογική Σάρωσης ---
def scan_port(target, port):
    banner_info = "" # Αρχικοποίηση μεταβλητής για το banner

    try:
        # Δημιουργία Socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1) # Timeout 1 δευτερόλεπτο

        # Προσπάθεια σύνδεσης (3-Way Handshake)
        result = client.connect_ex((target, port))

        if result == 0:
            # ➡️ ΝΕΟ ΒΗΜΑ: Προσπάθεια Banner Grabbing
            if port == 80 or port == 443:
                # Στέλνει ένα αίτημα HTTP για να πάρει την απάντηση του Web Server
                client.send(b"HEAD / HTTP/1.0\r\n\r\n") 
                
            elif port == 21 or port == 22 or port == 23:
                # Για άλλες υπηρεσίες, απλά προσπαθεί να λάβει την απάντηση καλωσορίσματος
                pass # Απλά συνεχίζουμε για να λάβουμε το banner

            try:
                # Λαμβάνει τα πρώτα 1024 bytes (το banner)
                banner = client.recv(1024).decode('utf-8', errors='ignore')
                banner_info = " | Banner: " + banner.split('\n')[0].strip()
            except:
                banner_info = " | Banner: (Could not retrieve)"
            
            return f"✅ Port {port} is OPEN {banner_info}"
        else:
            return f"❌ Port {port} is CLOSED"

    except socket.gaierror:
        return f"🚨 Error: Hostname could not be resolved."
    except Exception as e:
        return f"🚨 Error scanning port {port}: {e}"
    finally:
        client.close() # Βεβαιωνόμαστε ότι κλείνει η σύνδεση

# --- 3. Κύρια Συνάρτηση (Main) ---
def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # Μετατροπή των ports από string σε λίστα αριθμών
    ports_raw = args.ports.split(',')
    ports_to_scan = []
    
    for p in ports_raw:
        if '-' in p:
            start, end = map(int, p.split('-'))
            ports_to_scan.extend(range(start, end + 1))
        else:
            ports_to_scan.append(int(p))
            
    print(f"\n--- Scanning Target: {args.target} ({len(ports_to_scan)} ports) ---\n")
    
    for port in ports_to_scan:
        status = scan_port(args.target, port)
        print(status)
    
    print("\n--- Scan Finished ---\n")

    check_reputation(args.target)

# --- 4. Λογική Threat Intelligence ---
def check_reputation(ip_address):
    # ⚠️ ΠΡΟΣΟΧΗ: Αντικατάστησε το 'YOUR_ABUSEIPDB_KEY' με το δικό σου κλειδί API!
    API_KEY = '31d783e0ccd51f31808739345beddbd1b91959b62bae32a4605a0c9f512fa8bbd257076f0f8c520b'

    # Εάν είναι localhost ή nmap.org, παραλείπουμε τον έλεγχο
    if ip_address == '127.0.0.1' or ip_address == 'scanme.nmap.org':
        print(f"ℹ️ Skipping Threat Intelligence check for {ip_address}.")
        return

    print(f"\n--- Checking Threat Reputation for {ip_address} ---")

    # API Endpoint και Headers (για έλεγχο IP)
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY 
    }

    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90',
        'verbose': 'true'
    }

    try:
        response = requests.get(url=url, headers=headers, params=params)

        # Εάν το αίτημα ήταν επιτυχές
        if response.status_code == 200:
            data = response.json().get('data', {})
            confidence = data.get('abuseConfidenceScore', 0)
            reports = data.get('totalReports', 0)

            print(f"🔥 Abuse Confidence Score: {confidence}% (Based on {reports} reports)")

            # Προσδιορισμός κινδύνου
            if confidence > 50:
                print(f"🚨 ALERT: High risk IP! Check reports manually.")
            elif confidence > 0:
                print(f"⚠️ Warning: Low risk IP with some reports.")
            else:
                print(f"✅ Reputation: IP is Clean or unlisted.")
        else:
            print(f"🚨 Error: AbuseIPDB returned status code {response.status_code}.")

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network Error during Threat Intelligence check: {e}")

# --- 5. Εκκίνηση ---
if __name__ == "__main__":
    main()
