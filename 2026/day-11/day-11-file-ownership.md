# Day 11 – File Ownership Challenge (chown & chgrp)
## TASK 1 -> create file and user then change it owner
```
touch devops-file.txt
ls -l
sudo useradd -m tokyo
sudo passwd tokyo
sudo chown tokyo devops-file.txt
```
## TASK 2 -> CREATE FILE AND GROUP AND CHANGE ITS GROUP
```
touch team-notes.txt
ls -l
sudo groupadd heist-team
sudo chgroup heist-team team-notes.txt
```
## TASK 3 -> CREATE FILE AND USER ,GROUP AND CHAGNE IT TOGETHER
```
touch project-config.yaml
sudo useradd -m professor
sudo passwd professor
sudo chown professor:hiest-team project-config.yaml
```
## TASK 4 -> CREATE FOLDER AND USER AND CHANGE ITS GROUP AND USER OF DIRECTORY
```
  mkdir app-logs
  sudo useradd -m barlin
  sudo passwd barlin
  chown -R barlin:hiest-team app-logs/
```
## TASK 5 ->  CREATE DIRECTORY AND INSIDE THE DIRECTORY CHANGE ITS OWNER 
```
  mkdir -p heist-project/vault
  mkdir -p heist-project/plans
  touch heist-pject/vault/gold.txt
  touch heist-project/plans/statergy.txt
  sudo groupadd planner
sudo chown -R professor:planner heist-project/
ls -lR heist-projet
```
## TASK 6 -> CREATE DIRECTORY ANF FILE ,USER , CHANGE OWNERSHIP AND GROUP OF EACH FILE
```
  sudo useradd nairobi
sudo passwd nairobi
sudo groupadd vault-team
sudo group-add tech-team
mkdir -p bank-heist/access-codes.txt
touch bank-heist/access-codes.txt
touch bank-heist/escape-plan.txt
touch bank-heist/blueprints.pdf
chown tokyo:vault-team bank-heist/acess-code.txt
chown nairobi: vault-team bank-heist/escape.txt
shown barlin : tech team bank-heist/blueprints.pdf
ls -l bank-heist
```

<img width="1920" height="308" alt="Screenshot (52)" src="https://github.com/user-attachments/assets/8b37805e-d76f-458f-b672-2335ff7df71e" />
<img width="1920" height="745" alt="Screenshot (53)" src="https://github.com/user-attachments/assets/4de44e00-66c5-4bd3-88e7-4b1182125138" />
<img width="1583" height="824" alt="Screenshot (54)" src="https://github.com/user-attachments/assets/b4b2841c-fc56-4a44-a56f-6d65efc94ee4" />
<img width="1920" height="170" alt="Screenshot (51)" src="https://github.com/user-attachments/assets/d427c801-08d2-4ba3-a716-5a95db72dcd7" />


