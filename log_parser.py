import re
import json
import sys
from colorama import Fore, Style, init

init(autoreset=True)

# Pattern για να ταιριάξουμε τα βασικά πεδία του FIM Log
# (Timestamp, Log Level, Filename, User, Action)
FIM_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}): (ALERT|INFO|WARNING): The hash for file '(.+?)' was changed by user '(.+?)'. Action: (.+?)\."

def parse_log_entry(log_entry):
    """Αναλύει μία γραμμή log χρησιμοποιώντας Regular Expressions."""
    match = re.match(FIM_PATTERN, log_entry)
    
    if match:
        timestamp, log_level, filename, user, action = match.groups()
        
        # Δημιουργία του δομημένου JSON αντικειμένου
        structured_log = {
            "timestamp": timestamp,
            "log_level": log_level,
            "event_type": "FIM_CHANGE",
            "filename": filename,
            "user": user,
            "action": action
        }
        return structured_log
    else:
        # Επιστροφή σφάλματος για logs που δεν ταιριάζουν στο pattern
        return {"error": "Unparsable Log Format", "raw_entry": log_entry.strip()}

def main():
    if len(sys.argv) != 3:
        print(f"{Fore.YELLOW}⚠️ Usage: python3 {sys.argv[0]} <input_log_file> <output_json_file>")
        print(f"{Fore.YELLOW}Example: python3 {sys.argv[0]} raw_fim_logs.txt structured_output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    parsed_logs = []
    
    try:
        with open(input_file, 'r') as infile:
            for line_number, line in enumerate(infile, 1):
                # Αγνοούμε τις κενές γραμμές
                if not line.strip():
                    continue

                parsed_entry = parse_log_entry(line)
                parsed_logs.append(parsed_entry)
                
                if "error" in parsed_entry:
                    print(f"{Fore.RED}🚨 Error parsing line {line_number}: {parsed_entry['error']}")
                else:
                    print(f"{Fore.GREEN}✅ Line {line_number} Parsed: {parsed_entry['filename']} -> {parsed_entry['action']}")
    
    except FileNotFoundError:
        print(f"{Fore.RED}🚨 Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Εγγραφή όλων των δομημένων logs στο αρχείο εξόδου JSON
    try:
        with open(output_file, 'w') as outfile:
            json.dump(parsed_logs, outfile, indent=4)
        print(f"\n{Fore.CYAN}--- Parsing Finished ---")
        print(f"{Fore.GREEN}Successfully saved {len(parsed_logs)} entries to '{output_file}'")
    except Exception as e:
        print(f"{Fore.RED}🚨 Error writing output file: {e}")

if __name__ == "__main__":
    main()
