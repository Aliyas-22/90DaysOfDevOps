## Day 09 – Linux User & Group Management
# to add newuser
```
sudo useradd -m barlin
sudo useradd -m tokyo
sudo useradd -m professor
```
# to create groups
```
sudo groupadd devlopers
sudo groupadd admins
```
# give access to user of groups
```
sudo gpasswd -a tokyo devlopers
sudo gpasswd -a professor admins
sudo usermod -aG devlopers,admins barlin
```
#to see the groups
```
getent groups
```
<img width="1920" height="549" alt="Screenshot (38)" src="https://github.com/user-attachments/assets/17c82107-53ff-46ad-b4b1-a2a1921669fd" />
