# Linux File System Hierarchy 
## commands 
```bash 
 / (root) = this is the top most directory , all other folders live inside this
/home = this is For personal space ,like users file , document ,photos
/etc = configure file such as system setting , password config , network config ex. /etc/passwd
/usr = application program stores installed softwere ,libraries and program ex. /usr/bin (program) , /usr/lib (libraries)
/var = changing data where the things change everyday stores logs ,chache ,temprarory mail
/tmp = store temprory files and auto delete after reboot
/bin = stores commands like ls , mv , cat ,pwd ,cp
```
## Scenario-Based Practice

# Scenario 1: Service Not Starting

## A web application service called 'myapp' failed to start after a server reboot.
What commands would you run to diagnose the issue?
Write at least 4 commands in order.


```
step 1 :systemctl status myapp
 why: by using this command it will give me the running services names
step 2 : journalctl -u myapp -n 50
 why : by using this it will give which problem the myapp facing using logs and logs file will be big so i will tell give me last 50 lines of logs
step 3 : systemctl is-enabled myapp
 why: it will check is myapp is enabled to start on boot 

```

# Scenario 2: High CPU Usage

## Your manager reports that the application server is slow.You SSH into the server. What commands would you run to identify which process is using high CPU?

```
step 1 : top
why : it will give me live running processes list
step 2 : htop
why : it will give the user friendly interface to see running process
step 3 : ps aux --sort=-%cpu | head -10
why : by using this command it will give me list of running commands by sorting which proces is using high cpu from first 10 lines
```
# Scenario 3: Finding Service Logs

## A developer asks: "Where are the logs for the 'docker' service?" The service is managed by systemd.What commands would you use?

```
step 1 : journalctl -u ssh -n 50
why : systemd log process are in journald it give the logs of last 50 lines to view
step 2 : journalctl -u ssh -f
why : it will give dockers real time logs
```

# Scenario 4: File Permissions Issue

## A script at /home/user/backup.sh is not executing.When you run it: ./backup.sh ,You get: "Permission denied" 
What commands would you use to fix this?

```
step 1 : ls -l /home /usr/backup.sh
why : firstly i will check this file have permission or not in output i will focus on x which executable file which means this have permission if not
step 2 : chmod +x /home/usr/backup.sh
why : change mode will add permission x to the backup.sh file
step 3 :  ls -l /home /usr/backup.sh
why : to see the changes are done or not is there x is available
step 4 : ./backup.sh
why : run this file to check is it executing or not
```




 
