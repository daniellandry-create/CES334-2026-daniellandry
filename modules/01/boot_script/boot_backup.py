import os
import subprocess
from pathlib import Path
import shutil
from datetime import datetime

def main():
    repo_name = "CS3340-2026"

    # Go to repository directory
    repo_root = f"/home/stu3340/Documents/repos/{repo_name}/"
    os.chdir(repo_root)

    # Stash the current changes and switch to a branch that is a copy of main on the remote
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'fetch', 'origin'], check=True)
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'stash', '-u'], check=True)

    ip_branch_name = "ip-branch"

    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'switch', '-c', ip_branch_name, 'origin/main'], check=True)

    # Find IP address and write it to ip.md
    ip_address = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True).stdout.strip()

    print(f"IP Address: {ip_address}")

    ip_root = Path(f"/home/stu3340/Documents/repos/{repo_name}/raspi-ip")
    ip_path = Path(f"/home/stu3340/Documents/repos/{repo_name}/raspi-ip/ip.md")
    ip_path.parent.mkdir(parents=True, exist_ok=True)
    
    curr_time = datetime.now()

    with open(ip_path, "w", encoding="utf-8") as file:
        file.write("## Ryan's Raspberry Pi\n");
        file.write(f"Current IP address: `{ip_address}`\n")
        file.write(f"Last updated: {curr_time}")

    subprocess.run(['chown', '-R', 'stu3340:stu3340', ip_path], check=True)

    # Copy important files specified in backup_list.txt to identical locations in raspberrypi
    backup_list_path = Path(f"/home/stu3340/Documents/repos/{repo_name}/modules/01/boot-script/backup_list.txt")
    backup_root = f"/home/stu3340/Documents/repos/{repo_name}/raspberrypi"

    with open(backup_list_path, "r") as file:
        for line in file:
            source_str = line.strip()
            source_path = Path(source_str)
            backup_path = Path(backup_root + source_str)

            print(source_path, backup_path)

            # Make parent directories as needed
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the file
            if source_path.is_dir():
                shutil.copytree(source_path, backup_path, dirs_exist_ok = True)
            else:
                shutil.copy(source_path, backup_path)
    
    subprocess.run(['chown', '-R', 'stu3340:stu3340', backup_root], check=True)
    
    # Push to GitHub
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'add', repo_root], check=True)

    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'commit', '-m', f'"Raspberry Pi power on backup: {curr_time}"'], check=True)
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'push', 'origin', 'HEAD:main'])

    # Switch back to original branch and clean up IP branch
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'switch', '-'])
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'stash', 'pop'])
    subprocess.run(['sudo', '-u', 'stu3340', 'git', 'branch', '-d', ip_branch_name])

if __name__ == "__main__":
    main()



    





