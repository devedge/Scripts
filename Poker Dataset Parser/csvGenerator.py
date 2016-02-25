 
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

dirPath = ""
csvName = ""
csvFile = ""

# per-game loop method (takes game array)
#   for each game in the array
#   either call the csv saver method in csvGenerator.py to save data row by row
#   or keep a counter of stuff and write to the csv file after

def writeCSV(gameArray):
    global csvFile

    # array of values taken from parserAPI.py and using gameArray
    csvrow =  []

    # append the needed values from gameArray to csvrow if they exist
    # csvrow.append(str())

    csvFile.writerow(csvrow)




def main():
    global dirPath
    global csvName
    global csvFile

    # Get the path to the data folder and the name of the CSV file to write to
    if (sys.version_info[0] >= 3):
        dirPath = eval(input('Enter the absolute path to the folder with the dataset: '))
        csvName = eval(input('Enter a name for the csv file that will be created: '))
    else:
        dirPath = input('Enter the absolute path to the folder with the dataset: ')
        csvName = input('Enter a name for the csv file that will be created: ')

    # check the file location of the csv file
    checkFileLocation(csvName)

    # create the blank csv file

    # open the csv file
    # with open(csvName, 'w', newline='') as csvfile:
    csvFile = csv.writer(open(csvName, "wb"))

    # call the parserAPI.py file that starts parsing
    parserAPI.scanDirectory(dirPath)



def checkFileLocation(csvName):
    print("wat")


main()
