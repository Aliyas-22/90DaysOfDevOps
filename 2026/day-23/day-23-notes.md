# TASK 1
## What is a branch in Git?
   + a brach is a movaable pointer to a specific commit 
## Why do we use branches instead of committing everything to main?
   + because the main branch is highly important and stable so its best practice to not interrupt it
## What is HEAD in Git?
   + it is a pointer that point towards the current location 
## What happens to your files when you switch branches?
   + when we switch the branch git updates directory and file change according to that branch last commit

# TASK 3 
## List all branches in your repo
 + TWO BRANCHES 
    + main
    + dev
## Create a new branch called feature-1
 + git branch feature-1
## Switch to feature-1
 + git switch feature-1
## Create a new branch and switch to it in a single command — call it feature-2
 + git checkout -b feature-2
## Try using git switch to move between branches — how is it different from git checkout?
 + git switch feture-2
 + git switch helps only to switching the branches and git checkout switch branches plus restore the file. 
## Make a commit on feature-1 that does not exist on main
 + vim notes.md
 + git add notes.md
 + git commit -m  "chore:minor changes"
 + git push origin dev
## Switch back to main — verify that the commit from feature-1 is not there
 + git switch main 
 + feature-1 commits are not in the main
## Delete a branch you no longer need
 + git branch -d feature-2

## TASK 3
## Create a new repository on GitHub (do NOT initialize it with a README)
 + vim gittest
 + git init
 + git add gittest
 + git commit -m " add file"
 + git switch main
 + git push origin main
## Connect your local devops-git-practice repo to the GitHub remote
 + git clone <httpurl>

## Push your main branch to GitHub
 + git push origin main
## Push feature-1 branch to GitHub
 + git push origin feature-1
## Answer in your notes: What is the difference between origin and upstream?
 + origin is the personal copy of our github project
 + upstream is the original project owned by the main so upstream use to pull the request 
# TASK 4 
 ## Make a change to a file directly on GitHub (use the GitHub editor)
## Pull that change to your local repo
 + git pull origin main
## Answer in your notes: What is the difference between git fetch and git pull?
 + git fetch only download the new data from the github to local it does not change any current file 
 + git pull downloads the new dats and immidiatley mergs it into current branch 
# TASK 5
## Answer in your notes:
## What is the difference between clone and fork?
+ git clone is use to create copy of repository to local
+ git fork use to create copy of someone else reposirotry to our github 
## When would you clone vs fork?
 + when i want to work locally on my project i will use clone 
 + when i want to take someone else repository inside my github i will use fork
## After forking, how do you keep your fork in sync with the original repo?
 + i will add the original repository to an upstream and fetch chenges from upstream and merge them to my main and push to the origin

   # screenshots
   <img width="1501" height="129" alt="Screenshot day23png" src="https://github.com/user-attachments/assets/1b0f8f07-dbdb-4627-abca-e8307867c0e9" />
<img width="1920" height="208" alt="Screenshot day 22" src="https://github.com/user-attachments/assets/4342bb7f-4037-4c87-8c29-b9127812fc22" />
<img width="1920" height="165" alt="Screenshot day22 2" src="https://github.com/user-attachments/assets/a613969f-8965-4525-9cda-c0b692970767" />

