#!/usr/bin/env python

import os
import re

# This script parses all of the java files in a directory and its subdirectories
# to find the longest method

# To use, run "python find_longest_java_method.py" and specify an absolute path to 
# a folder to search. The Java file that contains the longest method will have its 
# full path printed out to the console, along with the number of lines it spans, 
# and the number of Java files that were searched.


fileCount = 0
maxLineCount = 0
methodLineStart = 0
longestFileName = ""

# Main method
# This prompts for a directory location, and returns the absolute pathname,
# length of the longest method, and number of files searched
def main():

    global fileCount
    global maxLineCount
    global longestFileName
    global methodLineStart

    path = input("Enter the absolute path to the folder: ")

    print("Searching...")
    print(" ")

    # Iterate over the current directory and all of its subdirectories
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".java")):

                # goto parse method
                parse_java_longest_method(os.path.join(root, name))
                fileCount += 1


    print("File with longest method: ")
    print(str(longestFileName))
    print(" ")
    print("Method starts at line " + str(methodLineStart) + " and has a length of " + str(maxLineCount) + " lines")
    print(" ")
    print("Number of files searched: " + str(fileCount))



# parse a java file to find the longest method
def parse_java_longest_method(name):
    
    # REGEX pattern to find a Java method declaration
    pattern = "((public|private|protected|static|final|native|synchronized|abstract|transient)+\s)+[\$_\w\.\<\>\[\]]*\s+[\$_\w\.]+\([^\)]*\)?\s*\{?[^\}]*\}?"

    global maxLineCount
    global longestFileName
    global methodLineStart

    currentLineStart = 0
    currentLineCount = 0
    nestedLevel = 0
    method = False

    # open the file and iterate over each line
    with open(name, 'r') as f:
        for line in f:

            # search for method declaration
            if (re.search(pattern, line)):
                method = True
                currentLineStart = currentLineCount

            # search for any open brackets
            elif (re.search("{", line) and method):
                nestedLevel += 1

            # search for any closed brackets
            elif (re.search("}", line) and (nestedLevel > 0) and method):
                nestedLevel -= 1

            # search for end of method
            elif (re.search("}", line) and (nestedLevel == 0) and method):

                # check if this method is the current longest
                if ( (currentLineCount - currentLineStart) > maxLineCount):
                    maxLineCount = currentLineCount - currentLineStart
                    longestFileName = name
                    methodLineStart = currentLineStart
                    
                method = False

            currentLineCount += 1


# Program start
main()
