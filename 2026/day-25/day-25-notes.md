# Day 25 – Git Reset vs Revert & Branching Strategies
## Task 1: Git Reset — Hands-On
### Make 3 commits in your practice repo (commit A, B, C)
### Use git reset --soft to go back one commit — what happens to the changes?
  + After doing ```git rest --soft Head~1``` head~1 means (c) so the c is removed from the history
  + heand is pointing to B
  + and in ``` git status ``` i see the changes of (C) is in staging area

# OUTPUT
<img width="1920" height="400" alt="Screenshot (153)" src="https://github.com/user-attachments/assets/ae08c497-b95f-4f97-8cf8-677ad846cb14" />
<img width="1920" height="380" alt="Screenshot (152)" src="https://github.com/user-attachments/assets/e00fe6fc-75ab-4057-be18-a99d4d212ff3" />


### Re-commit, then use git reset --mixed to go back one commit — what happens now?
  + After doing ``` git reset --mixed HEAD~1 ``` commit (C)is removed
  + heand pointing to (B)
  + but they move to working directory (unstaged)

# OUTPUT
<img width="1920" height="955" alt="Screenshot (154)" src="https://github.com/user-attachments/assets/eff04f75-96ef-4b90-9591-f9aa000377b6" />


### Re-commit, then use git reset --hard to go back one commit — what happens this time?
  + after doing ``` git reset --hard HEAD~1 ``` commit (C) will removed
  + Head pointing to (B)
  + All changes are deleted from c
  + working directory is clean

# OUTPUT
<img width="1920" height="964" alt="Screenshot (155)" src="https://github.com/user-attachments/assets/f5b3afd7-9b54-4511-af21-7ecc005d2178" />


## Answer in your notes:
### What is the difference between --soft, --mixed, and --hard?
  + ``` --soft ``` :- it removes the comit ,but keeps the changes staged
  + ``` --mixed ```:- it removes the commit and unstaged the changes
  + ``` --hard ``` :- it delete the commit and make working direcotry clean
### Which one is destructive and why?
  + git --hard is distructive because it deletes commits + staging changes + working directory changes so data will loss 
### When would you use each one?
  + ``` --soft ``` : when i want to change commit message or keep changes staged
  + ``` -- mixed ``` : when i want to re-edit files and re-stage file properly
  + ``` --hard ``` : when i want to completely delete the changes nd clean the brnach
### Should you ever use git reset on commits that are already pushed?
  + no


## Task 2: Git Revert — Hands-On
### Make 3 commits (commit X, Y, Z)
### Revert commit Y (the middle one) — what happens?
  + ``` git revert <commit id> ``` 
### Check git log — is commit Y still in the history?
  + yes after doing y is still in the history but the new commits that reverse the changes of that commit

# OUTPUT
<img width="1920" height="586" alt="Screenshot (156)" src="https://github.com/user-attachments/assets/e8a08406-a3ff-40d1-a1a7-14cf9893da61" />
<img width="1920" height="467" alt="Screenshot (157)" src="https://github.com/user-attachments/assets/0fb576b9-7dda-4b04-8a26-e182d40e7b4f" />


## Answer in your notes:
### How is git revert different from git reset?
  + git reset removes commits from branch history and also delete when we use --hard
  + git revert does not commit that undoes the changes ,keep history safe 
### Why is revert considered safer than reset for shared branches?
  + git revert is safer because it does not rewrite history it creates a new commit that undoes changes so everyone in the team stay in sync.
  + git reset changes hisotry and requires force push which can break other developers branches.
### When would you use revert vs reset?
  + i will use git revert when i am working on a shared branches
  + i will use git reset when the commit is not pushed yet

## Task 3: Reset vs Revert — Summary
## Create a comparison in your notes:

|             | git reset	| git revert |
--------------|-------------|------------|
 What it does | git reset moves the branch pointer and rewrites history	  |	git revert creates a new commit that cancels the previous one|
Removes commit from history? |	yes |	no|
Safe for shared/pushed branches? |	no |	yes|
 When to use | 	when working on locally and commit is not pushed yet	| when working on shered or pushed branches|

## Task 4: Branching Strategies
## Research the following branching strategies and document each in your notes with:

### How it works (short description)
### A simple diagram or flow (text-based is fine)
### When/where it's used
  + gitflow :- Large teams, scheduled releases, projects with planned release cycles
  + github flow :- Projects with continuous deployment, small or medium teams
  + Trunk-Based Development :- Startups, teams practicing continuous integration, projects needing fast delivery
## Pros and cons
   + gitflow :-
     + pros
         + Clear structure, separates development
         + good for managing multiple features and releases
      + cons
         + Complex and slow
         + small or fast moving teams
   + github flow :-
     + pros
        + Simple, fast,
        + easy to manage
      + cons
        + harder to manage so many releases
   + trunk-based devlopment :-
     + pros
        + Very fast
        + reduces merge conflicts
        +  main always deployable
      + cons
        + Harder to manage if too many developers
### GitFlow — develop, feature, release, hotfix branches
  + main = The main branch holds production-ready code
  + devlop = The develop branch is for ongoing development
  + feature = Developers create feature branches from develop to work on new features
  + release = Once a release is ready, a release branch is created from develop and eventually merged into main (and back into develop)
  + hotfix = if urgent bugs appear in production, hotfix branches are created from main and merged back into both main and develop
    + diagram
      
  main
  |
  |--- hotfix
  |
develop
  |--- feature
  |
  |--- release

### GitHub Flow — simple, single main branch + feature branches
   + main = The main branch (main) always holds deployable code
   + feture = Developers create feature branches off main to work on new features or bug fixes
   + the feature is merged back into main There are no long-lived develop or release branches and deployments happen directly from main
        + Diagram
  main
  |
  |--- feature
  |--- feature
  |--- hotfix

### Trunk-Based Development — everyone commits to main, short-lived branches
 + Trunk-Based Development is a simple and fast branching strategy
 + There is only one main branch (trunk) in tbd
 + Developers create very short-lived feature branches this helps Lasting just a few hours, and merge them back into the main branch frequently
 + this will minimize the conflict and made branch ready to deply
      + Daigram
main
  |
  |--- feature-short-lived
  |--- feature-short-lived

   
## Answer:
### Which strategy would you use for a startup shipping fast?
  + I would use Trunk-Based Development for a startup that needs to ship fast
  + It allows developers to create very short-lived feature branches,
  + often lasting only a few hours, and merge them back into the main branch frequently
  + This reduces conflicts, keeps the main branch always deployable, and allows the team to release new features quickly.
### Which strategy would you use for a large team with scheduled releases?
  + For a large team with scheduled releases, I will use GitFlow
  + In GitFlow the develop branch is used for ongoing development,
  + feature branches are used to add new features,
  + and hotfix branches are used to fix urgent bugs
  + Once everything is ready and stable, a release branch is created and merged into main for deployment
  + This structure helps large teams coordinate work, manage releases, and ensure the main branch stays stable





    
