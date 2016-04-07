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


The only part of the script that needs to be edited is `writeCSV()`, between the comment headers `#### ---- ####`. Examples are provided in the file. <br><br>

For each row that you want to have in the CSV file, use `csvrow.append()` to add the value from the gameArray. These values are extracted using the API methods from parserAPI.py. All of the possible methods you can use are provided below under the `parserAPI.py` section.<br><br>
For example, to get the game ID of each game, you would use `parserAPI.getGameID()`. <br>
Appending it as a row in the CSV file would look like: `csvrow.append(parserAPI.getGameID())` <br>
After all of the values have been appended, use `csvFile.writerow(csvrow)` to write the row to the file.

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

