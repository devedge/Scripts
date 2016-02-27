## About

Python parser script for a poker dataset taken from [here](https://web.archive.org/web/20110205042259/http://www.outflopped.com/questions/286/obfuscated-datamined-hand-histories)

***


To use, [Download ZIP file](https://github.com/devedge/Scripts/raw/master/Poker%20Dataset%20Parser/PokerDatasetParser.zip), extract it, and in the directory, run: `python csvGenerator.py` from the command line. (Note: this has only been tested with Python 3.5)
<br><br>

Advanced: <br> 
Run with `python csvGenerator.py /absolute/path/to/dataset/folder output.csv y` <br>
The second argument (/absolute/path/to/dataset/folder) is absolute path to the dataset folder. All of the files in the folder must be the raw text files (eg., uncompress them before running the parser) <br><br>
The third argument is the CSV output file that will be generated. The fourth (and optional) argument (y), which means 'yes', is to overwrite the csv file specified if it already exists.<br><br>


## Program Logic

<br>

There are three python scripts that take care of the three major tasks involved: a parser (datafileParser.py), an interface for the user to interact with (csvGenerator.py), and an API that simplifies getting data from the parser (parserAPI.py)

<br><br>
`csvGenerator.py` <br>
...

<br><br>
`datafileParser.py` <br>
...

<br><br>
`parserAPI.py` <br>
...
