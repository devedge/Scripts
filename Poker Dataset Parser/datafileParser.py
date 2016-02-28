import re
import traceback

# the data file is parsed line by line
# as each line is being processed, variables keep track of where in the file the 
#       current line is.

# player numbers are assigned in the order they appear
# their IDs and number are stored in two different arrays for temporary indexing reference


# General global variables
firstGame = True
arrayListUpdated = False
currentSector = "init"
dealerSeat = 0
tempPlayerArray = []
tempPlayerIndex = []
gamesList = []
gameArray = []
playerArrayInstance = []
skipGame = False
failInfo = []
lineNumber = 0
filename = ""


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

# Loser indices
loserPresentIndex = 0
indexOfLoserIndex = 1
losingHandIndex = 2

# Cards played indices
lHCardsPlayedIndex = 0
lHCardsTableIndex = 1
lHCardDescriptIndex = 2

# User indices
userIDIndex = 0
userChipsAmount = 1
userPreGameIndex = 2
userPocketCardsIndex = 3
userFlopIndex = 4
userTurnIndex = 5
userRiverIndex = 6
userShowdownIndex = 7



# Initializes a blank gameArray
def initGameArray():
    global gameArray

    gameArray = [
                    0,              # 0  game ID
                    "NULL",         # 1  date
                    "NULL",         # 2  time and timezone
                    0,              # 3  number of rounds
                    [],             # 4  cards on board
                    0.0,            # 5  total pot amount
                    0,              # 6  num players
                    0,              # 7  dealer player
                    0,              # 8  small blind player
                    0,              # 9  big blind player
                    [
                        False,      #  game won              # 10  win info
                        False,      #  only collected
                        0,          #  number of winners
                        [],         #  index of winners
                        [],         #  money received (for each winner, can be appended)
                        [           #  winning/collected hand
                            ["NA"],  # cards played (usually two)
                            ["NA"],  # cards on table (usually five)
                            ""       # card description
                        ]  
                    ],
                    [
                        False,      #  is there a loser      # 11  lost info
                        0,          #  index of loser
                        [           #  losing hand
                            ["NA"],  # cards played (usually two)
                            ["NA"],  # cards on table (usually five)
                            ""       # card description
                        ]          
                    ]
                ]

# Initializes a blank player array
def initPlayerInstance():
    global playerArrayInstance

    playerArrayInstance =   [
                                "NULL",     # player ID
                                0.0,        # dollars in chips
                                [["NA"]],   # user actions before the game starts (usually empty, other than small/big blind, antes, or sitout)
                                [["NA"]],   # user actions during the pocket cards
                                [["NA"]],   # user actions during the flop
                                [["NA"]],   # user actions during the turn
                                [["NA"]],   # user actions during the river
                                [["NA"]]    # user actions during the showdown
                            ]


