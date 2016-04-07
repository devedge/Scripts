## About

Python parser script for a poker dataset taken from [here](https://web.archive.org/web/20110205042259/http://www.outflopped.com/questions/286/obfuscated-datamined-hand-histories)

***

Run with: <br>
```bash
python csvGenerator.py
```

or: <br>
```bash
python csvGenerator.py /absolute/path/to/dataset/folder outputResults.csv y
```
<br>
Where `/absolute/path/to/dataset/folder`  contains all the (unzipped) text data to mine, `outputResults.csv` is the CSV file that gets generated, and `y` (yes) will overwrite the CSV file if it already exists (`n`, no, will not overwrite the file and will prompt for a new name).



[Download the ZIP containing the script.](https://github.com/devedge/Scripts/raw/master/Poker%20Dataset%20Parser/data/PokerDatasetParser.zip) This has only been tested with Python >= 3.5.<br><br>


## Setup

The structure of the CSV file (rows and columns) needs to be manually defined in `csvGenerator.py`. None of the other files need to be changed. More information on how to edit the file is defined in the `csvGenerator.py` section below.<br><br>


## Program Logic

The general program logic is split up into three different Python files. The parser itself is `datafileParser.py`, the API for interacting with the parser is `parserAPI.py`, and the front-end that handles interaction with the user and creates the CSV files is `csvGenerator.py`.


<br>
<h5>`csvGenerator.py`     [view](https://github.com/devedge/Scripts/blob/master/Poker%20Dataset%20Parser/csvGenerator.py)</h5> <br>
The part of the script that needs to be edited is the first method in `writeCSV()` at the top of the file. 
<br>
The parser returns one game at a time (gameArray), and between the comment headers `#### ---- ####` is the code where each value is added to the current row. For each value you want to add to the current row, use `csvrow.append()`. These values are extracted using methods from `parserAPI.py`, which are all defined below in the `parserAPI.py` section.
<br>
For example in the code provided below:
 - `parserAPI.getGameID()` returns the current game's ID
 - `parserAPI.getDate()` returns the date of the game
 - `parserAPI.isGameWon()` returns 'true' if the game was won, and 'false' if otherwise
 - `parserAPI.getTotalPot()` returns the game's total pot amount
<br>
```python
# Writes the csv file from information gathered from the gameArray
def writeCSV(gameArray):
    global csvFile

    # Initialize the gameArray in parserAPI
    parserAPI.initGameArray(gameArray)

    # array of values taken from parserAPI.py using the gameArray
    csvrow =  []

    #### ---- ####  Edit this part so the values are appended to the array as a row

    # For each game, store the game ID, date, if the game was won, what the total pot was
    csvrow.append(parserAPI.getGameID())
    csvrow.append(parserAPI.getDate())
    csvrow.append(parserAPI.isGameWon())
    csvrow.append(parserAPI.getTotalPot())

    #### ---- ####

    # Writes the current row to disk
    csvFile.writerow(csvrow)
```


<br>
The 'csvGenerator.py' script is in charge of getting user input, scanning every directory and subdirectory, passing each file to the datafileParser.py script, and writing the values to a CSV file.

<br><br>
<h5>`parserAPI.py`     [view](https://github.com/devedge/Scripts/blob/master/Poker%20Dataset%20Parser/parserAPI.py)</h5> <br>
This script is dedicated to providing readable methods to extract values from the gameArray that `datafileParser.py` returns.
<br>
Currently, all of the methods and their descriptions are in the parserAPI file. They will be added here soon.

<br><br>
<h5>`datafileParser.py`     [view](https://github.com/devedge/Scripts/blob/master/Poker%20Dataset%20Parser/datafileParser.py)</h5> <br>
This script parses a poker game text file. It saves each game in the file as a gameArray, and saves all of the games in one long gamesList, which is returned. [An example gameArray](https://github.com/devedge/Scripts/blob/master/Poker%20Dataset%20Parser/data/example%20gameArray.txt)

