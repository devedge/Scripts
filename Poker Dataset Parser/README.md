## About

Python parser script for a poker dataset taken from [here](https://web.archive.org/web/20110205042259/http://www.outflopped.com/questions/286/obfuscated-datamined-hand-histories)

***


To run, [download the ZIP file](https://github.com/devedge/Scripts/raw/master/Poker%20Dataset%20Parser/PokerDatasetParser.zip), extract it, and in the directory, run: `python csvGenerator.py` from the command line. (Note: this has only been tested with Python 3.5)
<br><br>

Advanced: <br> 
Run with `python csvGenerator.py /absolute/path/to/dataset/folder output.csv y` <br><br>
The second argument (/absolute/path/to/dataset/folder) is the absolute path to the dataset folder. All of the files in the folder must be the raw text files (eg., uncompress them before running the parser) <br><br>
The third argument is the CSV output file that will be generated. The fourth (and optional) argument (y), which means 'yes', is to overwrite the specified CSV file if it already exists.<br><br>


## Setup

The structure of the CSV rows needs to be manually defined, as needed, in csvGenerator.py. <br>
More information is provided under the `csvGenerator.py` section below. <br><br>


## Program Logic

There are three python scripts that take care of the three major tasks involved: a parser (datafileParser.py), an interface for the user to interact with (csvGenerator.py), and an API that simplifies getting data from the parser (parserAPI.py)

<br>
<h1>`csvGenerator.py`</h1> <br>

The only part of the script that needs to be edited is `writeCSV()`, between the comment headers `#### ---- ####` <br><br>

For each row that you want to have in the CSV file, use `csvrow.append()` to add the value from the gameArray that you want. These values are extraced using the API methods from parserAPI.py. All of the possible methods you can use to extract game values are provided below under `parserAPI.py` <br><br>
For example, to get the game ID of each game, you would use `parserAPI.getGameID()`. Appending it as a row in the CSV file would look like: `csvrow.append(parserAPI.getGameID())` <br>
After all of the values have been appended, use `csvFile.writerow(csvrow)` to write the row to the file.

<br>
The 'csvGenerator.py' script is in charge of getting user input, scanning every directory and subdirectory, passing each file to the datafileParser.py script, and writing the values to a CSV file.

<br><br>
<h1>`parserAPI.py`</h1> <br>
This script is dedicated to providing readable methods to extract values from the gameArray that `datafileParser.py` returns.
...

<br><br>
<h1>`datafileParser.py`</h1> <br>
...

