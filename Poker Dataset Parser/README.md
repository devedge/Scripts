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

The structure of the CSV rows needs to manually defined, as needed, in the first method (writeCSV()) in csvGenerator.py. <br>
For each row that you want to have in the CSV file, you need to `csvrow.append()` the value from the gameArray that you want, using the API methods from parserAPI.py (eg., `parserAPI.getGameID()` returns the game ID, so appending it looks like this: `csvrow.append(parserAPI.getGameID())` ) <br>
A list of all of the possible game methods you can extract will be provided below, under `parserAPI.py`


## Program Logic

There are three python scripts that take care of the three major tasks involved: a parser (datafileParser.py), an interface for the user to interact with (csvGenerator.py), and an API that simplifies getting data from the parser (parserAPI.py)

<br><br>
`csvGenerator.py` <br>
...

<br><br>
`parserAPI.py` <br>
...

<br><br>
`datafileParser.py` <br>
...

