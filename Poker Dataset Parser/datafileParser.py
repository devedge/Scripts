import re

# the data file is parsed line by line
# as each line is being processed, variables keep track of where in the file the 
#       current line is.

# player numbers are assigned in the order they appear
# their IDs and number are stored in two different arrays for temporary reference

firstGame = True
currentSector = "init"
dealerSeat = 0
tempPlayerArray = []
tempPlayerIndex = []
gamesList = []
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



file = "/home/usr/dataset-50.txt"


def parseFile(datafile):

    global firstGame
    global tempPlayerArray
    global tempPlayerIndex
    global dealerSeat
    global currentSector

    initGameArray()
    initPlayerInstance()

    seatCounter = 0

    with open(datafile, 'r') as f:

        linenumber = 0

        # Parse the file line by line
        for line in f:

            linenumber += 1
            # This is the first line of a game, so reset all of the per-game variables.
            # Then, extract the gameID, date, and time & timezone. 
            if (re.search("Stage", line)):
               
                # reset all the per-game variables
                tempPlayerArray = []
                tempPlayerIndex = []
                initPlayerInstance()
                initGameArray()
                
                currentSector = "init"
                dealerSeat = 0

                line = line.split()
                
                gameArray[0] = int(line[1].replace("#", "").replace(":", ""))   # insert game ID
                gameArray[1] = line[7]                                          # insert date
                gameArray[2] = (line[8] + line[9])                              # insert time and timezone
            
            # This is the second line of a new game, so extract and
            # save the dealer seat number from the line.
            elif (re.search("Table", line)):
                print(line)
                line = line.split()

                 # len(line) - 4 

                dealerSeat = int(line[line.index("Seat") + 1].replace("#", "")) 

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
            elif (len(line.split()) != 0):  # as long as the line is not empty
                # If this is the "init" sector, first grab the seat initializations, then
                # grab the blind posts
                if (currentSector == "init"):
                    splitline = line.split()

                    # Extract the seat assignments, user IDs, and dollar amount in chips per
                    # user
                    if (re.search("Seat", line)):
                        # append an initialized playerArrayInstance to the gameArray
                        initPlayerInstance()
                        gameArray.append(playerArrayInstance)

                        tempPlayerArray.append(splitline[3])
                        tempPlayerIndex.append(int(splitline[1]))

                        # Save the user ID and dollar amount in chips
                        currentPlayer = tempPlayerArray.index(splitline[3]) + 1
                        gameArray[11 + currentPlayer][0] = splitline[3]
                        gameArray[11 + currentPlayer][1] = float(splitline[4].replace("(", "").replace("$", "").replace(",", ""))

                    # Extract the blind post declarations
                    else:
                        if (re.search("small blind", line)):
                            gameArray[8] = tempPlayerArray.index(splitline[0]) + 1
                        else:
                            gameArray[9] = tempPlayerArray.index(splitline[0]) + 1  # the big blind is always last

                            # Since the players are all saved, update the gameArray's info
                            # Save the number of players
                            gameArray[6] = len(tempPlayerArray)
                            print(linenumber)
                            # Set the dealer player
                            gameArray[7] = tempPlayerIndex.index(dealerSeat) + 1


                # Parse all of the actions taken during the Pocket Cards round
                if (currentSector == "pocketCards"):
                    extractUserAction(line.split(), 2)

                if (currentSector == "flop"):
                    extractUserAction(line.split(), 3)

                if (currentSector == "turn"):
                    extractUserAction(line.split(), 4)

                if (currentSector == "river"):
                    extractUserAction(line.split(), 5)

                if (currentSector == "showdown"):
                    extractUserAction(line.split(), 6)

                # If this is currently the summary, get the total pot, board results (if any),
                # and the user results
                if (currentSector == "summary"):
                    # Extract the total pot amount from the line
                    if (re.search("Total Pot", line)):
                        line = line.split()

                        gameArray[5] = float(line[1].replace("Pot($", "").replace(")", "").replace(",", ""))

                    # Extract the board configuration from the line
                    elif (re.search("Board", line)):
                        line = line.split()

                        for x in range(1, len(line)):
                            gameArray[4].append(line[x].replace("[", "").replace("]", ""))

                    # Else parse the user results
                    elif (re.search("Seat", line)): 
                        # search for the word "Seat", and keep a count of the number of seats, 
                        # since there is no indication of when the game is over
                        seatCounter += 1
                        # print("help")
                        # print(gameArray[6])
                        # print(seatCounter)
                        line = line.split()

                        # find out who won, who lost, who collected, and any other info that might be needed

                        if (seatCounter == gameArray[6]):
                            seatCounter = 0
                            gamesList.append(gameArray)
    
    # once all of the games in a file have been parsed, return the list
    return gamesList


# Parse a user's action from a line and save the results in the gameArray
def extractUserAction(line, sectorIDX):

    action = line[2]
    actionEntry = []

    if (action == "Bets"):
        actionEntry.append("Bets")
        actionEntry.append(float(line[3].replace("$", "").replace(",", "")))

    elif (action == "Calls"):
        actionEntry.append("Calls")
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

    playerIDX = 11 + tempPlayerArray.index(line[0]) + 1

    if(gameArray[playerIDX][sectorIDX][0][0] == "NA"):
        gameArray[playerIDX][sectorIDX][0] = actionEntry
    else:                        
        gameArray[playerIDX][sectorIDX].append(actionEntry)




####### Testing and debugging #######
newlist = parseFile(file)

print(newlist[300])

# somevalue = 2
# print(" ")
# # print(newlist[0])
# # print(" ")
# # print(newlist[1])
# # print(" ")
# print(newlist[somevalue][0:10])
# print(" ")
# print(newlist[somevalue][10])
# print(" ")
# print(newlist[somevalue][11])
# print(" ")
# print(newlist[somevalue][12])
# print(" ")
# print(newlist[somevalue][13])
# print(" ")

# print(newlist[somevalue][14])
# print(" ")
# # print(newlist[somevalue][14][2])
# # print(newlist[somevalue][14][3])
# # print(newlist[somevalue][14][4])
# # print(newlist[somevalue][14][5])
# # print(newlist[somevalue][14][6])

# # print(" ")

# print(newlist[somevalue][15])
# print(" ")
# print(newlist[somevalue][16])
# print(" ")
# # print(newlist[somevalue][16])
# # print(" ")
# # print(newlist[3])
# print(" ")
