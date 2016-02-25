import re

# the data file is parsed line by line
# as each line is being processed, variables keep track of where in the file the 
#       current line is.

# player numbers are assigned in the order they appear
# their IDs and number are stored in two different arrays for temporary reference

firstGame = True
arrayListUpdated = False
currentSector = "init"
dealerSeat = 0
tempPlayerArray = []
tempPlayerIndex = []
# gamesList = []
gameArray = []
playerArrayInstance = []


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
                        [],         #  money received
                        ""          #  winning hand (the full string?)
                    ],
                    [
                        False,      #  is there a loser      # 11  lost info
                        0,          #  number of losers
                        [],         #  index of losers
                        ""          #  losing hand (the full string?)
                    ]
                ]

# Initializes a blank player array
def initPlayerInstance():
    global playerArrayInstance

    playerArrayInstance =   [
                                "NULL",     # player ID
                                0.0,        # dollars in chips
                                [["NA"]],   # user actions during the Pocket Cards
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

    gamesList = []
    initGameArray()
    initPlayerInstance()

    lineNumber = 0 # for debugging purposes

    with open(datafile, 'r') as f:

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

                # Begin to parse the first line
                line = line.split()
                dashIndex = line.index("-")
                
                gameArray[0] = int(line[1].replace("#", "").replace(":", ""))   # insert game ID
                gameArray[1] = line[dashIndex + 1]                              # insert date  (7)
                gameArray[2] = (line[dashIndex + 2] + line[dashIndex + 3])      # insert time and timezone (8 & 9)
            

            # This is the second line of a new game, so extract and
            # save the dealer seat number from the line.
            elif (re.search("Table", line)):
                line = line.split()

                 # Get the dealer seat number from the value that comes after the word "Seat"
                dealerSeat = int(line[line.index("Seat") + 1].replace("#", "")) 


            # Update the current sector the script is in as it progresses through the game
            elif (re.search("\*\*\* POCKET CARDS \*\*\*", line)):
                currentSector = "pocketCards"
                gameArray[3] += 1
            
            elif (re.search("\*\*\* FLOP \*\*\*", line)):
                currentSector = "flop"
                gameArray[3] += 1
            
            elif (re.search("\*\*\* TURN \*\*\*", line)):
                currentSector = "turn"
                gameArray[3] += 1

            elif (re.search("\*\*\* RIVER \*\*\*", line)):
                currentSector = "river"
                gameArray[3] += 1

            elif (re.search("\*\*\* SHOW DOWN \*\*\*", line)):
                currentSector = "showdown"
                gameArray[3] += 1

            elif (re.search("\*\*\* SUMMARY \*\*\*", line)):
                currentSector = "summary"


            # Depending on the current sector the loop is in, parse the user actions and 
            # populate the gameArray
            else:
                # Is the current line empty?
                lineNotEmpty = bool(len(line.split()) != 0)

                # If this is the "init" sector, first grab the seat initializations, then
                # grab the blind posts.
                # Get the information from the lines following the 'Stage' and 'Table' declarations
                if ((currentSector == "init") and lineNotEmpty): 
                    splitline = line.split()

                    # Extract the seat assignments, user IDs, and dollar amount in chips per
                    # user
                    if (re.search("Seat", line)):

                        # append an initialized playerArrayInstance to the gameArray
                        initPlayerInstance()
                        gameArray.append(playerArrayInstance)

                        # Set up temporary arrays that are used to find out what order players were declared
                        tempPlayerArray.append(splitline[3])

                        try:
                            tempPlayerIndex.append(int(splitline[1]))
                        except Exception as e:
                            print(lineNumber)
                            print(datafile)
                            raise e
                        
                        # Get the declaration index of the user using the tempPlayerArray index
                        currentPlayer = tempPlayerArray.index(splitline[3]) + 1

                        # Save the user ID and dollar amount in chips
                        gameArray[11 + currentPlayer][0] = splitline[3]
                        gameArray[11 + currentPlayer][1] = float(splitline[4].replace("(", "").replace("$", "").replace(",", ""))

                    # Extract the blind post declarations
                    # need to save the antes, sitout (game 3064882390)
                    else:
                        if (re.search("Posts small blind", line)):
                            gameArray[8] = tempPlayerArray.index(splitline[0]) + 1
                        elif (re.search("Posts big blind", line)):
                            gameArray[9] = tempPlayerArray.index(splitline[0]) + 1

                            # Since the players are all saved, update the gameArray's info
                            # Save the number of players
                            gameArray[6] = len(tempPlayerArray)

                            # Set the dealer player
                            # If the dealer is dead, set the dealer index to 0
                            try:
                                gameArray[7] = tempPlayerIndex.index(dealerSeat) + 1
                            except Exception:
                                gameArray[7] = 0


                # Parse the user actions during the pocket cards, flop, turn, river, and showdown sections
                elif ((currentSector == "pocketCards") and lineNotEmpty):
                    extractUserAction(line.split(), 2)

                elif ((currentSector == "flop") and lineNotEmpty):
                    extractUserAction(line.split(), 3)

                elif ((currentSector == "turn") and lineNotEmpty):
                    extractUserAction(line.split(), 4)

                elif ((currentSector == "river") and lineNotEmpty):
                    extractUserAction(line.split(), 5)

                elif ((currentSector == "showdown") and lineNotEmpty):
                    extractUserAction(line.split(), 6)



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

                        gameArray[5] = float(line)

                    # Extract the board configuration from the line after the Total Pot amount
                    elif (re.search("Board", line)):
                        line = line.split()

                        for x in range(1, len(line)):
                            gameArray[4].append(line[x].replace("[", "").replace("]", ""))

                    # Else parse the user results in the summary (TODO)
                    elif (re.search("Seat", line)): 

                        line = line.split()

                        # find out who won, who lost, who collected, and any other info that might be needed


                    # If the line is blank and the array has not been updated yet, append it to the
                    # gamesList and change the arrayListUpdated flag
                    elif(not arrayListUpdated):
                        gamesList.append(gameArray)
                        arrayListUpdated = True


    # once all of the games in a file have been parsed, return the list
    return gamesList


# Parse a user's action from a line and save the results in the gameArray
def extractUserAction(line, sectorIDX):

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

    elif (action == "Does"):
        actionEntry.append("Does not show")

    else:
        actionEntry.append(action) # check, fold, or muck

    # Determine the player's absolute index in the gameArray using tempPlayerArray
    playerIDX = 11 + tempPlayerArray.index(line[0]) + 1

    # If the player has not made a move during the current sector, replace the first value
    # (which is blank) in the play actions array
    if(gameArray[playerIDX][sectorIDX][0][0] == "NA"):
        gameArray[playerIDX][sectorIDX][0] = actionEntry
    else:
        # Otherwise, the player has made a move, so append the action
        gameArray[playerIDX][sectorIDX].append(actionEntry)




####### Testing and debugging #######
# newlist = parseFile(file)

# print(len(newlist))

# for x in range(0, len(newlist)):
#     print(gamesList[x])


## TODO ##

# when there are Antes, they get announced before the small and big blind get posted.
# need to check that

# when a dealer is dead, there is no dealer seat

