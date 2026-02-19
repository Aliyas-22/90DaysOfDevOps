
# Task 1: Install and Authenticate

  ### Install the GitHub CLI on your machine
  + winget install --id GitHub.cli
    
  ### Authenticate with your GitHub account
   + gh auth login
  ### Verify you're logged in and check which account is active
   + gh auth status
  ###  Answer in your notes: What authentication methods does gh support?
   + GitHub support
      + HTTPS
      + SSH
      + BROWSER-BASED AUTHENTICATION

# Task 2: Working with Repositories

  ### Create a new GitHub repo directly from the terminal — make it public with a README
  + ``` gh repo create learning-repo-gh --public --add-readme --confirm ```
  ###  Clone a repo using gh instead of git clone
  + ``` gh repo clone Aliyas-22/learning-repo-gh ```
  ###  View details of one of your repos from the terminal
  + ``` gh repo view ```
  ###  List all your repositories
  + ``` gh repo list ```
  ###  Open a repo in your browser directly from the terminal
  + ``` gh repo view  learning-repo-gh --web ```
  ###  Delete the test repo you created (be careful!)
  + ``` gh repo delete learning-repo-gh --ye ```
# OUTPUT
<img width="1920" height="1080" alt="Screenshot (161)" src="https://github.com/user-attachments/assets/7bdfec80-dcd4-4cc6-a372-b2cfc2e2e749" />


# Task 3: Issues

###    Create an issue on one of your repos from the terminal — give it a title, body, and a label
  + ``` gh issue create --repo Aliyas-22/practice-cli --title "fix readme format" --body "this readme file needs better structure" --lebel bug ```
###    List all open issues on that repo
  + ``` gh issue list  --repo Aliyas-22/practice-cli ```
###    View a specific issue by its number
 + ``` gh issue view 1 --repo Aliyas-22/practice-cli ```
###    Close an issue from the terminal
 + ``` gh issue close --repo Aliyas-22/practice-cli ```
###    Answer in your notes: How could you use gh issue in a script or automation?
+ we can use the issue in monitoring scripts
+ to track failiure


# Task 4: Pull Requests


###    Create a branch,
+ ``` git checkout -b feature-1 ```
### make a change
+ echo "add new update from feature branch >> Radme.md
+ git add Readme.md
+ git commit -m "added changes to readme from branch feature
### push it
+ git push -u origin feature-1 
### create a pull request entirely from the terminal
+ gh pr create --base main --head feature-1 --title "updated readme feature branch" --body "this pr update the readme fie"
###    List all open PRs on a repo
+ gh pr list
###    View the details of your PR — check its status, reviewers, and checks
+ gh pr view 2
###    Merge your PR from the terminal
+ gh pr merge 2
###    Answer in your notes:
   ###     What merge methods does gh pr merge support?
   + github cli supports ```merge commit``` ```sqaush merge``` an ```rebase merge``` using gh merge pr merge 
   ###     How would you review someone else's PR using gh?
  + gh pr list (to see pr list)
  + gh pr view <id> (to see detials of specid pr )
  + gh pr diff 3 (this will show how many lines are deleted and inserted)
  + gh pr review <id> --commit --body "improve varibale name"


# OUTPUT
<img width="1920" height="985" alt="Screenshot (164)" src="https://github.com/user-attachments/assets/641e5fbc-23f9-4edd-816b-1632a5d952bd" />


<img width="1920" height="983" alt="Screenshot (166)" src="https://github.com/user-attachments/assets/99b5824b-3c29-4cd0-bf69-24f0c9646d1c" />

# Task 5: GitHub Actions & Workflows (Preview)

 ###   List the workflow runs on any public repo that uses GitHub Actions
  + gh run list --repo owner/repo
 ###   View the status of a specific workflow run
 + gh run view <id> --repo owner/repo
###    Answer in your notes: How could gh run and gh workflow be useful in a CI/CD pipeline?
 + gitHub Workflows automate software development process by defining a series of steps
 + (like building and testing code)
 + that run automatically when a specific event (like a code push) occurs.

(Don't worry if you haven't learned GitHub Actions yet — this is a preview for upcoming days)

# Task 6: Useful gh Tricks

## Explore and try these — add the ones you find useful to your git-commands.md:

  ###  gh api — make raw GitHub API calls from the terminal
  + gh api repo/Aliyas-22/ppractice-cli
  ###  gh gist — create and manage GitHub Gists
  + gh gist create file.txt
  ###  gh release — create and manage releases
  + gh release create v1.0.0
 ###   gh alias — create shortcuts for commands you use often
 + gh alias set mypr "list --author @me"
 ###   gh search repos — search GitHub repos from the terminal
 + gh search repos docker



