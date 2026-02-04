# Day 12 – Breather & Revision (Days 01–11)
## systemd commands
```
sudo systemctl status <service name>
sudo systemctl start <service name>
journalctl <service name>
```
## read and write the file
```
makdir devops-file
cd devops-file
touch notes.txt
echo "hello" > notes.txt
echo "devops" >> notes.txt
tail -2 notest.txt | tee output.txt
```
## file permission
```
mkdir learning
cd learning
touch learn.txt
ls -l
sudo useradd -m sunday
sudo passwd sunday
sudo groupadd week
chmod 750 learn.txt
chown sunday:week learn.txt
```
##  5 you’d reach for first in an incident
```
ps
top
ls
curl
```
## create user and chaange its ownership 
```
mkdir devops
touch devops.txt
sudo useradd aliya
sudo passwd aliya
sudo groupadd learning
chown -R aliya:learning devops/
chmod 750 devops/
```
## Mini Self-Check 

### Which 3 commands save you the most time right now, and why?
the three commands save me the most time are:
```
ls -l
to see the file permission and ownership
```
```
cd
to navigate quickly accross directory
```
```
journalctl -u <service name>
checking logs
```
### How do you check if a service is healthy? List the exact 2–3 commands you’d run first
```
systemctl status <service>
to check service is active or not
```
```
journalctl <service name>
to analyze logs
```
```
ps aux | grep service
to confirm process is running
```
### How do you safely change ownership and permissions without breaking access? Give one example command
i use chown to change ownership and chmod to adjust permission carefully.
```
sudo chown -R user:group folder-name
```
```
chmod 750 file-name
```
### What will you focus on improving in the next 3 days?
```
in next three days i will focus on mastaring linux file permission and ownership and
i plan to practice chmod.chown and file permission modes like 755 and 644 ..
