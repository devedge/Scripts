import re
import traceback

# the data file is parsed line by line
# as each line is being processed, variables keep track of where in the file the 
#       current line is.

# player numbers are assigned in the order they appear
# their IDs and number are stored in two different arrays for temporary indexing reference


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
                    
                    gameArray[0] = int(line[1].replace("#", "").replace(":", ""))   # insert game ID
                    gameArray[1] = line[dashIndex + 1]                              # insert date  (7)
                    gameArray[2] = (line[dashIndex + 2] + line[dashIndex + 3])      # insert time and timezone (8 & 9)
                

                # This is the second line of a new game, so extract and
                # save the dealer seat number from the line.
                elif (re.search("Table", line) and not skipGame):
                    line = line.split()

                     # Get the dealer seat number from the value that comes after the word "Seat"
                    dealerSeat = int(line[line.index("Seat") + 1].replace("#", "")) 


                # Update the current sector the script is in as it progresses through the game
                elif (re.search("\*\*\* POCKET CARDS \*\*\*", line) and not skipGame):
                    currentSector = "pocketCards"
                    gameArray[3] += 1
                
                elif (re.search("\*\*\* FLOP \*\*\*", line) and not skipGame):
                    currentSector = "flop"
                    gameArray[3] += 1
                
                elif (re.search("\*\*\* TURN \*\*\*", line) and not skipGame):
                    currentSector = "turn"
                    gameArray[3] += 1

                elif (re.search("\*\*\* RIVER \*\*\*", line) and not skipGame):
                    currentSector = "river"
                    gameArray[3] += 1

                elif (re.search("\*\*\* SHOW DOWN \*\*\*", line) and not skipGame):
                    currentSector = "showdown"
                    gameArray[3] += 1

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
                            currentPlayer = getDeclarationIndex(splitline[3]) # tempPlayerArray.index(splitline[3]) + 1 #

                            # If the user ID is not the standard length of 22, fail
                            if (len(splitline[3]) != 22):
                                skipGame = True
                                failInfo.append(["ERROR: User ID is nonstandard length", ("file: " + datafile), ("line: " + str(lineNumber)), ("ID: " + splitline[3])])
                            else:
                                # Save the user ID and dollar amount in chips
                                gameArray[11 + currentPlayer][0] = splitline[3]
                                gameArray[11 + currentPlayer][1] = float(splitline[4].replace("(", "").replace("$", "").replace(",", ""))


                        # Extract the blind post declarations, antes posted, dealer seat 
                        # getting shifted, or a player sitting out
                        elif (re.search("Posts small blind", line)):
                            gameArray[8] = getDeclarationIndex(splitline[0]) # tempPlayerArray.index(splitline[0]) + 1

                        elif (re.search("Posts big blind", line)):
                            gameArray[9] = getDeclarationIndex(splitline[0]) # tempPlayerArray.index(splitline[0]) + 1

                        elif (re.search("- Ante", line)): # ante
                            print("ANTE TODO")

                        elif (re.search("button moves to Seat", line)):
                            # The dealer seat shifts
                            dealerSeat = int(splitline[4])

                        elif (re.search("- sitout", line)): # sitout

                            print("yolo")

                        else:
                            # Since the players are all saved, update the gameArray's info
                            # Save the number of players
                            gameArray[6] = len(tempPlayerArray)

                            # Set the dealer player
                            # If the dealer is dead, set the dealer index to 0
                            try:
                                gameArray[7] = tempPlayerIndex.index(dealerSeat) + 1
                            except Exception:
                                gameArray[7] = 0

                            # elif (re.search("Posts big blind", line)):
                            #     try:
                            #         # find the player in the player array
                            #         gameArray[9] = tempPlayerArray.index(splitline[0]) + 1
                            #     except Exception:
                            #         # If the player was not declared but shows up mid-game, declare it invalid
                            #         # (as in the file "abs NLH handhq_61-OBFUSCATED.txt", line 6655)
                            #         skipGame = True
                            #         failInfo.append(["ERROR: Player not declared but shows up mid-game", ("file: " + datafile), ("line: " + str(lineNumber))])

                            #         # failInfo.append(["INFO: Dead dealer", ("file: " + datafile), ("line: " + str(lineNumber))])

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
    if (len(failInfo) != 0):

        with open("errorlog.txt", 'a') as f:

            for x in range(0, len(failInfo)):
                f.write(str(failInfo[x]) + "\n")

            f.write("\n")


    # once all of the games in a file have been parsed, return the list
    return gamesList


# Parse a user's action from a line and save the results in the gameArray
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

    elif (action == "Does"):
        actionEntry.append("Does not show")

    else:
        actionEntry.append(action) # check, fold, or muck

    try:
        # Determine the player's absolute index in the gameArray using tempPlayerArray
        playerIDX = 11 + tempPlayerArray.index(line[0]) + 1
    
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
        failInfo.append(["ERROR: Exception while adding user action to gameArray", ("file: " + filename), ("line: " + str(lineNumber)), e])



# In the dataset files, the users are not declared in order and they are given 
# number IDs that are not consecutive. Therefore, the script gives the players an 
# index value as they appear, and resolves the discrepancies by using the
# tempPlayerArray and tempPlayerIndex arrays. This method retrives the players'
# actual index (how they show up) from their unsername using an index lookup in the tempPlayerArray
def getDeclarationIndex(value):

    global tempPlayerArray
    global lineNumber
    global filename
    global skipGame

    try:
        return int(tempPlayerArray.index(value) + 1)
    except Exception as e:
        skipGame = True
        failInfo.append(["ERROR: Player not declared but shows up mid-game", ("file: " + filename), ("line: " + str(lineNumber)), e])
        return 0
