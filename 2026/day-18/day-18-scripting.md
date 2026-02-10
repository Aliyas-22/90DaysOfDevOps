# Day 18 – Shell Scripting: Functions & Slightly Advanced Concepts
## Task 1: Basic Functions
1- Create functions.sh with:
A function greet that takes a name as argument and prints Hello, <name>!
```
1)vim function.sh
2)greet() #create function
3) echo "hello"
4) greet #call
```
2- A function add that takes two numbers and prints their sum
Call both functions from the script
```
1)  read -p "enter the number1:" num1 #input
2)  read -p "enter the number 2:" num2
3) add() #create function
4) num1=$1 num2=$2 #variable assign
5) sum = $((num1+num2)) #condition
6)echo "the sum of num1 and num2is: $sum"
7)add $num1 $num2 #call
```
## OUTPUT
<img width="1920" height="620" alt="Screenshot (98)" src="https://github.com/user-attachments/assets/edd56317-e4d1-4cf5-b20b-c2d227c2673d" />


## Task 2: Functions with Return Values
1- Create disk_check.sh with:
A function check_disk that checks disk usage of / using df -h
```
1)vim disk_check.sh
2)check_disk() #create function
3)echo "checking the disk usage"
4)df -h #command
5) check_disk #call
```
## OUTPUT
<img width="1920" height="406" alt="Screenshot (99)" src="https://github.com/user-attachments/assets/79d4e658-a8a0-4f59-b522-c260ad61b995" />



2- A function check_memory that checks free memory using free -h
A main section that calls both and prints the results
```
1)vim check_memory
2)check_my_memory() #function
3)echo"checking memory "
4) free -h #commnad
5)check_my_memory #call
```
## OUTPUT
<img width="1920" height="165" alt="Screenshot (99)" src="https://github.com/user-attachments/assets/42417007-edee-4c04-ac94-f011370a6b39" />


## Task 3: Strict Mode — set -euo pipefail
Create strict_demo.sh with set -euo pipefail at the top
Try using an undefined variable — what happens with set -u?
Try a command that fails — what happens with set -e?
Try a piped command where one part fails — what happens with set -o pipefail?
Document: What does each flag do?

## set -u →
```
1)vim strict_demo.sh
2)echo "hello $name"
```
### DOCUMENTATION:
#### set -u → stops script when using undefined variable


## set -e →
```
1)mkdir test.txt8
2)mkdir test.txt7
3)echo "done"
```
### DOCUMENTATION:
#### set -e → stops script when any command fails


## set -o pipefail →
```
1)echo "--- in this -0 use ---"
2)cat hello.txt | grep hello
```
### DOCUMENTATION
#### set -o pipefail → fails pipeline if any command fails

## OUTPUT
<img width="1920" height="370" alt="Screenshot (100)" src="https://github.com/user-attachments/assets/a5a107ad-ed82-4eef-b037-ab5e15b8331a" />

## Task 4: Local Variables
Create local_demo.sh with:
A function that uses local keyword for variables
Show that local variables don't leak outside the function
Compare with a function that uses regular variables 
```
1)learn_local() #CREATE FUNCTION
2)local local_vari="i am local" #USE LOCAL VARIABLE
3) echo "inside the function local: $local_vari" ##INSIDE IT WILL PRINT VARIBALE VALUE
4) learn_global() #CREATE FUNCTION
5)global_vari="i am global" #USE REGULAR VARIBALE
6)  echo "inside the function global: $global_vari"
7)learn_local #CALL 
8)echo "outside the function: $local_vari" ##OUTSIDE THE FUNCTION
9)learn_global #CALL
10)echo "outside the function: $global_vari" ## OUTSIDE THE FUNCTION
```
## OUTPUT
<img width="1920" height="262" alt="Screenshot (102)" src="https://github.com/user-attachments/assets/ab6fe7e3-6308-442e-891e-3efafb1ccd15" />

## Task 5: Build a Script — System Info Reporter
Create system_info.sh that uses functions for everything:

1- A function to print hostname and OS info
```
my_info(){
        echo "------ system information ------"
        local host_name
        host_name=$(hostname -s)
        echo "hostname is :$host_name"

}
```
2-A function to print uptime
```
my_uptime(){
        echo "------- system uptime --------"
        local up_time
        up_time=$(uptime -p)
        echo "uptime is :$up_time"
}
```
3-A function to print disk usage (top 5 by size)
```
my_disk_usage(){
        echo "--------------- disk usage ---------------"
        du -h / 2>/dev/null | sort -rh | head -n 5 || true
        }
```


4-A function to print memory usage
```
my_memory_usage(){
        echo "--------------- memory usage ---------"
        local memory_usage
        memory_usage=$(free -m)
        echo "free memory is :$memory_usage"
}
```
5-A function to print top 5 CPU-consuming processes
```
        echo "------------------  top 5 cpu process -------------"
        ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6
        echo
        echo "Finished"
        }
```
6-A main function that calls all of the above with section headers
```
main(){
        my_info
        my_uptime
        my_memory_usage
        my_disk_usage
        my_cpu_process
}
main
```
## output
<img width="1920" height="766" alt="Screenshot (103)" src="https://github.com/user-attachments/assets/a94e2d0d-9429-4dc1-a030-52eb3b04ae29" />

## What I learned:
+ Created and used Bash functions to organize and reuse code efficiently

+ Learned how to call functions to perform specific tasks

+ Built functions to check system memory and disk usage

+ Understood the difference between local and global variables

+ Used local variables inside functions to keep data limited and avoid unwanted changes

+ Learned that local scope improves code safety and maintainability

+ Practiced writing scripts in strict mode using set -euo pipefail

Understood that:

+ set -e → exit script when a command fails

+ set -u → error on undefined variables

+ set -o pipefail → fail the script if any command in a pipeline fails


