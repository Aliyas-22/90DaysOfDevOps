# file permission and file operation challenge 
## create files
```
touch devops.txt
touch notes.txt
touch script.txt
```
## edit the file 
```
vim devops.txt -> echo "hello everyone"
vim notes.txt -> echo "learning linux file permissions"
vim script.txt -> echo "hello devops"
```
## read the file 
```
cat devops.txt
cat notes.txt
cat script.txt
```
## display the first and last 5 line 
```
head -n 5 /etc/passwd
tail -n 5 /etc/passwd
```
## check for permission
```
ls -l
```
## setting the script.txt
```
chmod 450 script.txt
```
## setting the devops.txt to read-only
```
chmod 333 devops.txt
```
## setting the notes.txt  to read and write 
```
chmod 460 notes.txt
```
## Try writing to a read-only file - what happens?
```
permission denied
```
## Try executing a file without execute permission
```
command not found
```
## What i learned
```
i have learned that if a group dont have permission for rwx you can't accesses the file
and also creating and giving permission to files.
