# Day 28 – Revision Day: Everything from Day 1 to Day 27
## Task 1: Self-Assessment Checklist
# Can do confidently
## Linux
✅ Navigate the file system, create/move/delete files and directories

✅ Manage processes — list, kill, background/foreground

✅ Work with systemd — start, stop, enable, check status of services

✅Read and edit text files using vi/vim or nano

✅ Troubleshoot CPU, memory, and disk issues using top, free, df, du

✅ Explain the Linux file system hierarchy (/, /etc, /var, /home, /tmp, etc.)

✅ Create users and groups, manage passwords

✅ Set file permissions using chmod (numeric and symbolic)

✅ Change file ownership with chown and chgrp

✅  Check network connectivity — ping, curl, netstat, ss, dig, nslookup

## shell scripting

✅ Write a script with variables, arguments, and user input

✅Use if/elif/else and case statements

✅ Write for, while, and until loops

✅ Define and call functions with arguments and return values

✅  Handle errors with set -e, set -u, set -o pipefail, trap

## Git & GitHub


✅  Initialize a repo, stage, commit, and view history

✅  Create and switch branches

✅  Push to and pull from GitHub

✅  Explain clone vs fork

✅  Merge branches — understand fast-forward vs merge commit

✅  Rebase a branch and explain when to use it vs merge

✅  Use git stash and git stash pop

✅  Cherry-pick a commit from another branch

✅  Explain squash merge vs regular merge

✅  Use git reset (soft, mixed, hard) and git revert
 
✅ Explain GitFlow, GitHub Flow, and Trunk-Based Development

# Need to revisit
🟥 Create and manage LVM volumes

🟥 Schedule scripts with crontab

🟥Use grep, awk, sed, sort, uniq for text processing


# Task 2: Revisit Your Weak Spots

❗ Create and manage LVM volumes

 ### day-13-lvm.md
 
+ created physical vloume
    + ``` pvcreate /dev/nvme1n1 /dev/nvme2n1 /dev/nvme3n1 ```
+ created volume group
    + ``` vgcreate revision-vg /dev/nvme1n1 /dev/nvme2n1 ```
+ created logical group
    + ``` lvcreate -L 10G -n revision-lv revision-vg ```
+ created directory
    + ``` mkdir /mnt/revision-lv-mount ```
+ formated it
   + ```  mkfs.ext4 /dev/revision-vg/revision-lv```
+ mounted it
   + ``` mount /dev/revision-vg/revision-lv /mnt/revision-lv-mount```
+ exteneded it
   + ```  lvextend -L +4G /dev/revision-vg/revision-lv```
+ to see the changes when we do df -h
   + ``` resize2fs /dev/revision-vg/revision-lv ```
  # screenshots

<img width="1920" height="163" alt="Screenshot (167)" src="https://github.com/user-attachments/assets/0853767a-a5a2-4c1c-a97a-ee7606172e59" />
<img width="1920" height="312" alt="Screenshot (168)" src="https://github.com/user-attachments/assets/e9924505-77a3-4033-b8ac-67e029683df3" />
<img width="1920" height="459" alt="Screenshot (169)" src="https://github.com/user-attachments/assets/d280a2d5-0319-45c7-8650-cc82d143d29c" />
<img width="1920" height="155" alt="Screenshot (170)" src="https://github.com/user-attachments/assets/ee3958bb-6d67-449a-a198-675d448ceb78" />
<img width="1920" height="157" alt="Screenshot (171)" src="https://github.com/user-attachments/assets/9b1076e4-31c3-4e07-8f8f-9f34b9c0751f" />
<img width="1920" height="380" alt="Screenshot (172)" src="https://github.com/user-attachments/assets/add4c34f-be3e-4fde-be9c-d395db6839e9" />


❗ Schedule scripts with crontab


