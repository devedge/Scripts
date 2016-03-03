
# Array indices, declared globally
# Main gameArray indices
gameIDIndex = 0
dateIndex = 1
timeIndex = 2
numRoundsIndex = 3
boardCardsIndex = 4
totalPotIndex = 5
numPlayersIndex = 6
dealerIndex = 7
smallBlindIndex = 8
bigBlindIndex = 9
gameWonIndex = 10
gameLostIndex = 11
firstUserIndex = 12

# Winner/collected indices
winnerPresentIndex = 0
collectorPresentIndex = 1
numWinnersIndex = 2
idxWinnersIndex = 3
moneyRecievedIndex = 4
winningHandIndex = 5

# Loser indices
loserPresentIndex = 0
indexOfLoserIndex = 1
losingHandIndex = 2

# Cards played indices
cardHandPlayedIndex = 0
cardHandTableIndex = 1
cardHandDescriptIndex = 2

# User indices
userIDIndex = 0
userChipsAmount = 1
userPreGameIndex = 2
userPocketCardsIndex = 3
userFlopIndex = 4
userTurnIndex = 5
userRiverIndex = 6
userShowdownIndex = 7

gameArray = []

# The gameArray is initialized here to simplify extracting values
def initGameArray(gameArrayInput):
    global gameArray

    gameArray = []
    gameArray = gameArrayInput


# Returns an int
def getGameID():
    return int(gameArray[gameIDIndex])

# Returns a string
def getDate():
    return gameArray[dateIndex]

# Returns a string
def getTime():
    return gameArray[timeIndex]

# Returns an int
def getTotalPot():
    return gameArray[totalPotIndex]

# Returns a boolean
def isGameWon():
    return bool(gameArray[gameWonIndex][winnerPresentIndex])

# Returns a boolean
def isGameCollected():
    return bool(gameArray[gameWonIndex][collectorPresentIndex])

# Returns a boolean
def isGameLost():
    return bool(gameArray[gameLostIndex][loserPresentIndex])

# Returns a boolean true if the dealer is dead
def isDealerDead():
    return bool(int(gameArray[dealerIndex]) == 0)

# Returns true if the Board cards are displayed
def isBoardCardsDisplayed():
    return bool(len(boardCardsIndex) != 0)

def getBoardCards():
    return gameArray[boardCardsIndex]

def getNumberRounds():
    return gameArray[numRoundsIndex]






#### ---- #### General Player information

# Gets the number of players in the current game (int)
def getNumberPlayers():
    return gameArray[numPlayersIndex]

# Get the player ID (string)
def getPlayerID(playerIndex = 1):
    return gameArray[firstUserIndex - 1 + playerIndex][userIDIndex]

# Get the player's dollar amount in chips (float)
def getPlayerChipsAmount(playerIndex = 1):
    return float(gameArray[firstUserIndex - 1 + playerIndex][userChipsAmount])

# Gets the player action at a certain play in the game. Will return the 
# first action by default. The number of actions a player has taken can 
# be found with the method below this one.

# The plays are numbered in this order:
#   1   Pre-game actions
#   2   Pocket Cards
#   3   Flop
#   4   Turn
#   5   River
#   6   Showdown
def getOnePlayerAction(playerIndex = 1, play = 1, action = 1):
    return gameArray[firstUserIndex - 1 + playerIndex][userPreGameIndex + play - 1][action - 1][0]

# A user can take multiple actions during a play, so this returns the number 
# of actions he has taken
def getNumActions(playerIndex = 1, play = 1):

    if (gameArray[firstUserIndex - 1 + playerIndex][userPreGameIndex + play - 1][0][0] == "NA"):
        return 0
    else:
        return len(gameArray[firstUserIndex - 1 + playerIndex][userPreGameIndex + play - 1])

# Returns an array of all the player actions during a play (which is usually 1, but
# occasionally 2)
def getAllPlayerActions(playerIndex = 1, play = 1):
    array = []

    for x in range(0, getNumActions(playerIndex, play)):
        array.append(gameArray[firstUserIndex - 1 + playerIndex][userPreGameIndex + play - 1][x][0])
    
    return array



