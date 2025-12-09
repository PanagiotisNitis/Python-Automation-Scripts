# 🛡️ Python Security Automation & Tool Kit

### **Στόχος του Project**
Αυτό το Portfolio αποτελείται από **8 εργαλεία κυβερνοασφάλειας** γραμμένα σε **Python**. Ο κύριος στόχος ήταν να μετατρέψω τη θεωρία σε πράξη, δημιουργώντας scripts που λύνουν πραγματικά προβλήματα σε ρόλους όπως **SOC Analyst (Tier 1)** και **Junior Pen Tester**.

* **Φιλοσοφία:** Επικεντρώνομαι σε εργαλεία που καλύπτουν όλες τις φάσεις: **Reconnaissance**, **Triage**, **Incident Response**, και **Forensics**.

---

## 🛠️ Τα 8 Εργαλεία και η Δουλειά τους

| Project | Κατηγορία | Τι Κάνει; (Πρακτική Εφαρμογή) | Κρίσιμες Δεξιότητες |
| :---: | :--- | :--- | :--- |
| **1. FIM Tool** | **Defensive/Integrity** | Παρακολουθεί κρίσιμα αρχεία (π.χ., ρυθμίσεις συστήματος) για **μη εξουσιοδοτημένες αλλαγές** (Alerting). | **SHA-256 Hashing**, File Integrity Monitoring. |
| **2. Log Parser** | **Log Analysis/SOC** | Μετατρέπει ακατέργαστα logs σε **δομημένο JSON** για εύκολη φόρτωση σε **SIEM** (Splunk/ELK). | **Regular Expressions (Regex)**, Data Normalization. |
| **3. Packet Sniffer** | **Forensics** | Συλλαμβάνει πακέτα δικτύου για να εντοπίσει **μη κρυπτογραφημένα credentials** ή payloads σε HTTP κίνηση. | **Scapy**, Network Protocol Analysis (Raw Data). |
| **4. Port Scanner** | **Network Recon** | Εντοπίζει γρήγορα **ανοιχτές θύρες** και υπηρεσίες σε έναν στόχο για χαρτογράφηση. | **Python Sockets**, TCP Handshake. |
| **5. Web Fuzzer** | **Web Testing** | Ανακαλύπτει **κρυφά αρχεία** και φακέλους σε Web Servers για επέκταση της επιφάνειας επίθεσης. | **HTTP Requests**, Threading, Status Codes. |
| **6. Threat Intel** | **Threat Intelligence** | Ελέγχει ύποπτες IPs μέσω **API** για άμεση επικύρωση alerts. | **API Calls**, Risk Scoring. |
| **7. FTP Brute Force** | **Offensive** | Δοκιμάζει την αντοχή των κωδικών σε υπηρεσίες FTP (Testing weak credentials). | **Networking Protocols**, Error Handling. |
| **8. Ping Sweep** | **Network Recon** | Βρίσκει γρήγορα **ποιοι hosts** είναι ζωντανοί σε ένα μεγάλο εύρος δικτύου. | **ICMP Protocol**, Threading. |

---

## 💡 Βασικά Takeaways (Για τον Recruiter)

* **Δεξιότητες:** Έχω πρακτική εμπειρία στη χρήση **Python** για **Network Analysis**, **Data Processing (Logs)**, και **Automated Testing**.
* **Πλαίσιο:** Ξέρω πώς αυτά τα εργαλεία ενσωματώνονται στον κύκλο ζωής ενός περιστατικού (π.χ., **FIM alert** -> **Log Analysis** -> **Packet Sniffer Forensics**).
* **Τεχνολογίες:** Χρησιμοποιήθηκαν εξειδικευμένες βιβλιοθήκες όπως **Scapy, hashlib, requests, threading**, πέρα από βασικές γνώσεις Python.