 
example1 =  [   
                3065607844,     # game ID
                "2009-07-14",   # date
                "19:34:54(ET)", # time and timezone
                5,              # number of rounds
                ["Ac", "Jc", "9d", "10s", "4s"],   # cards on board (can be variable)
                90,             # total pot amount
                5,              # num players
                1,              # dealer player
                1,              # small blind player
                2,              # big blind player
                [
                    True,       # game won              # win info
                    False,      # only collected
                    2,          # number of winners
                    [1, 2],     # index of winners
                    [43.50, 43.50]  # money received
                ],
                [
                    False,      # is there a loser      # lost info
                    0,
                    [0]
                ],
                [
                    "ZUf4UYlizITQF4Jk5sMf1A",   # player1 ID
                    1041,                       # dollars in chips
                    [["Raises", [30, 30]]],       # pocketCards       [action taken, value (if applicable)]
                    [["Checks", "NULL"]],         # flop
                    [["Checks", "NULL"]],         # turn
                    [["Checks", "NULL"]],         # river
                    [["Mucks", "NULL"]]           # showdown
                ], 
                [
                    "bSDJwbTmGA4R+u3vEJdXIA",
                    1012,
                    ["Calls", 25], 
                    ["Checks", "NULL"], 
                    ["Checks", "NULL"], 
                    ["Checks", "NULL"], 
                    ["Shows", ["9h", "8h"]]
                ],
                [
                    "y/xXiv3wrsVNOi4N7qXbuQ",
                    3401,
                    ["Calls", 20], 
                    ["Checks", "NULL"], 
                    ["Checks", "NULL"], 
                    ["Checks", "NULL"], 
                    ["Shows", ["9c", "6c"]]
                ],
                [
                    "X+u4T/E5ANkyZLKm1YjqwQ",
                    2468,
                    ["Folds", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"]
                ],
                [
                    "m5CQJNykYZdkaA89KwHNwQ",
                    2537.50,
                    ["Folds", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"], 
                    ["NA", "NULL"]
                ]
            ]

example2 =  [   
                3065446638,     # game ID
                "2009-07-14",   # date
                "18:49:11(ET)", # time and timezone
                5,              # number of rounds
                ["9d", "Ac", "7c", "Ah", "7h"],   # cards on board
                505,             # total pot amount
                6,              # num players
                1,              # dealer player
                2,              # small blind player
                3,              # big blind player
                [
                    True,       # game won              # win info
                    False,      # only collected
                    1,          # number of winners
                    [1],        # index of winners
                    [502],      # money received
                    ""          # winning hand (the full string)
                ],
                [
                    True,       # is there a loser      # lost info
                    1,          # number of losers
                    [3],        # index of losers
                    ""          # losing hand (the full string)
                ],
                [
                    "y/xXiv3wrsVNOi4N7qXbuQ",   # player1 ID
                    2898,                       # dollars in chips
                    [["Raises", [35, 35]]],       # [action taken, value (if applicable)]
                    [["Bets", 75]],
                    [["Bets", 140]], 
                    [["Checks", "NULL"]], 
                    [["Shows", ["10s", "Ad"]], ["Collects", 502]]
                ], 
                [
                    "9nEoiyBNT/5DNeziCrBkEw",
                    2164,
                    [["Folds", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]]
                ],
                [
                    "T2Y2AuJwSBvEYdoHMU4m1A",
                    2874.50,
                    [["Calls", 25]], 
                    [["Checks", "NULL"], ["Calls", 75]], 
                    [["Checks", "NULL"], ["Calls", 140]], 
                    [["Checks", "NULL"]], 
                    [["Shows", ["10d", "10h"]]]
                ],
                [
                    "m5CQJNykYZdkaA89KwHNwQ",
                    2785,
                    [["Folds", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]]
                ],
                [
                    "ZUf4UYlizITQF4Jk5sMf1A",
                    1186,
                    [["Folds", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]]
                ],
                [
                    "bSDJwbTmGA4R+u3vEJdXIA",
                    992,
                    [["Folds", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]], 
                    [["NA", "NULL"]]
                ]
            ]



gameIDIndex = 0
dateIndex = 1
timeIndex = 2


# should initialize the gamearray here once, and provide a method to wipe it after use

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
    return bool(gameArray[3])

# 


# 
# returns the first user if no user number is specified
# Returns a string
def getUserID(gameArray, numUser = 1):
    return gameArray[12 + numUser][1]

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




# to access everythink played by round:
#                13                6
# for x in range(playerarraystart, getNumPlayers()):
#    do something to each player


def getPlayerAction(playerID, playNumber):
    print("yeye")
    # if check return check
    # if bet return bet and amount
    # if call return call and amount
    # if raise return raise and [from amount, to amount]
    # if fold return fold
    # if muck return muck