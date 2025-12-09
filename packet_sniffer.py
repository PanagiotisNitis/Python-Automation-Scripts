import sys
from scapy.all import sniff, IP, TCP, Raw
from colorama import Fore, Style, init
import os 

init(autoreset=True)

# Παγκόσμια λίστα για αποθήκευση των ευρημάτων
vulnerable_packets = []

def packet_callback(packet):
    """Αναλύει κάθε πακέτο που πιάνεται."""
    global vulnerable_packets
    
    # 1. Φιλτράρισμα: Θέλουμε μόνο πακέτα IP με TCP (τα περισσότερα δεδομένα)
    if IP in packet and TCP in packet:
        # 2. Έλεγχος για Raw Data (payload)
        if Raw in packet:
            # Το payload είναι το περιεχόμενο του πακέτου
            payload = packet[Raw].load
            
            # 3. Φιλτράρισμα για HTTP (μη κρυπτογραφημένο) κείμενο
            try:
                # Προσπαθούμε να αποκωδικοποιήσουμε το payload σε κείμενο
                payload_str = payload.decode('utf-8', errors='ignore')
                
                # Έλεγχος για κλασικές HTTP λέξεις-κλειδιά
                if "GET /" in payload_str or "POST /" in payload_str or "User-Agent" in payload_str:
                    
                    # 4. Ειδικός έλεγχος για ευαίσθητα δεδομένα (π.χ., unencrypted login)
                    if "password" in payload_str.lower() or "passwd" in payload_str.lower():
                        
                        # Βρέθηκε ευαίσθητο δεδομένο σε μη κρυπτογραφημένο πακέτο!
                        print(f"{Fore.RED}🚨 [ALERT] Potential Credentials Found in Unencrypted Traffic!")
                        print(f"{Fore.RED}   Source: {packet[IP].src}:{packet[TCP].sport} -> Destination: {packet[IP].dst}:{packet[TCP].dport}")
                        print(f"{Fore.YELLOW}   Payload Snippet: {payload_str[:80]}...")
                        vulnerable_packets.append(payload_str)
                        return
                    
                    # print(f"{Fore.GREEN}✅ HTTP Packet Captured: {packet[IP].src} -> {packet[IP].dst}")
            except:
                # Αγνοούμε πακέτα που δεν είναι κείμενο (π.χ., εικόνες, δυαδικά)
                pass

def main():
    print(f"{Fore.CYAN}--- Starting Simple Packet Sniffer ---")
    print(f"{Fore.CYAN}Listening for HTTP traffic on interface eth0 (default)...")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop the sniffing.")

    try:
        # snif: Η συνάρτηση που "πιάνει" τα πακέτα
        # filter: Το φίλτρο δικτύου (μόνο κίνηση στη θύρα 80, HTTP)
        # prn: Η συνάρτηση που καλείται για κάθε πακέτο
        #sniff(filter="tcp port 80", prn=packet_callback, store=0, timeout=20) 
        
        # Νέα γραμμή (για local testing):
        sniff(iface="lo", filter="tcp port 80", prn=packet_callback, store=0, timeout=20)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}--- Sniffing Stopped by User ---")
    except Exception as e:
        print(f"{Fore.RED}🚨 Error during sniffing (Did you run with sudo?): {e}")

    print(f"{Fore.GREEN}Total sensitive packets captured: {len(vulnerable_packets)}")

if __name__ == "__main__":
    # Το Packet Sniffing απαιτεί συνήθως δικαιώματα root
    if sys.platform != "win32" and os.geteuid() != 0:
        print(f"{Fore.RED}🚨 This script must be run with sudo/root privileges.")
        sys.exit(1)
    
    import os # Χρειάζεται εδώ για να δουλέψει το os.geteuid()
    main()
