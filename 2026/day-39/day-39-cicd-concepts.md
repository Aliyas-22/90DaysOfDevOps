  # Day 39 – What is CI/CD?
## Task 1: The Problem

### Think about a team of 5 developers all pushing code to the same repo manually deploying to production.

+ Write in your notes:

   + *What can go wrong?*
       + **When multiple devloper manually deploy to production this cause sevral problems such  as:**
       + **coping file**
       + **running commands manually can be risky because sometimes we are upload files or we uploaded *wroung files or may missed enviroment variable***
       + **down time risk will increase**
       + **security risk accidentalial deletion possiable**
     
   + *What does "it works on my machine" mean and why is it a real problem?*
 
     
        **this is a real problem because when devloper builds application and inside devloper's computer**
        **which helps to runthe application also the library ,database version are avialable**
        **On the other hand the clint doesn't have this dependencies so this cause production failure , Delays releases, create enviroments**
     
   + *How many times a day can a team safely deploy manually?*
     
        **once in a day a day team can safely deploy manually**

---
## Task 2: CI vs CD

### Research and write short definitions (2-3 lines each):

  + *Continuous Integration — what happens, how often, what it catches*
    
      **Developers regularly push their code to a shared repository, and automatically the system builds and tests the code.**
    
  + *Continuous Delivery — how it's different from CI, what "delivery" means*
    
      **After CI successfully builds and tests the code, the application is automatically prepared and made ready for production deployment.**
  
  + *Continuous Deployment — how it differs from Delivery, when teams use it*
    
     **Every successful change that passes CI automatically gets deployed to production without human approval.**

*Write one real-world example for each.*
### 1) contineous integration
 **shared Google Doc used by 5 people writing a report,Every time someone edits, Google automatically saves it It checks formatting**
 **That automatic saving + conflict detection = Continuous Integration concept**
###  2) contineous delivery

**suppose we are ordering from Amazon - Item packed -Label printed -Ready for shipping -But shipment happens only when warehouse manager approves it so That approval step = Continuous Delivery,**
**System is ready to deploy but human decides**

### 3) Continuous Deployment 

**Whenever Instagram developers fix a small bug, it automatically goes live to users without waiting for manager approval.No manual button.**
**As soon as code passes tests, it goes live automatically = Continuous Deployment**

---
## Task 3: Pipeline Anatomy

### A pipeline has these parts — write what each one does:

  + *Trigger — what starts the pipeline*
     + whenever we
        - pull
        - push
        - manual clicked
        
  +  *Stage — a logical phase (build, test, deploy)*
      +  build: The system compiles source code, resolves dependencies
      +  test: Automated testing runs across multiple layers: unit tests
      +  deploy : The deployment automation system releases the application to: Development
    
  +  *Job — a unit of work inside a stage*
      + it will
         - run the unit that test
         - run integration
         - runs unit that deploy
  +  *Step — a single command or action inside a job*
      + we give 
         - one command
         - or action to perform 
  +  *Runner — the machine that executes the job*
      + which could be any
         - ubuntu
         - windows
         - macos
         - self-hosted
  +  *Artifact — output produced by a job*
      + compiled
      + test report
      + docker image 

---
## Task 4: Draw a Pipeline

### Draw a CI/CD pipeline for this scenario:

# *A developer pushes code to GitHub. The app is tested, built into a Docker image, and deployed to a staging server.*
*Include at least 3 stages. Hand-drawn and photographed is perfectly fine.*

![WhatsApp Image 2026-03-04 at 2 26 16 PM](https://github.com/user-attachments/assets/7d3b5441-2fed-4123-833a-8654a9f5cfca)


---
## Task 5: Explore in the Wild

  + Open any popular open-source repo on GitHub (Kubernetes, React, FastAPI — pick one you know)
  + https://github.com/frappe/frappe/blob/develop/.github/workflows/create-release.yml
    + Find their .github/workflows/ folder
    + Open one workflow YAML file
  ```YAML
    name: Generate Semantic Release
on:
  push:
    branches:
      - version-14-beta
permissions:
  contents: read

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Entire Repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: 24
      - name: Setup dependencies
        run: |
          npm install @semantic-release/git @semantic-release/exec --no-save
      - name: Create Release
        env:
          GH_TOKEN: ${{ secrets.RELEASE_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.RELEASE_TOKEN }}
          GIT_AUTHOR_NAME: "Frappe PR Bot"
          GIT_AUTHOR_EMAIL: "developers@frappe.io"
          GIT_COMMITTER_NAME: "Frappe PR Bot"
          GIT_COMMITTER_EMAIL: "developers@frappe.io"
        run: npx semantic-release
```
  
  +  Write in your notes:
    
     + What triggers it?
        
        -  **Runs on push**
        -  **Branch version-14-beta**
          
     + How many jobs does it have?
        - **one job**
     + What does it do? (best guess)
        - **it is downloading the repository**
        - **and also it is installing the node js**
        