# Get a count of the actions of a player over the course of a game
def getUserActionCount(playerIndex = 1):

    # The values are: [calls, bets, raises, all-in, shows, check, fold, muck, sitout]
    actionCount = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # for every play
    for x in range(0,6):
        
        # for every action (usually 1, but occasionally 2)
        for y in range(0, getNumActions(playerIndex, (x + 1))):

            action = getOnePlayerAction(playerIndex, (x + 1), (y + 1) )

            if (action.lower() == "calls"):
                actionCount[0] += 1
            elif (action.lower() == "bets"):
                actionCount[1] += 1
            elif (action.lower() == "raises"):
                actionCount[2] += 1
            elif ((action.lower() == "all-in") or (action.lower() == "all-in(raise)")): # or all-in (raises)
                actionCount[3] += 1
            elif (action.lower() == "shows"):
                actionCount[4] += 1
            elif (action.lower() == "checks"):
                actionCount[5] += 1
            elif (action.lower() == "folds"):
                actionCount[6] += 1
            elif (action.lower() == "mucks"):
                actionCount[7] += 1
            elif (action.lower() == "sitout"):
                actionCount[8] += 1


    return actionCount




#### ---- #### Winning Player information

# Get the number of winning players (int)
# There are occasionally two winners in a game
def getNumberWinners():
    return int(gameArray[gameWonIndex][numWinnersIndex])


# Get the index of the winning player. Use this with the methods above this section.
# eg., Get the winning player's ID: getPlayerID(getWinningPlayerIndex(1))
# The winnerIndex is usually 1, unless there are several winners such that the second winner is 2, etc...
def getWinningPlayerIndex(winnerIndex = 1):
    return gameArray[gameWonIndex][idxWinnersIndex][winnerIndex - 1]


# Get the money won, from the winnerIndex (which is 1 for the first winner)
def getWinningPlayerAmount(winnerIndex = 1):
    return gameArray[gameWonIndex][moneyRecievedIndex][winnerIndex - 1]


# Returns an array of two values (the winning hand)
def getWinningHand(cardIDX = 0, winnerIndex = 1):

    if (cardIDX == 0):
        return gameArray[gameWonIndex][winningHandIndex][cardHandPlayedIndex][winnerIndex - 1]
    else:
        return gameArray[gameWonIndex][winningHandIndex][cardHandPlayedIndex][winnerIndex - 1][cardIDX - 1]


# Returns a 5-value array of the cards on the table if no card is specified
# Otherwise, return the specific card at the cardIDX, which goes from 1 to 5
def getWinningCardsOnTable(cardIDX = 0, winnerIndex = 1):

    if (cardIDX == 0):
        return gameArray[gameWonIndex][winningHandIndex][cardHandTableIndex][winnerIndex - 1]
    else:
        return gameArray[gameWonIndex][winningHandIndex][cardHandTableIndex][winnerIndex - 1][cardIDX - 1].replace(":", "").replace("B", "").replace("P", "")


# Return the winning hand description
def getWinningHandDescription(winnerIndex = 1):
    return gameArray[gameWonIndex][winningHandIndex][cardHandDescriptIndex][winnerIndex - 1]





#### ---- #### Losing Player information

def getLosingPlayerIndex():
    return gameArray[gameLostIndex][indexOfLoserIndex]


# Returns an array of two values if no card specified, or returns the
# specific card at the cardIDX, which goes from 1 to 2
def getLosingHand(cardIDX = 0):

    if (cardIDX == 0):
        return gameArray[gameLostIndex][losingHandIndex][cardHandPlayedIndex]
    else:
        return gameArray[gameLostIndex][losingHandIndex][cardHandPlayedIndex][cardIDX - 1]


# Returns a 5-value array of the cards on the table if no card is specified
# Otherwise, return the specific card at the cardIDX, which goes from 1 to 5
def getLosingCardsOnTable(cardIDX = 0):

    if (cardIDX == 0):
        return gameArray[gameWonIndex][losingHandIndex][cardHandTableIndex]
    else:
        return gameArray[gameWonIndex][losingHandIndex][cardHandTableIndex][cardIDX - 1].replace(":", "").replace("B", "").replace("P", "")


# Returns the losing hand description
def getLosingHandDescription():
    return gameArray[gameWonIndex][losingHandIndex][cardHandDescriptIndex]


