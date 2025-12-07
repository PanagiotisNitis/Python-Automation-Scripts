import socket
import argparse
import sys

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


if __name__ == "__main__":
    main()
