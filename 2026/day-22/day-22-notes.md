# Task 1: Install and Configure Git
+ Verify Git is installed on your machine
   + git --version
+Set up your Git identity — name and email
   + git config --global <user.name>
+Verify your configuration
   + git config --list

# Task 2: Create Your Git Project
+ Create a new folder called devops-git-practice
   + mkdir devops-git-practice
+ Initialize it as a Git repository
   + git init devops-git-practice
+ Check the status — read and understand what Git is telling you
    + git status


# Task 3: Create Your Git Commands Reference
+ Create a file called git-commands.md inside the repo
     + vim git-commands.md
+ Add the Git commands you've used so far, organized by category:
+ For each command, write:
     + git init <filename> :- helps to initialize new git repository
     + git add <filename>  :- it adds the working direcotry to stageing area
     + git commit -m " message" :- save the snapshot of project/repo
     + git clone <httpurl> : helps to create a local copy of an existing git repository
     + git status :-  to monitat the state of repo or working direcotry
       
+ Setup & Config
    + git config --global user.name
  
+ Basic Workflow
    + git init <filename>
    + git add <filename>
    + git commit -m "message"
      
+ Viewing Changes
    + git status

# Task 4: Stage and Commit
+ Stage your file
    + git add <filename>
+ Commit with a meaningful message
    + git commit -m " initial commit"
+ View your commit history
    + git log
    + git log --oneline

# Task 5: Make More Changes and Build History
+ Edit git-commands.md — add more commands as you discover them
     + git status
     + git branch
     + git log
     + git log --oneline
+ Check what changed since your last commit
     + git log
+ Stage and commit again with a different, descriptive message
     + git add git-commands.md
     + git commit -m " new commands "
      
# Task 6: Understand the Git Workflow
Answer these questions in your own words (add them to a day-22-notes.md file):

+ What is the difference between git add and git commit?
    + git add - adds the working direcotry to stageing area & git commit - save the snapshot of project/repo
   
+ What does the staging area do? Why doesn't Git just commit directly?
    + taging acts as a middle ground between your actual project files (working directory) and the saved history repository
+ What information does git log show you?
    + commit id ,commit message from which branch with sequence
+ What is the difference between a working directory, staging area, and repository?
    + the working directory is for active editing, the staging area is for preparing specific changes, and the repository is for permanent storage of your project's history 

# screenshots
<img width="1920" height="298" alt="Screenshot day22 2" src="https://github.com/user-attachments/assets/4553ef4a-2839-428c-9849-95262fd44834" />
<img width="1920" height="208" alt="Screenshot day 22" src="https://github.com/user-attachments/assets/bf7e5bc6-8e95-462e-8be4-38f707a97193" />


