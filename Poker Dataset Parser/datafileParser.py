
import re

# the file is parsed like a state machine (will have to do it anyway since every line needs to be parsed)
# as each line is processed, counters and indices are updated to reflect the current state of the 
#   lines being processed

# player numbers are assigned in the order they appear
# their IDs and number are stored in an array to quickly reference just over the current parsing

datafile = "/home/usr/dataset-test.txt"

# c1 = 0
# c2 = 0

# numberGamesParsed = 0

# def parseFile():

gamearray = []
initGameArray()

with open(datafile, 'r') as f:


    dealerSeat = 0

    pocketCards = False
    flop = False
    turn = False
    river = False
    showdown = False

    # Parse every line in the file
    for line in f:

        # This is the first line of a game, so (return the results of 
        # the last game?) and reset all of the per-game variables.
        # Then, extract the gameID, date, and time & timezone. 
        if (re.search("Stage", line)):
            # return the results of the last game?
            # reset all the per-game variables
            
            dealerSeat = 0

            line = line.split()
            
            # line[1] = int(line[1].replace("#", "").replace(":", ""))
            
            gamearray[0] = int(line[1].replace("#", "").replace(":", ""))   # insert game ID
            gamearray[1] = line[7]                                          # insert date
            gamearray[2] = (line[8] + line[9])                              # insert time and timezone

            #gamearray.append(line[1])           # append game ID
            #gamearray.append(line[7])           # append date
            #gamearray.append(line[8] + line[9]) # append time and timezone
            
            # print(gamearray)
            # print(line)
            # c1 += 1
            # go to a method that quits when the next game is found?
        
        # This is the second line of a new game, so extract and
        # save the dealer seat number from the line.
        elif (re.search("Table", line)):
            line = line.split()

            # doesn't work if the table has two-worded name (should work now)
            dealerSeat = int(line[ len(line) - 4 ].replace("#", "")) 

        # Use a REGEX to find the initial declaration of seats
        elif (re.search("", line)):
            
            line = line.split()

        # if pocket cards haven't started and the line contains "blind"

        # elif (re.search("*** POCKET CARDS ***", line)):
        # edits the first play array
        
        # elif (re.search("*** FLOP ***", line)):
        # edits the second play array
        
        # elif (re.search("*** TURN ***", line)):
        # edits the third play array

        # elif (re.search("*** RIVER ***", line)):
        # edits the fourth play array

        # elif (re.search("*** SHOW DOWN ***", line)):
        # edits the fifth play array

        # elif (re.search("*** SUMMARY ***", line)):
        # marks the end of the game

        # elif (re.search("Total Pot", line)):
        # 




def initGameArray():
    global gamearray

    gamearray = [   
                    0,       # game ID           (int)
                    "NULL",  # date              (string)
                    "NULL",  # time and timezone (string)
                    False,   # game won          (boolean)
                    0,       # number of rounds  (int)
                    ["NULL", "NULL", "NULL", "NULL", "NULL"], # cards on board  (strings)
                    0.0,     # total pot         (double)
                    0.0,     # win amount        (double)
                    0,       # number of players (int)
                    0,       # dealer player     (int)
                    0,       # small bind player (int)
                    0,       # big bind player   (int)
                    0,       # winning player    (int)
                    [        # player 1 nested array
                        "NULL",  # player ID        (string)
                        0.0,     # dollars in chips (double)
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"]
                    ], 
                    [        # player 2 nested array
                        "NULL",  # player ID        (string)
                        0.0,     # dollars in chips (double)
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"], 
                        ["NULL", "NULL"]
                    ]
                    # etc... another nested array for each player
                ]








