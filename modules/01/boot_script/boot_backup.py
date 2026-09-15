import os
import subprocess
from pathlib import Path
import shutil
from datetime import datetime

def main():
    # Go to repository directory
    repo_root = "/home/stu3340/Documents/repos/CS3340-2026-daniellandry/"
    os.chdir(repo_root)
    subprocess.run(['git', 'switch', 'main'], check=True)

    # Check for synced state with remote (to avoid merge conflicts)
    subprocess.run(['git', 'fetch', 'origin'], check=True)
    commits = subprocess.run(['git', 'log', 'HEAD...origin/main', '--oneline'], capture_output=True, text=True, check=True).stdout.strip()
    push_to_remote = len(commits) = 0

    # Find ip address and write it to ip.md
    ip_address = subprocess.run(['hostname', '-I'], capture_output=True,text=True,check=True).stdout.strip()

    print(f"IP Address: {ip_address}")

    ip_path = Path("/home/stu3340/Documents/repos/CS3340-2026-daniellandry/raspberrypi/etc/ip.md")

    with open(ip_path, "w", encoding="utf-8") as file:
        file.write("## Daniel's Raspberry Pi\n")
        file.write(f"Current IP address: `{ip_address}`")

    # Copy important files specified in backup_list.txt to identical locations in rasberrypi
    backup_list_path = Path("/home/stu3340/Documents/repos/CS3340-2026-daniellandry/modules/01/boot_script/backup_list.txt")
    backup_root = "/home/stu3340/Documents/repos/CS3340-2026-daniellandry/raspberrypi"

    with open(backup_list_path, "r") as file:
        for line in file:
            source_path = line.stip()
            backup_path = backup_root + source_path

            # Make parent directories as needed
            Path(backup_path).parent.mkdir(parents=True, exist_ok=True)

            # Copy the file
            shutil.copy(source_path, backup_path)

    # Push to github
    if push_to_remote:
        curr_time = datetime.now()

        subprocess.run(['git', 'add', 'repo_root'], check=True)
        subprocess.run(['git', 'commit', '-m', f'"Rasberry Pi power on backup: {curr_time}"'], check=True)
        subprocess.run(['git', 'push'], check=True)

if __name__ == "__main__":
    main()





    





