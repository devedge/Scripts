#!/usr/bin/python

import sys
import csv
import os.path
import parserAPI  
import datafileParser

csvName = ""
csvFile = ""


# Writes the csv file from information gathered from the gameArray
def writeCSV(gameArray):
    global csvFile

    # array of values taken from parserAPI.py and using gameArray
    csvrow =  []


    #### ---- ####
    # This is the part to edit
    # Append the values to the array in the order that the row should look like


    csvrow.append(parserAPI.getGameID(gameArray))


    #### ---- ####


    # Write the row to the csv file
    csvFile.writerow(csvrow)



# The main method
def main(argv):
    
    global csvName
    global csvFile
    overwrite = "n"
    dirPath = ""

    # Get the location of the dataset's directory, and the name of the csv file
    if (len(sys.argv) == 1):
        dirPath = input('Enter the absolute path the dataset folder: ')
        csvName = input('Enter a name for the csv file: ')

    elif (len(sys.argv) == 3):
        dirPath = sys.argv[1]
        csvName = sys.argv[2]

    elif (len(sys.argv) == 4):
        dirPath = sys.argv[1]
        csvName = sys.argv[2]
        overwrite = sys.argv[3]

    elif (sys.argv[1].lower() == "help"):
        print("Usage: ")
        print("$ python csvGenerator.py")
        print("or")
        print("$ python csvGenerator.py /absolute/path/to/folder output.csv y")
        print("where 'y' (yes) is optional, and overwrites the previous file")
        exit(0)

    else:
        print("Usage: ")
        print("$ python csvGenerator.py")
        print("or")
        print("$ python csvGenerator.py /absolute/path/to/folder output.csv y")
        print("where 'y' (yes) is optional, and overwrites the previous file")
        exit(0)


    # check the file location of the csv file
    checkFileLocation(overwrite)

    # open the csv file
    csvFile = csv.writer(open(csvName, "w"))

    print("Working...")

    # Call the method that scans the entire directory of data files
    scanDirectory(dirPath)

    print("Done")


# Scan every text file in the path and its subfolders
def scanDirectory(path):
    for (root, dirs, files) in os.walk(path):
            for name in files:
                if name.endswith((".txt")):

                    # Parse the file to get the list of games
                    gamesList = datafileParser.parseFile(os.path.join(root, name))

                    # For every game in the array, call the function that writes
                    # the csv file
                    for x in range(0, len(gamesList)):
                        writeCSV(gamesList[x])


# Check if the file exists, and overwrite it if the user wants to
def checkFileLocation(overwrite):
    global csvName

    if (os.path.exists(csvName) and (overwrite != "y")):
        if (input("The file already exists. Overwrite it? (y/n): ") == "n"):
            csvName = input("Enter a new filename: ")


# The program start point
main(sys.argv[1:])
