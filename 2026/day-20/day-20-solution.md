# Day 20 – Bash Scripting Challenge: Log Analyzer and Report Generator
## ask 1: Input and Validation
Your script should:

Accept the path to a log file as a command-line argument
Exit with a clear error message if no argument is provided
Exit with a clear error message if the file doesn't exist

 ```
1)create file vim log_analyzer.sh
2)give the arrgument that will accpet the command line argument #$1
code:-
if [ $# -ne 1 ]; then
    echo "Usage: $0 <path_of_log_file>"
    exit 1
fi

log_path="$1"

if [ ! -f "$log_path" ]; then
    echo "Error: Log file not found!"
    exit 1
fi
```
## output
<img width="1920" height="199" alt="Screenshot (117)" src="https://github.com/user-attachments/assets/c09fc7ed-aebb-45e0-b17f-93e1c7635994" />

## Task 2: Error Count
Count the total number of lines containing the keyword ERROR or Failed
Print the total error count to the console
```
1)before doing the task two i created sample_log.log file
2)use the cammand grep and -c -i -o -E -n
-i Case insensitive search
-n  Displays line number with matched line
-c  Counts number of matching lines
-o  Prints only the matched word
-E Enables extended regex (for multiple patterns)
3) and learn about new tools like
-grep = filters only error lines
-awk  =removes timestamp
-sort  =groups identical messages together
-uniq -c = counts duplicates
-sort -nr =highest count first
code:-
total_errors=$(grep -ci "ERROR" "$log_path")
total_lines=$(wc -l < "$log_path")
```
## output 
<img width="1920" height="198" alt="Screenshot (118)" src="https://github.com/user-attachments/assets/1b6ceae8-e661-45ed-9748-39d5002ce249" />


## Task 3: Critical Events
Search for lines containing the keyword CRITICAL
Print those lines along with their line number

```
1)using sed 's/^/Line / this in the code proper prefix word line 
code:-
critical_events=$("grep -n "ALERT" "$log_path" | sed 's/^/Line /')
```
## output

<img width="1920" height="646" alt="Screenshot (119)" src="https://github.com/user-attachments/assets/e2d1266a-1957-4c43-a3dc-0124e564f1e7" />

## Task 4: Top Error Messages
Extract all lines containing ERROR
Identify the top 5 most common error messages
Display them with their occurrence count, sorted in descending order
```
code:-
top_errors=$(grep -iE "ERROR|Failed" "$log_path" | awk '{$1=$2=$3=""; print $0}'| sort | uniq -c | sort -rn | head -5)
```

## Task 5: Summary Report
Generate a summary report to a text file named log_report_<date>.txt (e.g., log_report_2026-02-11.txt). The report should include:

Date of analysis
Log file name
Total lines processed
Total error count
Top 5 error messages with their occurrence count
List of critical events with line numbers
```
1)by using tee transforing the output
created file with timestamp $(date +%F_%H-%M-%S)
code :-
today=$(date +%F_%H-%M-%S)
report_file="log_report_${today}.txt"


echo "==================== LOG SUMMARY REPORT ===================="
echo "Date of Analysis : $today"
echo "Log File         : $log_path"
echo "Total Lines      : $total_lines"
echo "Total ERROR Lines: $total_errors"
echo ""

echo "================== TOP 5 ERROR MESSAGES ================="
echo "$top_errors"
echo ""

echo "================== CRITICAL EVENTSS ================="
echo "$critical_events"
echo "=============================================================="
} | tee "$report_file"
```
## output 

<img width="1920" height="606" alt="Screenshot (120)" src="https://github.com/user-attachments/assets/5cbdfab6-21c8-4c89-a173-2700c551707b" />


# WHAT I LEARNED 
+ Learned how to read and analyze log files using Linux commands.
+ Learned how to use the grep command to search specific keywords inside a log file.
+ Learned different grep options: -o, -n,-i,-E,-c
+ Learned how to search multiple error
+ understood how log analysis works in real systems...
