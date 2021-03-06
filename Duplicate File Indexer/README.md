## About

A NodeJS script that hashes every file in a directory and its subdirectories to find duplicates. <br>
Any duplicate found is moved into a folder called `duplicates` one level above the searched folder. Also inside the folder is a log showing the original file, the one moved, and their full paths.
<br><br>

## Install

After unzipping [the file](https://github.com/devedge/Scripts/raw/master/Duplicate%20File%20Indexer/data/DuplicateFileIndexer.zip), run this in the directory:

`$ npm install`

to install the packages locally.
<br><br>


## To Use:

Saves the older duplicate files and moves the newer versions to a `duplicates` folder
```
$ node duplicate_indexer.js --folder /folder/path/here --older
```

Saves the newer duplicate files and moves the older versions to a `duplicates` folder
```
$ node duplicate_indexer.js --folder /folder/path/here --newer
```

(Default) Saves the older duplicate files and moves the newer versions to a `duplicates` folder
```
$ node duplicate_indexer.js --folder /folder/path/here
```
