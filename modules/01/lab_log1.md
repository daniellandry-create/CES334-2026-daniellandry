# Creative Embedded Systems

## Lab 1 - Dev & Prod

Performed by: Ryan Fernandes and Daniel Landry

### Action Plan

1. Research Raspberry Pi file structure for configs
2. Create raspberrypi directory in repo that mimics the researched file structure
3. Create the ip.md doc where appropriate
4. Commit/push changes
5. Plug in the Pi (starting with HDMI and peripherals, then power last)
6. Find Pi MAC address
7. Register the Pi as a device on the yalewireless network
8. Find Pi IP address
9. SSH into the Pi using provided username and password
10. Generate a new SSH key for the Pi on GitHub (no password)
11. Research how to run a script on the Pi after networking has been achieved
12. Research which files are important to backup on the Pi
13. Choose a language for our script and research how to copy files and record current IP address
14. Write the script and test that it runs once per login after networking has been achieved

-- *Optional* --

15. Clone the 3340 repo onto the Pi
16. Add to the script to move files to 3340 repo and push to GitHub

### Execution

1. Research Raspberry Pi file structure for configs

- /boot/config.txt is an important config file (provided in the lab guide)
- Raspberry Pi directory structure mimics that of Linux
  - /bin = Essential User Command Binaries
  - /boot = Static Files of the boot loader
  - /dev = Device Files
  - /etc = Host specific system configuration
  - /home = User home directories
  - /lib = Shared libraries
  - /media = Removable Media
  - /mnt = Temporarily Mounting Filesystems
  - /opt = Add-on Application software package
  - /sbin = System Binaries
  - /srv = Data for service from system
  - /tmp = Temporary Files
  - /usr = User Utilities and Applications
  - /proc = Process Information
- Possibly /boot/config.txt is actually /boot/firmware/config.txt
- config.txt can include other config files, so we should check the contents, and make sure that these files are also backed up
- autoboot.txt may also be a config worth backing up (specified boot_partition number)
- cmdline.txt could also be imporant
- "Boot" means to turn on the device and load operating system into memory, so it is ready for use
- Possibly backup entire /boot directory
- /etc seems to be a good place to store ip.md since this is where ssh keys, etc go

2. Create raspberrypi directory in repo that mimics the researched file structure

- Made local directory in "Documents" for Creative Embedded Systems
- Cloned repo locally
- Opened repo in VSCode
- Opened command-line in VSCode
- Used command-line unix to create the standard Linux filestructure (top-level), as well as "firmware/" within /boot
- Also created modules top-level directory

3. Create the ip.md doc where appropriate

- Used "touch ip.md" to create ip.md in /etc

4. Commit/push changes

- Ran git status
- Ran git add .
- Committed with git commit -m "..."
- Pushed to main with git push
- Verified that all the changes got pushed to GitHub
- **Noted** that directories without files were not pushed to GitHub
  - May troubleshoot later, but not urgent

5. Plug in the Pi (starting with HDMI and peripherals, then power last)

- Plugged in keyboard (which had mouse connected to it already) via USB (black ports)
- Plugged in mini HDMI, but it was a loose fit, so took off top case to be safe and plugged in mini HDMI fully
- Plugged in power via USB-C
- Fan lights on Pi went red, then green, then fan started moving and lights changed colors
- Light near power button was blinking green
- Turned the monitor on
- Unplugged HDMI mini and replugged into HDMI 1
- Screen turned on revealing Pi OS

6. Find Pi MAC address
7. Register the Pi as a device on the yalewireless network

- Tested clicking WiFi in Pi OS and connecting to yalewireless network w/o configuring MAC address
- Connection worked and able to open Chrome pages
- However, cannot establish private connection because computer's date and time is incorrect (fix later possibly)

8. Find Pi IP address

- Opened Pi command line
- Used hostname -I to list IP address

9. SSH into the Pi using provided username and password

