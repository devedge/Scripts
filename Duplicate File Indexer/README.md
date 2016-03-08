## ABout

A NodeJS script that hashes every file in a directory and its subdirectories to find duplicates. <br>
Any duplicate found is moved into a folder called `duplicates` one level above the searched folder. Also inside the folder is a log showing the original file, the one moved, and their full paths.
<br><br>

## Install

After unzipping [the file](), run this in the directory:

`$ npm install`

to install the packages locally.
<br><br>


## To Use:

Save the older duplicate files from the filepath "/folder/path/here"
```
$ node dfi_index.js --folder /folder/path/here --older
```

Save the newer duplicate files from the filepath "/folder/path/here"
```
$ node dfi_index.js --folder /folder/path/here --newer
```

(Default) Saves the older duplicate files from the filepath "/folder/path/here"
```
$ node dfi_index.js --folder /folder/path/here
```
