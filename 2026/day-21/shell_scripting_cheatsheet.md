# Day 21 – Shell Scripting Cheat Sheet: Build Your Own Reference Guide
## Task 1: Basics
Document the following with short descriptions and examples:

Shebang (#!/bin/bash) — what it does and why it matters
+ shebang is a top most line of a script
+ that tells kernel which interpreter to use to execute the script

Running a script — chmod +x, ./script.sh, bash script.sh
+ use to change the direcotry mode
+ +x adds execute permission
+ example:- chmod +x <file_name>

Comments — single line (#) and inline
+ this means run the current file

Variables — declaring, using, and quoting ($VAR, "$VAR", '$VAR')
+ $var - basically this will print the value of variable
+ '$var' - this wil print exact word not the value means treat everything same
+ "$var" - it store the value of variable 

Reading user input — read
+ use to take input from the user
+ -p allow message to display 

Command-line arguments — $0, $1, $#, $@, $?
+ $0 - zero position argument
+ $1 - first position argument
+ $# - total number of argument
+ $@ - all argument
+ $? - last executed command

## Task 2: Operators and Conditionals
Document with examples:

String comparisons — =, !=, -z, -n
+ equal to =
```
  if [ "$name" = "Aliya" ]; then
  echo "Match"
fi
```
+ not equal to !=
```
if [ "$name" != "Aliya" ]; then
  echo "Match"
fi
```
Integer comparisons — -eq, -ne, -lt, -gt, -le, -ge
+ greater than 
 ```
  if [ "$num" -gt 10 ]; then
  echo "Big number"
fi
 ```
+ less than
```
  if [ "$num" -lt 10 ]; then
  echo "Big number"
fi
```
+ equal to
```
  if [ "$a" -eq "$b" ]; then
  echo "Both numbers are equal"
fi
```
+ not equal to
```
  if [ "$a" -ne "$b" ]; then
  echo "Numbers are not equal"
fi
```

File test operators — -f, -d, -e, -r, -w, -x, -s
+ -f file exists
+ -d directory exits
+ -e file or direcotry exits
+ -r read permission
+ -w write permission
+ -x execute permission

if, elif, else syntax
+ if
```
if [ condition ]; then
  commands
fi
```
+ if else
```
if [ condition ]; then
  commands
else
  commands
fi
```
+ elif
```
if [ condition1 ]; then
  commands
elif [ condition2 ]; then
  commands
else
  commands
fi
```

Logical operators — &&, ||, !
+ && - Both conditions must be true.
```
age=25

if [[ $age -gt 18 && $age -lt 60 ]]; then
  echo "Working age"
fi
```
+ || - At least one condition must be true.
```
day="Sunday"

if [[ $day == "Saturday" || $day == "Sunday" ]]; then
  echo "Weekend"
fi
```
+ ! - if not
```
file="test.txt"

if [[ ! -f $file ]]; then
  echo "File does not exist"
fi
```
## Task 3: Loops
Document with examples:

for loop — list-based and C-style
```
for (( i=1; i<=3; i++ ))
do
  echo $i
done

```
while loop
```
count=1

while [ $count -le 3 ]
do
  echo $count
done


```
until loop
```
num=1

until [ $num -gt 3 ]
do
  echo $num
  ((num++))
done

```

Loop control — break, continue
```
for i in 1 2 3 4 5
do
  if [ $i -eq 3 ]; then
    continue
  fi
  echo $i
done
```
## Task 4: Functions
Document with examples:

Defining a function — function_name() { ... }
```
greet() {
  echo "Hello"
}
 greet #Calling a function
```



Passing arguments to functions — $1, $2 inside functions
```
add() {
  echo $(($1 + $2))
}

add 5 3
```

Local variables — local
```
num=10   # global variable

test_func() {
  local num=5   # local variable
  echo "Inside function: $num"
}

test_func
echo "Outside function: $num"
```
## Task 6: Useful Patterns and One-Liners
Include at least 5 real-world one-liners you find useful. Examples:

Find and delete files older than N days
```
find /var/log/myapp -type f -name "*.log" -mtime +7 -delete

```
Count lines in all .log files
```
cat *.log | wc -l
```
Replace a string across multiple files
```
sed -i 's/oldtext/newtext/g' *.txt

```
Check if a service is running
```
systemctl is-active nginx
```
Monitor disk usage with alerts
```
usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$usage" -gt 80 ]; then echo "Disk usage above 80%!"; fi

```

Tail a log and filter for errors in real time
```
tail -f app.log | grep --line-buffered "ERROR"
```


Task 7: Error Handling and Debugging
Document with examples:

Exit codes — $?, exit 0, exit 1
```
ls file.txt
echo $?
```
```
if [ ! -f "file.txt" ]; then
  echo "File not found"
  exit 1
fi

exit 0
```
set -e — exit on error
set -u — treat unset variables as error
set -o pipefail — catch errors in pipes
set -x — debug mode (trace execution)
```
-e Exit the script immediately if any command fails.
-u Stop the script if an undefined variable is used.
-o if any command in a pipeline fails, the whole pipeline fails.
-x Print each command before executing it.


  
