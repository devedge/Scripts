
# import os
# import datafileParser
# import csvGenerator

gameIDIndex = 0
dateIndex = 1
timeIndex = 2
numRoundsIndex = 3
boardCardsIndex = 4
totalPotIndex = 5
numPlayersIndex = 6
dealerIndex = 7
smallBindIndex = 8
bigBindIndex = 9
gameWonIndex = 10
gameLostIndex = 11
firstUserIndex = 12


# class parserAPI:
# indices in the gameArray

# def __init__():
#     print("parserAPI init")


# a dead dealer will have a value of 0
# should initialize the gamearray here once, and provide a method to wipe it after use


# for each file in the directory
#   call datafileParser.py to parse it
#   get the games list array that is returned
#   call the per-game loop method in csvGenerator.py
# def scanDirectory(path):

#     # Scan every text file in the path and its subfolders
#     for (root, dirs, files) in os.walk(path):
#             for name in files:
#                 if name.endswith((".txt")):

#                     # Parse the file to get the list of games
#                     gamesList = datafileParser.parseFile(os.path.join(root, name))
#                     arraySize = len(gamesList)

#                     # For every game in the array, call the function that writes
#                     # the csv file
#                     for x in range(0, arraySize):
#                         csvGenerator.writeCSV(gamesList[x])



# dont need
# def getGame(gameIDX):
    # return 4 # gameList[gameIDX - 1]

# get id
# Returns an int
def getGameID(gameArray):
    return int(gameArray[gameIDIndex])

# get date
# Returns a string
def getDate(gameArray):
    return gameArray[dateIndex]

# get time
# Returns a string
def getTime(gameArray):
    return gameArray[timeIndex]

# Returns a boolean
def gameWon(gameArray):
    return bool(gameArray[10][0])

# 
def isDealerDead(gameArray):
    return bool(int(gameArray[dealerIndex]) == 0)


# 
# returns the first user if no user number is specified
# Returns a string
def getUserID(gameArray, numUser = 1):
    return gameArray[firstUserIndex - 1 + numUser][0]

# instead of getting just a winner ID, what if we got the entire winner array?

# Gets the winner of a game (should include a check that fails if the game wasn't won?)
# Returns a string
def getWinnerID(gameArray):
    return gameArray[12 + int(gameArray[12])][1]


# method that checks if there are cards on the board
# to use, have an if statement like:
# if boardCardsDisplayed():
#     save the cards on the board
#     else dont do anything to save, and skip to the next step



# print(example1)




# to access everything played by round:
#                13                6
# for x in range(playerarraystart, getNumPlayers()):
#    do something to each player


def getPlayerAction(playerID, playNumber):
    print("asdf")
    # if check return check
    # if bet return bet and amount
    # if call return call and amount
    # if raise return raise and [from amount, to amount]
    # if fold return fold
    # if muck return muck



                    









