## Day 16 – Shell Scripting Basics
# Task 1: Your First Script
1)Create a file hello.sh
2)Add the shebang line #!/bin/bash at the top
3)Print Hello, DevOps! using echo Make it executable and run it
```

1)Add shebang and code
2)touch hello.sh
3)vim hello.sh
echo "HELLO DEVOPS"
4)echo "Hello, DevOps!"
5)chmod 777 hello.sh
6)./hello.sh
```
## output
<img width="1044" height="128" alt="Screenshot (80)" src="https://github.com/user-attachments/assets/0363826f-960c-4d10-9d34-4c5ec91601bd" />

# Task 2: Variables
Create variables.sh with:
A variable for your NAME
A variable for your ROLE (e.g., "DevOps Engineer")
Print: Hello, I am <NAME> and I am a <ROLE>
Try using single quotes vs double quotes — what's the difference?
```
1) touch variables.sh
2)vim variables.sh
3)NAME= Aliya ROLE="DevOps Engineer"
echo " my name is $NAME and i am a $ROLE "
4)chmod 777 variables.sh
5)./variables.sh
```
## output
<img width="1920" height="165" alt="Screenshot (81)" src="https://github.com/user-attachments/assets/052885dc-0b87-4c52-9104-de0f18593698" />

# Task 3: User Input with read
Create greet.sh that:
Asks the user for their name using read
Asks for their favourite tool
Prints: Hello <name>, your favourite tool is <tool>
```
1)touch greet.sh
2)vim greet.sh
3)#!/bin/bash
read -p "enter your name:" name
read -p "etner you fav tool:" tool
echo "hello $name ur fav tool is $tool"
~                                         
4)read -p "Enter your name: " name read -p "Enter your favourite tool: " tool
5)chmod 777 greet.sh
6)./greet.sh
```
## output 
<img width="1920" height="213" alt="Screenshot (82)" src="https://github.com/user-attachments/assets/d76536d0-bcc4-475f-83d6-52523f5dbfe9" />

## Task 4: If-Else Conditions
Create check_number.sh that:

Takes a number using read
Prints whether it is positive, negative, or zero
Create file_check.sh that:

Asks for a filename
Checks if the file exists using -f
Prints appropriate message
```
1)touch check_number.sh
2)add code:
read -p "Enter a number: " number

if [ "$number" -gt 0 ]; then
    echo "Positive number"
elif [ "$number" -lt 0 ]; then
    echo "Negative number"
else
    echo "Zero"
fi
3)chmod +x check_number.sh
4)./check_number.sh
```
```
1)vim file_check.sh
2)read -p "Enter the file path to check: " file_path

if [ -f "$file_path" ]; then
    echo "File is found"
else
    echo "No file with that name"
fi
3)chmod 777 file_check.sh
4)./file_check.sh
```

## output
<img width="1920" height="298" alt="Screenshot (83)" src="https://github.com/user-attachments/assets/561c8417-b98b-44ae-b4e7-5529b6e38676" />

<img width="1920" height="330" alt="Screenshot (85)" src="https://github.com/user-attachments/assets/c65f5bb9-2269-4eea-826b-fe5b10b221d6" />

## Create server_check.sh that:
Stores a service name in a variable (e.g., nginx, sshd)
Asks the user: "Do you want to check the status? (y/n)"
If y — runs systemctl status <service> and prints whether it's active or not
```
1) vim  server_check.sh
2) add code:
service="nginx"

read -p "Do you want to check the status of $service? (y/n): " choice

if [ "$choice" = "y" ]; then
    systemctl status "$service"

    if systemctl is-active --quiet "$service"; then
        echo "$service is ACTIVE (running)"
    else
        echo "$service is NOT running"
    fi
else
    echo "Skipped."
fi

3)chmod 746 server_check.sh
4)./server_check.sh
```
## output
<img width="1920" height="315" alt="Screenshot (84)" src="https://github.com/user-attachments/assets/ace81363-4628-4c9c-90a0-75ff1b3eed1f" />


## What i learned
```
Created and executed Bash scripts using shebang, permissions, and basic commands.
Worked with variables, user input (read), and conditional logic (if-else).
Built practical DevOps scripts to check files, numbers, and service status using systemctl.
```