- Opened VSCode terminal
- Used command ssh (ip address)
- Asked to establish the authenticity of host
- Responded "yes" to continue connecting

- ISSUE: hit raspberry pi by accident and the monitor went blank
  - Played around with HDMI cord for a secong (plug/unplug), and moved it to HDMI 1, and problem solved (scrren back on)

- Typed "yes" and got "Conection closed by (ip) port 22"
- Tried again and got "password" prompt
- Typed in password, got permisison denied
- Reason likely because we did not indicate username with -l
- Did ^C to exit out of prompt
- Did ssh (ip) -l (username)
- Typed in password again and was able to login
- Got command line "stu3340@334ces-g"
- Did ls and got "Desktop, Documents, Downloads, etc"
- Did ls -a and saw ".config", but it's a directory
- cd .. took us to "home"
- cd .. took us to /, which had boot directory, as desired
- cd boot, ls showed config.txt, cmdline.txt, other images
- cd firmware showed another cmdline.txt, config.txt
- Uncertain which should be backed up and which shouldn't (tbd)

10. Generate a new SSH key for the Pi on GitHub (no password)

- Navigated to GitHub on computer
- Clicked on user icon and went to settings
- Went to SSH and GPG keys
- Clicked new SSH Key
- Gave the key a title (raspberypi ssh)
- Went to raspberry pi terminal and created ssh key using ssh-keygen -t ed25519
- Kept standard location (/home/stu3340/.ssh/id_ed25519)
- Hit enter for password, so no password
- To find the ssh key, ran cat /home/stu3340/.ssh/id_ed25519.pub
- Copied the full output
- Pasted that into the "Key field"
- Clicked "Add SSH Key"
- SSH key was added successfully

11. Research how to run a script on the Pi after networking has been achieved

- We can create a systemd file in /etc/systemd/system/(service_name.service)
- We can name it using [Unit] Descript =, and have it run after network established using After
- In [Service], we can define the command to run in ExecStart
- [Install] has WantedBy, and it is a bit unclear what is needed in there
- After = network.target seems to be boilerplate
- To run a python service, you can do [Service] ExecStart=/usr/bin/python myscript/python

12. Research which files are important to backup on the Pi

- For now, just backup the /boot directory to the same directory on our Git repo

13. Choose a language for our script and research how to copy files and record current IP address

- Going to write a .sh script

14. Write the script and test that it runs once per login after networking has been achieved

- cd ~ took us to /home/stu3340
- cd Documents
- ls showed nothing in Documents
- mkdir repos for clones repositories
- git clone (CPSC repo link)
- Clone was successful
- Testing git permissions
  - cd into CES repo
  - git status showed up-to-date branch
  - touch test.txt to create a test file
  - git status showed the new .txt file
  - git add . added it
  - git commit -m "test ssh"
  - Got a warning about setting email and name for git
  - Set these values with `git config --global user.email "email"` and `git config --global user.name "name"`
  - git push worked without password required
  - Confirmed file showed on git repo
  - Removed file locally and pushed again
- Wrote python script to write IP address and copy files specified with paths in a .txt
- Tried copying /boot/config.txt and got a file that said the config file had moved to /boot/firmware/config.txt (made this change)
- For now, backup_list file only has /boot/firmware/config.txt
- Added code to upload to github with subprocess.run
- Wrote systemd file to run the script on network connection (After=network-online.target)
- Tried copying it to systemd location, but got PermissionDenied. Used sudo and it worked without a password
- Added boot backup systemd script to the backup file list
- Realized that service was not configured to run (enabled), so ran `sudo systemctl enable boot_backup` to enable it
- Got error with Git "detected dubious ownership"
- Need to add User=stu3340 to [Service] in the service, so that it runs as the owner of the git repo
- Then, got issues with fetch, since the git remote with the https path. Needed it to be ssh
    - Used git remote set-url origin git@github.com:{username}/CS3340-2026.git
