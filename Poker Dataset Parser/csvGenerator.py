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

    # Initialize the gameArray in parserAPI
    parserAPI.initGameArray(gameArray)

    # array of values taken from parserAPI.py using the gameArray
    csvrow =  []


    #### ---- ####
    # This is the part to edit
    # Append the values to the array in the order that the row should look like

        

    

    # EXAMPLES
    # Uncomment to use

    # For all the games that are won, store the game ID, the user ID, 
    #       the amount won, the cards they played, the cards on the table,
    #       and the 'action, value' for each move they made during the game.

    # There can be multiple winners in a game. However, there is never more than
    # one loser or one player who collects the pot. 

    # Some games have winners and losers, other games have only winners or 
    # only losers, and some games have a player who collects the pot

    # if (parserAPI.isGameWon()):
    #       # if multiple winners
    #     csvrow.append(parserAPI.getGameID())
    #     csvrow.append(parserAPI.getWinnerID())

    #     csvFile.writerow(csvrow)




    # For every game that is lost, store the user ID, the cards they played, and
    #       the cards on the table

    if (parserAPI.isGameLost()):
        csvrow.append(parserAPI.getGameID())
        csvrow.append(parserAPI.getDate())
        csvFile.writerow(csvrow)




    # For each game, store the game ID, date, if the game was won, what the total pot was


    #### ---- ####
    



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
        print("$ python csvGenerator.py /absolute/path/to/dataset/folder output.csv y")
        print("where 'y' (yes) is optional, and overwrites the previous CSV file")
        exit(0)

    else:
        print("Usage: ")
        print("$ python csvGenerator.py")
        print("or")
        print("$ python csvGenerator.py /absolute/path/to/dataset/folder output.csv y")
        print("where 'y' (yes) is optional, and overwrites the previous CSV file")
        exit(0)


    # check the file location of the csv file
    checkFileLocation(overwrite)

    # Remove the old error log 
    if (os.path.exists("errorlog.txt")):
        os.remove("errorlog.txt")

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

                    # If the user decides to continue the script after an exception has occurred,
                    # don't save any games from the file where the error happened
                    if (gamesList != "NULL"):
                        # For every game in the array, call the function that writes
                        # the csv file
                        for x in range(0, len(gamesList)):
                            writeCSV(gamesList[x])


# Check if the file exists, and overwrite it if the user wants to
def checkFileLocation(overwrite):
    global csvName

    if (os.path.exists(csvName) and (overwrite.lower() != "y")):
        if (input("The file already exists. Overwrite it? (y/n): ") == "n"):
            csvName = input("Enter a new filename: ")


# The program start point
main(sys.argv[1:])
