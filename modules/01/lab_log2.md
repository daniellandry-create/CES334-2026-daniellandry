# Creative Embedded Systems

## Lab 1 - Dev & Prod

Performed by: Ryan Fernandes and Daniel Landry

### Action Plan

    1. Update boot script to backup RPi IP even when behind on commits
    2. Change location of ip.md file to CS3340/raspi-ip/
    3. Research further important config files in RPi system that should be backed up
    4. Revise boot script to backup additional important files/directories
    5. Complete SCP portion of assignment

### Execution

Part 1, GitHub Upload Script:
    1. Updated script generaly performs the following routine:
        1. Fetch main branch, stash local changes and create new branch ("ip-branch") that points to origin/main
        2. On new branch, create ip.md file in appropriate directory and push changes to remote branch
        3. Switch back to original branch, pop stashed local changes, and delete temporarily created local branch
    2. Script testing:
        - Manually ran program, successful run on second attempt (curr_time error)
        - Real test on RPi boot-up successfully pushed ip.md to origin/main on first attempt
    3. Updated script to backup the following additional files
        - /boot/firmware/config.txt
        - /etc/
        - cmdline.txt
    4. Ran into git commit error trying to backup additional files and directories
    5. Error determined to be with path concatenation - solved by treating paths as strings until final string created and turned into path object
    6. Ran into errors with file permission when copying etc/ directory for backup purposes
    7. Attempted to solve by running program with root user sudo privileges then switching to stu3340 user when running git commands in script
    8. Researched which github commands required user authentication 
    9. Ran program with root user permissions, program crashed because certain files copied to repo by root user were still owned by root user, so git couldn't index files because student user didn't have permissions 
    10. Fixed by running recursive chown command (with root user priviliges) on directories to be backed up to make student user new owner

Part 2, SCP File Upload:
    1. Created a new directory "~/Documents/ip-tracking"
    2. Created an empty "ip.txt" file in that location (so that it was outside of the git repo)
    3. Created an empty "ip.txt" file in a chosen location on our computer
    4. Found the IP address of our computer by holding option and then clicking on the WiFi logo
    5. Wrote the scp command: "scp -i {private key path} {location of ip-tracking/ip.txt} {username@computer_ip:ip.txt_loc}
    6. Copied code similar to our update ip.md code from part 1 in order to update ip.txt file with the current IP address before doing SCP
    7. Did crontab -e and entered the following: "*/10 * * * * /usr/bin/python3 /home/stu3340/Documents/CS3340-2026/modules/01/scp-script/send_ip.py
 
Part 3 (Copying work to Daniel's Pi):
    1. When I ssh'ed into my pi I got a warning about my .ssh file being "unprotected." Issue was likely that .ssh keys were accessible by any user on laptop. Used chmod 700 ~/.ssh to fix
    2. Useful git commands:
        - git branch --show-current
        - git branch -d branch_name
        - git switch -
        - git fetch origin -> git reset --hard origin/main
        