# Parses a file with a list of poker games and returns a list of all of the games, 
# represented as arrays
def parseFile(datafile):

    global firstGame
    global arrayListUpdated
    global tempPlayerArray
    global tempPlayerIndex
    global dealerSeat
    global currentSector
    global gamesList
    global failInfo
    global lineNumber
    global filename

    filename = datafile

    gamesList = []
    initGameArray()
    initPlayerInstance()

    lineNumber = 0 # for debugging purposes
    skipGame = False
    failInfo = []

    with open(datafile, 'r') as f:

        # If an unexpected error happens, fail and print out information
        try:

            # Parse the file line by line
            for line in f:
                lineNumber += 1

                # This is the first line of a game, so reset all of the per-game variables.
                # Then, extract the gameID, date, and time & timezone. 
                if (re.search("Stage", line)):
                   
                    # reset all the per-game variables
                    tempPlayerArray = []
                    tempPlayerIndex = []
                    initPlayerInstance()
                    initGameArray()
                    
                    arrayListUpdated = False
                    currentSector = "init"
                    dealerSeat = 0

                    skipGame = False

                    # Begin to parse the first line
                    line = line.split()
                    dashIndex = line.index("-")
                    
                    gameArray[gameIDIndex] = int(line[1].replace("#", "").replace(":", ""))   # insert game ID
                    gameArray[dateIndex] = line[dashIndex + 1]                              # insert date  (7)
                    gameArray[timeIndex] = (line[dashIndex + 2] + line[dashIndex + 3])      # insert time and timezone (8 & 9)
                

                # This is the second line of a new game, so extract and
                # save the dealer seat number from the line.
                elif (re.search("Table", line) and not skipGame):
                    line = line.split()

                     # Get the dealer seat number from the value that comes after the word "Seat"
                    dealerSeat = int(line[line.index("Seat") + 1].replace("#", "")) 


                # Update the current sector the script is in as it progresses through the game
                elif (re.search("\*\*\* POCKET CARDS \*\*\*", line) and not skipGame):
                    currentSector = "pocketCards"
                    gameArray[numRoundsIndex] += 1
                
                elif (re.search("\*\*\* FLOP \*\*\*", line) and not skipGame):
                    currentSector = "flop"
                    gameArray[numRoundsIndex] += 1
                
                elif (re.search("\*\*\* TURN \*\*\*", line) and not skipGame):
                    currentSector = "turn"
                    gameArray[numRoundsIndex] += 1

                elif (re.search("\*\*\* RIVER \*\*\*", line) and not skipGame):
                    currentSector = "river"
                    gameArray[numRoundsIndex] += 1

                elif (re.search("\*\*\* SHOW DOWN \*\*\*", line) and not skipGame):
                    currentSector = "showdown"
                    gameArray[numRoundsIndex] += 1

                elif (re.search("\*\*\* SUMMARY \*\*\*", line) and not skipGame):
                    currentSector = "summary"


                # Depending on the current sector the loop is in, parse the user actions and 
                # populate the gameArray
                elif(not skipGame):
                    # Is the current line empty?
                    lineNotEmpty = bool(len(line.split()) != 0)

                    # If this is the "init" sector, first grab the seat initializations, then
                    # grab the blind posts.
                    # Get the information from the lines following the 'Stage' and 'Table' declarations
                    if ((currentSector == "init") and lineNotEmpty): 
                        splitline = line.split()

                        # Extract the seat assignments, user IDs, and dollar amount in chips per
                        # user
                        if (re.search("\ASeat", line)):

                            # append an initialized playerArrayInstance to the gameArray
                            initPlayerInstance()
                            gameArray.append(playerArrayInstance)

                            # Set up temporary arrays that are used to find out what order players were declared
                            tempPlayerArray.append(splitline[3])
                            tempPlayerIndex.append(int(splitline[1]))
                            
                            # Get the declaration index of the user using the tempPlayerArray index
                            currentPlayer = getDeclarationIndex(splitline[3])

                            # If the user ID is not the standard length of 22, fail
                            if (len(splitline[3]) != 22):
                                skipGame = True
                                failInfo.append(["ERROR: User ID is nonstandard length", ("file: " + datafile), ("Game ID: " + str(gameArray[gameIDIndex])), ("line: " + str(lineNumber)), ("ID: " + splitline[3])])
                            else:
                                # Save the user ID and dollar amount in chips
                                gameArray[firstUserIndex + currentPlayer - 1][0] = splitline[3]
                                gameArray[firstUserIndex + currentPlayer - 1][1] = float(splitline[4].replace("(", "").replace("$", "").replace(",", ""))


                        # Extract the blind post declarations, antes posted, dealer seat 
                        # getting shifted, or a player sitting out
                        elif (re.search("Posts small blind", line)):
                            gameArray[smallBlindIndex] = getDeclarationIndex(splitline[0])
                            extractUserAction(splitline, userPreGameIndex)

                        elif (re.search("Posts big blind", line)):
                            gameArray[bigBlindIndex] = getDeclarationIndex(splitline[0])
                            extractUserAction(splitline, userPreGameIndex)

                        elif (re.search("- Ante", line)): # ante
                            extractUserAction(splitline, userPreGameIndex)

                        elif (re.search("button moves to Seat", line)):
                            dealerSeat = int(splitline[4])  # The dealer seat shifts

                        elif (re.search("- sitout", line)): # sitout
                            extractUserAction(splitline, userPreGameIndex)

                        else:
                            # Since the players are all saved, update the gameArray's info
                            # Save the number of players
                            gameArray[numPlayersIndex] = len(tempPlayerArray)

                            # Set the dealer player
                            # If the dealer is dead, set the dealer index to 0
                            try:
                                gameArray[dealerIndex] = tempPlayerIndex.index(dealerSeat) + 1
                            except Exception:
                                gameArray[dealerIndex] = 0


                    # Parse the user actions during the pocket cards, flop, turn, river, and showdown sections
                    elif ((currentSector == "pocketCards") and lineNotEmpty):
                        extractUserAction(line.split(), userPocketCardsIndex)

                    elif ((currentSector == "flop") and lineNotEmpty):
                        extractUserAction(line.split(), userFlopIndex)

                    elif ((currentSector == "turn") and lineNotEmpty):
                        extractUserAction(line.split(), userTurnIndex)

                    elif ((currentSector == "river") and lineNotEmpty):
                        extractUserAction(line.split(), userRiverIndex)

                    elif ((currentSector == "showdown") and lineNotEmpty):
                        extractUserAction(line.split(), userShowdownIndex)



                    # If this is currently the summary, get the total pot, board results (if any),
                    # and the user results. Update the gamesList once the parsing is done.
                    elif (currentSector == "summary"):

                        # Extract the total pot amount
                        if (re.search("Total Pot", line)):
                            line = line.split()

                            if (re.search(":", line[1])):
                                line = line[1].replace("Pot($", "").replace(",", "").split(":")
                                line = line[0]
                            else:
                                line = line[1].replace("Pot($", "").replace(")", "").replace(",", "")

                            gameArray[totalPotIndex] = float(line)

                        # Extract the board configuration from the line after the Total Pot amount
                        elif (re.search("Board", line)):
                            line = line.split()

                            for x in range(1, len(line)):
                                gameArray[boardCardsIndex].append(line[x].replace("[", "").replace("]", ""))

                        # Else parse the user results in the summary (TODO)
                        elif (re.search("Seat", line)): 
                            # splitline = line.split()

                            if (re.search("collected", line)):
                                # Split before the amount collected
                                splitline = line.split("Total")

                                gameArray[gameLostIndex][collectorPresentIndex] = True
                                # get index of collector, and get the collecter amount

                                if (re.search("HI:", line)):
                                    if (re.search("Does", line)):
                                        print("collecter did not show")
                                    else:
                                        print("collecter showed")


                            elif (re.search("won", line)):
                                print("game won")

                            elif (re.search("lost", line)):
                                # Split at the point before the cards list and the name of the hand
                                splitline = line.split("[")

                                gameArray[gameLostIndex][loserPresentIndex] = True
                                gameArray[gameLostIndex][indexOfLoserIndex] = getDeclarationIndex(line.split()[2])

                                # Save the hand description
                                gameArray[gameLostIndex][losingHandIndex][lHCardDescriptIndex] = splitline[0].split("with")[1].strip()

                                # Save the cards played and the full hand
                                gameArray[gameLostIndex][losingHandIndex][lHCardsPlayedIndex] = splitline[1].split("-")[0].split()
                                gameArray[gameLostIndex][losingHandIndex][lHCardsTableIndex] = splitline[1].split("-")[1].replace("]", "").split(",")


                        # If the line is blank and the array has not been updated yet, append it to the
                        # gamesList and change the arrayListUpdated flag
                        elif(not arrayListUpdated):
                            gamesList.append(gameArray)
                            arrayListUpdated = True


        # If any error happens, print the filename, line number, and line, then throw an exception
        except Exception:
            print("ERROR")
            print("In file:     " + datafile)
            print("Line number: " + str(lineNumber))
            print("Line:        " + line)
            traceback.print_exc()

            print(" ")
            if(input("Continue parsing (and ignore this file)? [y/n]: ").lower() == "n"):
                exit(0)
            else:
                gamesList ="NULL"
            print(" ")


    # Log any known errors encountered
    if ((len(failInfo) != 0) or (gamesList == "NULL")):

        with open("errorlog.txt", 'a') as f:

            for x in range(0, len(failInfo)):
                f.write(str(failInfo[x]) + "\n")

            if (gamesList == "NULL"):
                f.write("FILE ABORTED: " + filename)

            f.write("\n")


    # once all of the games in a file have been parsed, return the list
    return gamesList




