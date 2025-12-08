# Python Port Scanner: Automation for Reconnaissance

## Project Goal
This script was developed to automate the basic **host discovery** phase of security reconnaissance. It acts as a rudimentary **port scanning tool** to quickly identify **open ports** on a target host.

## Technologies & Security Concepts
* **Language:** Python 3
* **Library:** `socket` (Used to initiate the **TCP 3-Way Handshake** and determine port status, central to network security analysis).
* **Methodology:** **Connect-Scan** (attempts a full connection).
* **Control:** Uses `settimeout(1)` to prevent the script from waiting indefinitely, which is a good **security practice** to prevent self-imposed **Denial of Service (DoS)** issues.
* **SOC Relevance:** Understanding how these packets look on the network is crucial for writing **SIEM detection rules** (Splunk/ELK).
* **SOAR/Threat Intelligence:** Threat Intelligence: Implemented an automated IP reputation check feature by integrating the AbuseIPDB API, allowing for immediate risk assessment of scanned targets.

## Usage
```bash
python3 portscan.py 
# The script will prompt the user to input the target IP or Domain.

### 🛡️ File Integrity Monitor (FIM)
A Blue Team automation script that monitors critical files for unauthorized changes.
* **Methodology:** Calculates baseline SHA-256 hashes of target files.
* **Detection:** Runs a continuous loop to compare current file hashes against the baseline.
* **Alerting:** Triggers an immediate security alert in the console if a file is modified or deleted.
* **CIA Triad:** Addresses the **Integrity** aspect of information security.
