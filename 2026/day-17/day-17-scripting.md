# Day 17 – Shell Scripting: Loops, Arguments & Error Handling
## ask 1: For Loop
1)Create for_loop.sh that:
Loops through a list of 5 fruits and prints each one


2)Create count.sh that:
Prints numbers 1 to 10 using a for loop
```
1)-
vim for_loop.sh
for fruit in mango guvava orange pineapple strawbery
do
echo $fruit
done
2)-
vim count.sh
for num in {1..10}
do
echo $num
done
```
## outputs

<img width="1721" height="579" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/e58dab2a-3f77-4b3a-b6c5-589a731b22b4" />

## Task 2: While Loop
1)Create countdown.sh that:
Takes a number from the user


Counts down to 0 using a while loop
Prints "Done!" at the end
```
vim count.sh
read -p "enter the number:" num
while [ $num -ge 0 ]
do
echo $num
num = $((num - 1))
done
echo "done"
```
## output
<img width="1920" height="534" alt="Screenshot (92)" src="https://github.com/user-attachments/assets/d1756b96-c795-4b8b-88e7-8fadfef2e4c7" />

## Task 3: Command-Line Arguments
1) Create greet.sh that:
Accepts a name as ($1)


Prints Hello, <name>
If no argument is passed, prints "Usage: ./greet.sh "


2)Create args_demo.sh that:
Prints total number of arguments ($#)


Prints all arguments ($@)
Prints the script name ($0)

```
1)-
vim greet.sh
echo "hello $1"
./greet.sh Aliya
2)-
vim arg_demo.sh
echo "0th argument $0"
echo " 1st argument $1"
echo "total number of argument $#"
echo "list of argument $@"
```
## output

<img width="1574" height="357" alt="Screenshot (88)" src="https://github.com/user-attachments/assets/01b11db1-292a-4570-93c7-862755ec7539" />


## Task 4: Install Packages via Script
1)-Create install_packages.sh that:
Defines a list of packages: nginx, curl, wget


Loops through the list
Checks if each package is installed (use dpkg -s or rpm -q)


Installs it if missing, skips if already present
Prints status for each package
```
vim install_packages.sh
packages = ("nginx" "curl" "wget")
for packages in "${packages[@]}"
do
echo "checking $package
if dpkg -s "$package" &>/dev/null
then
echo "$package is already installed"
else
echo "$package not installed ,installing .."
sudo apt install -y "$package"
fi
```
## output

<img width="1920" height="389" alt="Screenshot (91)" src="https://github.com/user-attachments/assets/2755c57d-274d-4491-a2dd-eee6feaef014" />

## Task 5: Error Handling
1)Create safe_script.sh that:
Uses set -e at the top (exit on error)


Tries to create a directory /tmp/devops-test
Tries to navigate into it


Creates a file inside
Uses || operator to print an error if any step fails

```
vim safe_script.sh
set -e
mkdir /tmp/devops-test || {
    echo "Directory already exists"
    echo "Creating new directory"
    mkdir /tmp/devops_new
}

```
## output
<img width="1663" height="371" alt="Screenshot (89)" src="https://github.com/user-attachments/assets/acf0c5e9-384a-43d8-9158-655fc1a09db2" />

## WHAT I LEARNED 
### printing output, using while loops, handling command-line arguments with $1, automating package installation through scripts, and implementing basic error handling.
