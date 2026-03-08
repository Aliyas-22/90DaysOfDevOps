# Day 42 – Runners: GitHub-Hosted & Self-Hosted
## Task 1: GitHub-Hosted Runners
+ Create a workflow with 3 jobs, each on a different OS:
+ ubuntu-latest
    + ```YML
      runs-on: ubuntu-latest
      ```
      
+ windows-latest
    + ```YML
      runs-on: windows-latest
      ```
+ macos-latest
    + ```YML
      runs-on: macos-latest
      ```
      
+ In each job, print:
+ The OS name
+ The runner's hostname
+ The current user running the job
    + ```YMl
      name: Print OS and runner info
              run: |
                  echo "Running on ${{runner.os}}"
                  echo "Hostname: $HOSTNAME"
                  echo "Current user: $USER"
      ```
+ Watch all 3 run in parallel
+ Write in your notes: What is a GitHub-hosted runner? Who manages it?
    + **GitHub-hosted runners are virtual machines or containers for single-CPU runners that GitHub provisions to execute jobs in GitHub Actions workflows**
    + **GitHub maintains the runner app and OS images**

<img width="1920" height="916" alt="Screenshot (297)" src="https://github.com/user-attachments/assets/2b40c73d-29f1-48e8-b2e3-cf1f3f388113" />
<img width="1920" height="765" alt="Screenshot (298)" src="https://github.com/user-attachments/assets/3f2f331d-4a19-42d8-b695-c27e85deebef" />

---

## Task 2: Explore What's Pre-installed

+ On the ubuntu-latest runner, run a step that prints:
+ Docker version
   + ```YML
      run: docker --version
     ```
+ Python version
    ```YML
     run: python --version
    ```
+ Node version
   ```YML
     run: node --version
   ```
+ Git version
    ```YML
    run: git --version
    ```
+ Look up the GitHub docs for the full list of pre-installed software on ubuntu-latest
+ Write in your notes: Why does it matter that runners come with tools pre-installed?
    + **Pre-installed tools save setup time, so the workflow starts executing immediately without wasting pipeline minutes on installing basic dependencies every run.**

<img width="1920" height="917" alt="Screenshot (299)" src="https://github.com/user-attachments/assets/db30ca6f-7ff6-4978-92d8-c17ceddf62d4" />


---

## Task 3: Set Up a Self-Hosted Runner
+ Go to your GitHub repo → Settings → Actions → Runners → New self-hosted runner
+ Choose Linux as the OS
+ Follow the instructions to download and configure the runner on:
+ Your local machine, OR
+ A cloud VM (EC2, Utho, or any VPS)
+ Start the runner — verify it shows as Idle in GitHub
+ Verify: Your runner appears in the Runners list with a green dot.


 <img width="1920" height="592" alt="Screenshot (303)" src="https://github.com/user-attachments/assets/690ece95-687e-4143-833c-9f303829b8d2" />

---

## Task 4: Use Your Self-Hosted Runner
+ Create .github/workflows/self-hosted.yml
+ Set runs-on: self-hosted
   + ```YML
     runs-on: self-hosted
     ```
     
+ Add steps that:
+ Print the hostname of the machine (it should be YOUR machine/VM)
   + ```YML
     - name: print the hostname
       run: echo "Hostname:$HOSTNAME"
     ```
     
+ Print the working directory
    + ```YML
      - name: print the working directory
        run: echo " Working directory:$(pwd)"
      ```
+ Create a file and verify it exists on your machine after the run
    + ```YML
      - name: create file
        run: echo "This file was created by the GitHub Actions workflow" > github_actions.txt
     ```
   
+ Trigger it and watch it run on your own hardware
+ Verify: Check your machine — is the file there?
    + ```YML
      - name: Verify file exists
              run: |
                  if [ -f github_actions.txt ]; then
                      echo "File created successfully!"
                  else
                      echo "File creation failed!"
                      exit 1
                  fi
      ```

<img width="1920" height="909" alt="Screenshot (304)" src="https://github.com/user-attachments/assets/f3350bba-33e0-496d-bf8b-b8365459b6a4" />

---

## Task 5: Labels
+ Add a label to your self-hosted runner (e.g., my-linux-runner)
+ Update your workflow to use runs-on: [self-hosted, my-linux-runner]
   ```YML
    runs-on: my-linux-runner
   ```
+ Trigger it — does it still pick up the job?
    + yes 
+ Write in your notes: Why are labels useful when you have multiple self-hosted runners?
    + **labels are usefull when we have multiple selfhosted runner .without lables github cannot identify which runner to use for specific job**
    +  **so basically we lables to tell github to use this specific runner to run the job**
 
<img width="1920" height="518" alt="Screenshot (305)" src="https://github.com/user-attachments/assets/15215b2a-274a-40db-8989-5a0f360c99a2" />

<img width="1920" height="691" alt="Screenshot (306)" src="https://github.com/user-attachments/assets/da309716-c869-48c8-99d2-9f4f473e4f34" />

---
## ### Task 6: GitHub-Hosted vs Self-Hosted
Fill this in your notes:

| | GitHub-Hosted | Self-Hosted |
|---|---|---|
| Who manages it? | github  | user |
| Cost | github pays | pay for instance  |
| Pre-installed tools | yes | no |
| Good for | small and simple project | large and custome project |
| Security concern | more secure  | user is responsible for security |

---





