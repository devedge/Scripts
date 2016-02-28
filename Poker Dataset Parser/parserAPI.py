
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

gameArray = []

# a dead dealer will have a value of 0
# should initialize the gamearray here once, and provide a method to wipe it after use

def initGameArray(gameArrayInput):
    global gameArray
    gameArray = gameArrayInput


# get id
# Returns an int
def getGameID():
    return int(gameArray[gameIDIndex])

# get date
# Returns a string
def getDate():
    return gameArray[dateIndex]

# get time
# Returns a string
def getTime():
    return gameArray[timeIndex]

# Returns a boolean
def isGameWon():
    return bool(gameArray[10][0])

# 
def isDealerDead():
    return bool(int(gameArray[dealerIndex]) == 0)


# 
# returns the first user if no user number is specified
# Returns a string
def getUserID(numUser = 1):
    return gameArray[firstUserIndex - 1 + numUser][0]

# instead of getting just a winner ID, what if we got the entire winner array?



# get number of user actions per round (returns an int)



# Gets the winner of a game (should include a check that fails if the game wasn't won?)
# Returns a string
def getWinnerID():
    return gameArray[12 + int(gameArray[12])][1]

def getWinnerMoney():
    return gameArray[12]


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



                    









