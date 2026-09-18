import os
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    source_path = "/home/stu3340/Documents/ip-tracking/ip.txt"
    dest_path = "ryan@10.74.22.174:/Users/daniellandry/Documents/ip.txt"
    private_key = "/home/stu3340/.ssh/id_ed25519"

    curr_time = datetime.now()

    #copy current ip address to ip.txt
    ip_address = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True).stdout.strip()

    with open(source_path, "w", encoding="utf-8") as file:
        file.write("Daniel's Raspberry Pi\n")
        file.write(f"Current IP address: {ip_address}\n")
        file.write(f"Last updated: {curr_time}")

    #copy file to remote computer using scp
    subprocess.run(['scp', '-i', private_key, source_path, dest_path], check=True)

if __name__ == "__main__":
    main()