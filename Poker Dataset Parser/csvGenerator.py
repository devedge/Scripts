 
# ask for a directory to scan (recursive?)

# pass the directory to parserAPI.py

# in parserAPI.py, after each file parsed, 
#   call a method here for storing the array results in a csv file

# the method here for creating the csv file can call helper methods
#   from parserAPI.py to get relevant data


# all that has to be changed here is how the data will explicitly be
#   saved in the csv file

import sys
import csv
import os.path
import parserAPI  
import datafileParser

# from parserAPI import *

dirPath = ""
csvName = ""
csvFile = ""
numiter = 0

# per-game loop method (takes game array)
#   for each game in the array
#   either call the csv saver method in csvGenerator.py to save data row by row
#   or keep a counter of stuff and write to the csv file after

def writeCSV(gameArray):
    global csvFile
    global numiter

    numiter += 1

    # array of values taken from parserAPI.py and using gameArray
    csvrow =  []


    #### ---- ####
    # Append the values to the array in the order that the row should look like

    csvrow.append(parserAPI.getGameID(gameArray))


    #### ---- ####


    # Write the row to the csv file
    csvFile.writerow(csvrow)



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


# The starting point of the program
def main():
    
    global dirPath
    global csvName
    global csvFile

    # Get the path to the data folder and the name of the CSV file to write to
    if (sys.version_info[0] >= 3):
        dirPath = input('Enter the absolute path to the folder with the dataset: ')
        csvName = input('Enter a name for the csv file that will be created: ')
    else:
        dirPath = eval(input('Enter the absolute path to the folder with the dataset: '))
        csvName = eval(input('Enter a name for the csv file that will be created: '))

    # check the file location of the csv file
    # checkFileLocation(csvName)

    # create the blank csv file

    # open the csv file
    # with open(csvName, 'w', newline='') as csvfile:
    csvFile = csv.writer(open(csvName, "w"))

    # call the parserAPI.py file that starts parsing
    scanDirectory(dirPath) #parserAPI.

    print(numiter)



def checkFileLocation(csvName):
    print("wat")




main()
