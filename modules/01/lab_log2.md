# Creative Embedded Systems

## Lab 1 - Dev & Prod

Performed by: Ryan Fernandes and Daniel Landry

### Action Plan

    1. Update boot script to backup RPi IP even when behind on commits
    2. Change location of ip.md file to CS3340/raspi-ip/
    3. Research further important config files in RPi system that should be backed up
    4. 

### Execution

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
 



