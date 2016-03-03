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


    #### ---- ####  Edit this part so the values are appended to the array as a row

    # For all the games that were won
    if (parserAPI.isGameWon()):

        # Game ID and number players
        csvrow.append(parserAPI.getGameID())
        csvrow.append(parserAPI.getNumberPlayers())

        wpidx = parserAPI.getWinningPlayerIndex()

        # append the action count of the winner
        winnerActionArray = parserAPI.getUserActionCount(wpidx)
        csvrow.append(winnerActionArray[0])
        csvrow.append(winnerActionArray[1])
        csvrow.append(winnerActionArray[2])
        csvrow.append(winnerActionArray[3])
        csvrow.append(winnerActionArray[4])
        csvrow.append(winnerActionArray[5])
        csvrow.append(winnerActionArray[6])
        csvrow.append(winnerActionArray[7])
        csvrow.append(winnerActionArray[8])

        otherActionArray = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # append the action count of all the other players summed up
        for x in range(0, parserAPI.getNumberPlayers()):
            
            # For all the players who are not winners
            if ((x + 1) != wpidx):

                tempuserarray = parserAPI.getUserActionCount(x + 1)

                otherActionArray[0] += tempuserarray[0]
                otherActionArray[1] += tempuserarray[1]
                otherActionArray[2] += tempuserarray[2]
                otherActionArray[3] += tempuserarray[3]
                otherActionArray[4] += tempuserarray[4]
                otherActionArray[5] += tempuserarray[5]
                otherActionArray[6] += tempuserarray[6]
                otherActionArray[7] += tempuserarray[7]
                otherActionArray[8] += tempuserarray[8]


        csvrow.append(otherActionArray[0])
        csvrow.append(otherActionArray[1])
        csvrow.append(otherActionArray[2])
        csvrow.append(otherActionArray[3])
        csvrow.append(otherActionArray[4])
        csvrow.append(otherActionArray[5])
        csvrow.append(otherActionArray[6])
        csvrow.append(otherActionArray[7])
        csvrow.append(otherActionArray[8])


        csvFile.writerow(csvrow)


        # winningPlayerIDx = parserAPI.getWinningPlayerIndex()
        # csvrow.append(parserAPI.getGameID())
        # csvrow.append(parserAPI.getPlayerChipsAmount(winningPlayerIDx))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 1, 1))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 2, 1))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 3, 1))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 4, 1))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 5, 1))
        # csvrow.append(parserAPI.getOnePlayerAction(winningPlayerIDx, 6, 1))
        # csvrow.append(parserAPI.getWinningPlayerAmount())
        # csvrow.append(parserAPI.getWinningCardsOnTable(1))
        # csvrow.append(parserAPI.getWinningCardsOnTable(2))
        # csvrow.append(parserAPI.getWinningCardsOnTable(3))
        # csvrow.append(parserAPI.getWinningCardsOnTable(4))
        # csvrow.append(parserAPI.getWinningCardsOnTable(5))
        # csvFile.writerow(csvrow)




    # EXAMPLES
    # Uncomment to use

    # For all the games that are won, store the game ID, the user ID, 
    #       the amount won, and the cards on the table.
    # There can be multiple winners in a game. However, there is never more than
    # one loser or one player who collects the pot. 
    # Some games have winners and losers, other games have only winners or 
    # only losers, and some games have a player who collects the pot

    # if (parserAPI.isGameWon()):
    #     csvrow.append(parserAPI.getGameID())

    #     # get just the first winner for simplicity, since there can be two.
    #     # If we wanted both, we can use a for loop to iterate over both
    #     csvrow.append(parserAPI.getPlayerID(parserAPI.getWinningPlayerIndex())) 
        
    #     # Get the amount won
        
    #     # gets the cards that were on the table for the first player

    #     # Write the row
    #     csvFile.writerow(csvrow)




    # For every game that is lost, store the user ID, the cards they played, and
    #       the cards on the table

    # if (parserAPI.isGameLost()):
    #     csvrow.append(parserAPI.getPlayerID(parserAPI.getLosingPlayerIndex()))
    #     csvrow.append(parserAPI.getLosingHand(1))
    #     csvrow.append(parserAPI.getLosingHand(2))
    #     csvrow.append(parserAPI.getLosingCardsOnTable(1))
    #     csvrow.append(parserAPI.getLosingCardsOnTable(2))
    #     csvrow.append(parserAPI.getLosingCardsOnTable(3))
    #     csvrow.append(parserAPI.getLosingCardsOnTable(4))
    #     csvrow.append(parserAPI.getLosingCardsOnTable(5))
    #     csvFile.writerow(csvrow)


    # For each game, store the game ID, date, if the game was won, what the total pot was
    # csvrow.append(parserAPI.getGameID())
    # csvrow.append(parserAPI.getDate())
    # csvrow.append(parserAPI.isGameWon())
    # csvrow.append(parserAPI.getTotalPot())


    #### ---- ####

    # Notes:
    # depending on the number of actions during a game, what are the relations between each other?
    # seperate winner and other
    # keep a count of players
    # 9 columns for winner actions, 9 more columns for other users, add game id, add number of players
    # 
    


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

    # Insert a header
    csvFile.writerow([
                        "Game ID", 
                        "# Players", 
                        "W Calls", "W Bets", "W Raises", "W All-In", "W Shows", "W Check", "W Fold", "W Muck", "W Sitout", 
                        "O Calls", "O Bets", "O Raises", "O All-In", "O Shows", "O Check", "O Fold", "O Muck", "O Sitout"
                    ])

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