+ practiced shedulling script using crontab
+ like how to create crontaband how to schedule task with the help of cron
     + checked exsisting crontab ``` crontab -l ```
     + create shell script
     + then opened the ```crontab -e```
     + selected nano editor and added ``` */2 * * * * /``` this means every two minutes every hour everyday
     + then execute that .sh file
     + inside that file i see the logs
     + and deletd it 
# screenshots

<img width="1920" height="165" alt="Screenshot (174)" src="https://github.com/user-attachments/assets/b9a66c54-201f-465f-b271-22826ccc1d95" />
<img width="1784" height="754" alt="Screenshot (173)" src="https://github.com/user-attachments/assets/d4fe6c35-912f-4e6d-a1e8-cff5c71c84d6" />

❗ Use grep, awk, sed, sort, uniq for text processing

+ practied grep to find lines such as
  + INFO ``` grep "INFO" logs.txt |sort|uniq -c```
  + ERROR ```grep "ERROR" logs.txt |sort|uniq -c```
  + WARNING```grep "WARNING" logs.txt |sort|uniq -c```
+ practiced awk to search coloume wise log
  
+ ``` awk '$1=="ERROR" log.txt ```
+ sort to arrange data in alphabetical order
+ ```awk '$1=="ERROR" log.txt |sort```
  
+ uniq will remove the dublicates lines in the logs and print a single line only
+ ```awk '$1=="ERROR" log.txt |sort |uniq -c```

# screenshots
<img width="1920" height="1080" alt="Screenshot (176)" src="https://github.com/user-attachments/assets/70108964-cc7d-4ff5-85fe-bc502ebd327b" />



# Task 3: Quick-Fire Questions
## Answer these from memory (no Googling). Then verify your answers:

## What does chmod 755 script.sh do?
+ chmod helps to change mode 7 means read , write, executable for owner , 5 means user and other can reads and write 
## What is the difference between a process and a service?
 + process can be start/stop
 + but services can not be start/stop its running services in background
  
## How do you find which process is using port 8080?
 + netstat -tulp | grep : 8080
   
## What does set -euo pipefail do in a shell script?
 + e - this will stop the script imidieatly after erorr occur
 + u - if any undefined erorr came
 + o pipefail - this will stop when any command inside the pipe fail
   
## What is the difference between git reset --hard and git revert?
+ git reset - hard - will delete the commit and changes too
+ git revert - this will not change the history
+ create a new commit that undoes the changes
  
## What branching strategy would you recommend for a team of 5 developers shipping weekly?
+ i rcommend githubflow.
  
## What does git stash do and when would you use it?
+ git stash will hide changes for temporarly
+ this can be use while you are working on something and dont want to commit it or make changes
  
## How do you schedule a script to run every day at 3 AM?
+ by using cron tab
+ cron -e
+ 0 3 * * *
  
## What is the difference between git fetch and git pull?
+ git fetch - use for downloading changes without merging it
+ git pull - use for fetch and merge
  
## What is LVM and why would you use it instead of regular partitions?
+ LVM (Logical Volume Manager)- lvm resize volumes, combine disks, and take snapshots without downtime

  ## Task 5: Teach It Back
### Pick one topic you've learned and write a short explanation (5-10 lines) as if you're teaching it to someone who has never heard of it. Add it to your day-28-notes.md.

Examples:

Explain Git branching to a non-developer
Explain file permissions to a new Linux user
Explain what a crontab is and why sysadmins use it
Teaching is the best test of understanding.

# explain what is lvm 
+ LVM is a way to manage computer storage smartly.
+ In normal systems, storage is fixed.
+ If one part becomes full, we cannot change it easily.
+ LVM allows us to increase or decrease space anytime without stopping the system.
That’s why it is very useful for servers.
+ we can create the storage usiing these three :
    + physical volume
      + suppose we create three space (volume)
            
    + vloume group
      + now we combined it by group 
            
    + logical volume 

      + by that group we created we will make logical vloume means this will break the space to use 


  