# Parse a user's action from a line and save the results in the user's array in the gameArray
def extractUserAction(line, sectorIDX):
    global skipGame
    global failInfo
    global lineNumber
    global filename

    action = line[2]
    actionEntry = []

    if ( (action == "Bets") or (action == "Calls") or (action == "All-In") ):
        actionEntry.append(action)
        actionEntry.append(float(line[3].replace("$", "").replace(",", "")))

    elif (action == "Raises"):
        actionEntry.append("Raises")
        actionEntry.append([line[3].replace("$", ""), line[5].replace("$", "")])

    elif (action == "returned"):
        actionEntry.append("returned")
        actionEntry.append(float(line[3].replace("($", "").replace(")", "").replace(",", "")))

    elif (action == "Shows"):
        actionEntry.append("Shows")
        actionEntry.append([line[3].replace("[", ""), line[4].replace("]", "")])

    elif (line[1] == "Collects"):
        actionEntry.append("Collects")
        actionEntry.append(float(line[2].replace("$", "").replace(",", "")))

    elif (action == "Posts"):

        # If the user posts a small blind
        if (line[3] == "small"):
            actionEntry.append("Posts small blind")
            actionEntry.append(float(line[5].replace("$", "").replace(",", "")))

        # If the user posts a big blind
        elif (line[3] == "big"):
            actionEntry.append("Posts big blind")
            actionEntry.append(float(line[5].replace("$", "").replace(",", "")))

    elif (action == "Does"):
        actionEntry.append("Does not show")

    elif (action == "Ante"):

        # if an ante is returned
        if (line[3] == "returned"):
            actionEntry.append("Ante returned")
            actionEntry.append(float(line[4].replace("$", "").replace(",", "")))

        # if an ante is posted
        else:
            actionEntry.append("Ante")
            actionEntry.append(float(line[3].replace("$", "").replace(",", "")))

    else:
        actionEntry.append(action) # check, fold, muck, or sitout

    try:
        # Determine the player's absolute index in the gameArray using tempPlayerArray
        playerIDX = firstUserIndex + tempPlayerArray.index(line[0])
    
        # If the player has not made a move during the current sector, replace the first value
        # (which is blank) in the play actions array
        if(gameArray[playerIDX][sectorIDX][0][0] == "NA"):
            gameArray[playerIDX][sectorIDX][0] = actionEntry
        else:
            # Otherwise, the player has made a move, so append the action
            gameArray[playerIDX][sectorIDX].append(actionEntry)
    
    except Exception as e:
        # The user is not declared before an action
        # (as in file "abs NLH handhq_61-OBFUSCATED.txt", at line 6662)
        skipGame = True
        failInfo.append(["ERROR: Exception while adding user action to gameArray", ("file: " + filename), ("Game ID: " + str(gameArray[gameIDIndex])), ("line: " + str(lineNumber)), e])





# In the dataset files, the users are not declared in order and they are given 
# number IDs that are not consecutive. Therefore, the script gives the players an 
# index value as they appear, and resolves the discrepancies by using the
# tempPlayerArray and tempPlayerIndex arrays. This method retrives the players'
# actual index (how they show up) from their username using an index lookup in the tempPlayerArray
def getDeclarationIndex(value):

    global tempPlayerArray
    global lineNumber
    global filename
    global skipGame

    try:
        return int(tempPlayerArray.index(value) + 1)
    except Exception as e:
        skipGame = True
        failInfo.append(["ERROR: Player not declared but shows up mid-game", ("file: " + filename), ("Game ID: " + str(gameArray[gameIDIndex])), ("line: " + str(lineNumber)), e])
        return 0
