var commandLineArgs = require('command-line-args');
var recursive = require('recursive-readdir');
var pathmod = require('path');
var fs = require('fs');

// A Map to check for duplicates
var fileMap = new Map();

var duplicatesDir = 'duplicates/';
var saveOlder = true;
var printed = false;
var rootpath = '';

// node hashIndexer.js --folder /path/to/folder --older

// Get the user input from the command line, then
// parse the results
var cli = commandLineArgs([
    {name: 'folder', alias: 'f', type: String, multiple: false},
    {name: 'older', alias: 'o', type: Boolean},
    {name: 'newer', alias: 'n', type: Boolean}
]);

var options = cli.parse();

// Save the user options
rootpath = options.folder;
duplicatesDir = pathmod.join(pathmod.dirname(rootpath), duplicatesDir);

if (options.newer) {
    saveOlder = false;
} else if (options.older) {
    saveOlder = true;
}



// Iterate recursively over every folder and subfolder to get an array of files.
// Then call the hashAndMap() function to determine duplicates
recursive(rootpath, function (err, files) {

    // If an error happens, print it
    if (err) {console.log(err)};

    // Print out the number of files that have been found
    console.log("Parsing " + files.length + ' files');

    // For every file in the array, pass it to the hashAndMap() function
    for (var i = files.length - 1; i >= 0; i--) {
        hashAndMap(files[i], 'sha1');
    }

});



// Hashes the file and attempts to store it in a Map object.
// If there is already an entry, that means the current file
// is a duplicate, and it is moved to a 'duplicates' folder.
function hashAndMap(path, hashtype, cb) {
    var crypto = require('crypto');

    var fd = fs.createReadStream(path);
    var hash = crypto.createHash(hashtype);
    hash.setEncoding('hex');

    // When the hash is done
    fd.on('end', function() {
        hash.end();

        // Save the result
        var result = hash.read();

        // If it doesn't exist in the Map, save it with the
        // hash as the key and the filepath as the value for
        // the (key, value) pairs.
        if (typeof fileMap.get(result) === 'undefined') {
            fileMap.set(result, path);

        } else {

            // There is a duplicate, so call the function that moves the 
            // file to a 'duplicates' folder.
            movefile(path, fileMap.get(result), function (err) {
                if(err){
                    console.log('Could not move \'' + path + '\' for some reason')
                    console.log(err);
                }
            });
        }

        // If this is a callback, return (error, data)
        if (cb) {
            cb(null, result);
        }
    });

    // Pipe the file to the hash
    fd.pipe(hash);
};



// Moves one of the duplicate files ('path' or 'orig') into the 'duplicatesDir' 
// folder. Also creates a log of the original and duplicate files in the 
// 'duplicatesDir' folder.
function movefile(path, orig, cb) {
    var mkdirp = require('mkdirp');

    if (!printed) {console.log("Duplicates found. Saved at: " + duplicatesDir); printed = true;}

    // make the directory
    mkdirp(duplicatesDir, function(err) {

        filebydate(path, orig, saveOlder, function (returnedFile) {


            // check if both of the files still exist (messy workaround).
            // if one of them doesn't, return the other one (this means that the async move methods
            // moved one of the files before this one had a chance to do anything)
            fs.access(path, fs.F_OK, (err) => {
                // If the older file is no longer available, use the newer one
                if(err) {
                    returnedFile = orig;
                }
            });
            
            fs.access(orig, fs.F_OK, (err) => {
                // If the newer file is no longer available, use the older one
                if (err) {
                    returnedFile = path;
                }
            });


            // move the file
            fs.rename(returnedFile, pathmod.join(duplicatesDir, pathmod.basename(returnedFile)), function(err) {cb(err)});

            // append the duplicate error to a log
            var logfile = pathmod.join(duplicatesDir, 'duplicatelog.txt');

            // messy code to format logfile entries
            var m1 = 'Duplicate (orig) '
            var m2 = '          (dupl) '

            // indicate which file was moved
            if (returnedFile === orig) {
                m1 = m1 + '(moved): ' + orig + '\n';
                m2 = m2 + '       : ' + path + '\n';
                
            } else {
                m1 = m1 + '       : ' + orig + '\n';
                m2 = m2 + '(moved): ' + path + '\n';
            }

            var message = m1 + m2 + '\n';
            
            // append it to the log
            fs.appendFile(logfile, message, function(err) {cb(err)});
        });
    });
}



// Returns the oldest file. If 'getOlder' is true,
// return the oldest file, and if it is 'false' return
// the newer file
function filebydate(file1, file2, getOlder, cb) {

    var older = '';
    var newer = '';

    // find the oldest file
    if (fs.statSync(file1).birthtime.getTime() > fs.statSync(file2).birthtime.getTime()) {
        older = file2;
        newer = file1;
    } else {
        older = file1;
        newer = file2;
    }

    // based on the 'getOlder' boolean value, return the appropriate file
    if (getOlder) {
        cb(older);
    } else {
        cb(newer);
    }
}