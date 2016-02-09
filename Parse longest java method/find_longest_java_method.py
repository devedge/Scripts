#!/usr/bin/env python

import os
import re

# This script parses all of the java files in a directory and its subdirectories
# to find the longest method

# Currently, you specify an absolute directory path, and the last result printed
# to the console contains the longest method (this may be refined in the future)

fileCount = 0
maxLineCount = 0
longestFileName = ""

# Main method
# This prompts for a directory location, and returns the absolute pathname,
# length of the longest method, and number of files searched
def main():

    global fileCount
    global maxLineCount
    global longestFileName

    path = input("Enter the absolute path to the folder: ")

    print "Searching..."
    print " "

    # Iterate over the current directory and all of its subdirectories
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".java")):

                # goto parse method
                parse_java_longest_method(os.path.join(root, name))
                fileCount += 1


    print "File with longest method: " + str(longestFileName)
    print "             with length: " + str(maxLineCount)
    print " "
    print "Number of files searched: " + str(fileCount)



# parse a java file to find the longest method
def parse_java_longest_method(name):
    
    pattern = "((public|private|protected|static|final|native|synchronized|abstract|transient)+\s)+[\$_\w\.\<\>\[\]]*\s+[\$_\w\.]+\([^\)]*\)?\s*\{?[^\}]*\}?"

    global maxLineCount
    global longestFileName

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
                    
                method = False

            currentLineCount += 1


# Program start
main()
