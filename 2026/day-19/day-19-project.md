## Day 19 – Shell Scripting Project: Log Rotation, Backup & Crontab
## why we use rotation
+ we use log rotation to prevent log files from growing to large ,so rotation ensures that the old logs are compressed or deleted
## why we backup
+ we sue backup to protect our data if something goes wroung like a system failiure bacups allows us to restore important files..
## Task 1: Log Rotation Script
Create log_rotate.sh that:
Takes a log directory as an argument (e.g., /var/log/myapp)


Compresses .log files older than 7 days using gzip
Deletes .gz files older than 30 days


Prints how many files were compressed and deleted
Exits with an error if the directory doesn't exist

```
firstly create log files inside the /var/log/myapp
- sudo touch text1.log ,text2.log, text3.log
1)create file log_routate.sh
2)then takes argument
3)write command in this (gzip)
code :-

create_rotation(){

        echo "usage: <./log_rotation.sh source > < /var/log/myapp folder>"
}
if [ $# -eq 0 ]; then
        create_rotation
fi

LOG_DIR=$1
        if [ ! -d "$LOG_DIR" ]; then
    echo "directory is not found"
    exit 1
else
    echo "log directory found"
fi
echo "Starting log rotation in $LOG_DIR..."
COMPRESSED=$(find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec gzip {} +  -print | wc -l)
DELETED=$(find "$LOG_DIR" -type f -name "*.gz" -mtime +30 -print -delete | wc -l)
echo "Compressed files: $COMPRESSED"
echo "Deleted files: $DELETED"

echo "Log rotation completed."
```
## OUTPUT

<img width="1920" height="450" alt="Screenshot (114)" src="https://github.com/user-attachments/assets/cb1aab70-1344-4c3f-809a-91adf7c50988" />

## Task 2: Server Backup Script!

Create backup.sh that:
Takes a source directory and backup destination as arguments

Creates a timestamped .tar.gz archive (e.g., backup-2026-02-08.tar.gz)
Verifies the archive was created successfully


Prints archive name and size
Deletes backups older than 14 days from the destination
Handles errors — exit if source doesn't exist
```
1)create file
2)then taking argument
3)create function
4)add command (tar -czf)
 code:-
source_dir=$1
backup_dir=$2
Timestamp=$(date '+%y-%m-%d-%H-%M-%S')

create_backup(){
        archive_name="backup-$Timestamp.tar.gz"
    archive_path="$backup_dir/$archive_name"

   tar -czf "$archive_path" "$source_dir"

    if [ $? -eq 0 ]; then
        echo "Backup created: $archive_name"
        ls -lh "$archive_path"
    else
        echo "Backup failed"
        exit 1
    fi
}
delete_old(){
        find "$backup_dir" -name "*.tar.gz" -mtime +14 -delete
}
create_backup
delete_old
```
## output
<img width="1920" height="556" alt="Screenshot (106)" src="https://github.com/user-attachments/assets/d984f7c6-91f4-4fbc-8b77-5c6749687a5b" />


## Task 3: Crontab
Read: crontab -l — what's currently scheduled?
Understand cron syntax:
* * * * *  command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)


Write cron entries (in your markdown, don't apply if unsure) for:
Run log_rotate.sh every day at 2 AM
Run backup.sh every Sunday at 3 AM
Run a health check script every 5 minutes

```
1)created a crontab.txt (markdown)
2) inside that file writeing the cron entries with absolute paths
3)for both three files
line:-
0 2 * * *  /home/ubuntu/log_rotate.sh /var/log/myapp >> /home/ubuntu/devops.log 2>&1

0 3 * * 0 /home/ubuntu/lab/scripts/backup.sh /home/ubuntu/lab/source /home/ubuntu/lab/backup >> /home/ubuntu/lab/backup.log 2>&1

*/5 * * * 0 /home/ubuntu/health_check.sh >> /home/ubuntu/health.log 2>&1
```

## output

<img width="1920" height="267" alt="Screenshot (110)" src="https://github.com/user-attachments/assets/37dcead3-f487-4e14-9cfe-97be18da4a59" />

## Task 4: Combine — Scheduled Maintenance Script
Create maintenance.sh that:

Calls your log rotation function
Calls your backup function
Logs all output to /var/log/maintenance.log with timestamps
Write the cron entry to run it daily at 1 AM
```
1)creat the maintenance.sh and log file in the path /var/log/maintenance.log
2)then inside the script
3)create variable and assign it the path where your log file is
4)and mention the excuting argument in that so file will undestand how to run that files
 code :-
log_file="/var/log/maintenance.log"

log_message(){
        echo "[$(date '+%y-%m-%d %H:%M:%S')] $1" >> "log_file"
}
log_message "=======maintenance started==========="
log_message "======running log routation========="
sudo /home/ubuntu/log_rotate.sh /var/log/myapp  >> "$log_file" 2>&1

log_message "==========running backup==============="
/home/ubuntu/backup.sh /home/ubuntu/lab/source /home/ubuntu/lab/backup  >> "$log_file" 2>&1

log_message "===============maintenance completed==========="
```
## output
<img width="1920" height="861" alt="Screenshot (111)" src="https://github.com/user-attachments/assets/cc298bec-f13e-4c11-9a83-2c1f622a1a6f" />


### what i learned 
+ Learned how to create a log rotation script to compress .log files and delete log or .gz files older than 30 days.
+ Learned how to write a backup script to back up folders and automatically delete backup files older than 14 days.
+ Understood how to create .tar.gz archive files for efficient backup storage.
+ Handled and troubleshot errors such as “permission denied” and “file not found.”
+ Learned how cron entries work and how to schedule scripts (log rotation and backup) automatically.
+ Created a main maintenance.sh script to call both the log rotation and backup scripts together.
+ Learned how to redirect output after calling functions and store the logs in a separate log file for proper monitoring.
