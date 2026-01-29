## TARGET ##
# TO READ AND WRITE TEXT FILE #

# STEP 1 : create folder 
command : mkdir devops
then do cd to go inside the folder
#
# step 2: create file
command : touch notes.txt
#
# step 3: to write lines inside the notes.txt
command: cat > notes.txt
write 2 lines inside 
(>)= this is redirection used to write input inside the file
#
# step 4: to write more lines inside the file without opening the editor
command: echo "this is what i learn today" >> notes.txt
#
# step 5 : to read file 
command: cat notes.txt
#
# step 6: to see the starting  three lines of file
command : head -3 notes.txt
#
# step 7: to see the last two lines of file
command : tail -2 notes.txt
#
# step 8: want to print the output on screen + save the output in another file 
command: tail -2 notes.txt | tee output.txt
