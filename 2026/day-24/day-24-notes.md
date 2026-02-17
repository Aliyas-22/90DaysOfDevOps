#  Day 24 – Advanced Git: Merge, Rebase, Stash & Cherry Pick
## Task 1: Git Merge — Hands-On
### Create a new branch feature-login from main, add a couple of commits to it
  + ``` git checkour -b feature-login ```
### Switch back to main and merge feature-login into main
  + ``` git switch ```
### Observe the merge — did Git do a fast-forward merge or a merge commit?
<img width="1920" height="219" alt="Screenshot (135)1" src="https://github.com/user-attachments/assets/4e6eab2b-0470-4b0e-b9fd-ef40598336af" />

### Now create another branch feature-signup, add commits to it — but also add a commit to main before merging
 + ``` git checkout -b feature-signup ```
### Merge feature-signup into main — what happens this time?
 + ``` git merge feature-signup ```
 + it opend the editor and 
 + i saw (merge branch 'feature-signup') wants me to commit the message 
## Answer in your notes:
### What is a fast-forward merge?
 + fast-forward merge happens when git can merge a branch by simply moving the branch pointer forward without creating a merge commit 
### When does Git create a merge commit instead?
 + git creates a merge commit when the two brnches have diverged meaning both branches have new commits and git cannot fast-forward.
### What is a merge conflict? (try creating one intentionally by editing the same line in both branches)
+ A merge conflict occurs when git cannot automatically merge changes because the same part of a file was modified diffrently in both branches.

## Task 2: Git Rebase — Hands-On
### Create a branch feature-dashboard from main, add 2-3 commits
  + ``` git checkout -b feature-dashboard ```
### While on main, add a new commit (so main moves ahead)
### Switch to feature-dashboard and rebase it onto main
+ ``` git checkout -b feature-dashboard ```
+ ``` git rebase main ```
<img width="1920" height="242" alt="screenshot abc" src="https://github.com/user-attachments/assets/fc657608-9f63-4176-a385-a1726845c61e" />

### Observe your git log --oneline --graph --all — how does the history look compared to a merge?
  + git merge creates a branching history with a merge commit while rebase creates a linear history by rewriting commits without merge commit.

    <img width="1920" height="434" alt="Screenshot (138)" src="https://github.com/user-attachments/assets/95ca4983-4a75-47f0-9af6-a6ba96816d47" />
## Answer in your notes:
### What does rebase actually do to your commits?
 + rebase rewrites your commits by replaying them on top of another branch , creating new commit ids and changing their base 
### How is the history different from a merge?
 + merge keeps the original branch structure and adds a merge commit, creating a branching non linear history while rebase rewrites and replays commit onto another base basically it produce a clean linear hisotry.
### Why should you never rebase commits that have been pushed and shared with others?
 + because rebase rewrites the commits ,commits ids which breaks others history and couse conflicts 
### When would you use rebase vs merge?
 + we can rebase when we are working on private or a local branch
 + merge for safe collabration and shared branches

## Task 3: Squash Commit vs Merge Commit
### Create a branch feature-profile, add 4-5 small commits (typo fix, formatting, etc.)
  + ``` git checkout -b feature-profile ``` 
### Merge it into main using --squash — what happens?
  + ``` git merge --squash feature-profile ```
### Check git log — how many commits were added to main?
<img width="1920" height="916" alt="Screenshot (140)" src="https://github.com/user-attachments/assets/2eb09586-5de0-4d50-9c07-fbf66e1cfb02" />

### Now create another branch feature-settings, add a few commits
  + ``` git checkout -b feature-setting ```

### Merge it into main without --squash (regular merge) — compare the history
  +  the diffrence is that git merge history look messy but its complete history
  + in squash clean history but feature commits are lost in main
<img width="1920" height="568" alt="Screenshot (141)" src="https://github.com/user-attachments/assets/17383574-fed8-4bb5-b70f-ebe6d261cbcf" />
    
## Answer in your notes:
### What does squash merging do?
  + A sqaush merge applies the changes of a branch but not its individual commit history 
### When would you use squash merge vs regular merge?
  + use squash merge for a clean, simplified history
  + and use regular merge when you need to preserve  full commit history 
### What is the trade-off of squashing?
  + trade - off squashing is cleaner history at the cost if losing detailed commit .

## Task 4: Git Stash — Hands-On
### Start making changes to a file but do not commit
<img width="1920" height="258" alt="Screenshot (143)" src="https://github.com/user-attachments/assets/4b88a02c-f6d6-4685-9ebb-b7cbb2b61cf0" />
<img width="1920" height="310" alt="Screenshot (144)" src="https://github.com/user-attachments/assets/8f25517a-ccde-44e4-b862-2fd408400a35" />

### Now imagine you need to urgently switch to another branch — try switching. What happens?
  + git allows switching branches with uncommited changes if they dont conflict with the target the branch 
### Use git stash to save your work-in-progress
<img width="1920" height="590" alt="Screenshot (145)" src="https://github.com/user-attachments/assets/15a0a5d8-c7df-41ad-9881-37de5bdc7d1a" />
### Switch to another branch, do some work, switch back
  + git switch main
  + echo "add changes " > app.txt
  + git stash
### Apply your stashed changes using git stash pop
  + ``` git stash hello.txt ```
### Try stashing multiple times and list all stashes
  + ``` git stash list ```
### Try applying a specific stash from the list
  + ```git stash apply ``` 
## Answer in your notes:
## What is the difference between git stash pop and git stash apply?
  + git stash apply resotres the stashed changes keeps the stash saved and we can reuse it again
  + git stash pop resotres the stashed changes
  + delete the stash after applying and only one time use 
## When would you use stash in a real-world workflow?
  + when i want to switch branch urgently and the half code is written and dont want to commit it so that time i will use git stash so this will saves modified and staged changes and make it safe to switch barnches
    
## Task 5: Cherry Picking
### Create a branch feature-hotfix, make 3 commits with different changes
  + ``` git checkout -b feature-hotfix ```
   <img width="1920" height="979" alt="Screenshot (147)" src="https://github.com/user-attachments/assets/94c6129d-28f5-435f-bdf6-34fa90c79bd7" />

### Switch to main
 + ``` git switch main ```
### Cherry-pick only the second commit from feature-hotfix onto main
<img width="1920" height="499" alt="Screenshot (151)" src="https://github.com/user-attachments/assets/3e7ecfdb-44dc-4a19-a817-f6d0a5eb76c1" />

### Verify with git log that only that one commit was applied
<img width="1920" height="284" alt="Screenshot (149)" src="https://github.com/user-attachments/assets/8e028bb2-5b4c-4bc9-995d-b1c176994ca5" />

## Answer in your notes:
### What does cherry-pick do?
  + copy a specific commit from one branch and apply it onto our current branch
### When would you use cherry-pick in a real project?
  + when i need specific commit but do not want the enitre branch to be commit 
###  What can go wrong with cherry-picking?
  + cherry pickiking dublicates commits future merge conflict and hisotry inconsistance if overuse 
