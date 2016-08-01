// #!/usr/bin/env node

const commandLineArgs = require('command-line-args');
const colors = require('colors/safe');

const request = require('request');
const mkdirp = require('mkdirp');
const ineed = require('ineed');
const fs = require('fs');


// Set the cli options
const cli = [
    {name: 'url', alias: 'u', type: String, multiple: false},
    {name: 'folder', alias: 'f', type: String, multiple: false}
];

// Parse the options passed in
const options = commandLineArgs(cli);

// var url = options.url;
// var folder = options.folder;

// console.log(options);

if (!(typeof options.url === undefined) && options.url !== null) {
    
    // If a folder hasn't been specified, create one here
    if (options.folder === null) {
        // make a folder in the current directory

    } else {
        // Use the specified folder 
        // folder = options.folder;
    }


    // Run the image collector on the url
    ineed.collect.images.from(parse_url(options.url), function (err, response, result) {

        if (err) {
            console.log(colors.red(err));
            print_usage();
            
        } else {
            console.log(colors.green('Extracting images from: %s'), options.url);
            console.log(result.images.length + ' image(s) found');

            // call the function that gets all the image links
            // fetch_links(result);
        }
    });

} else {
    // print error and usage info
    console.log(colors.red('ERROR - A url must be specified'));
    print_usage();
}




// Return a url that can safely be queried by the 'request' module
function parse_url(input) {
    // if the url starts with 'https://' or 'http://', don't add it
    // else add 'http://', since there may not be an https connection

    if ((input.match(/^https:\/\//) !== null) || 
        (input.match(/^http:\/\//) !== null)) {

        return input;
    } else {
        return 'http://' + input;
    }
}


// General application usage information
function print_usage() {
    console.log('');
    console.log('Usage: image-dl -u <link to scrape> -f <folder to save images>');
    console.log('Example: ');
    console.log('       image-dl -u google.com');
    console.log('       image-dl -u google.com -f ~/Desktop/google/');
}



// If the url hasn't been provided
// if (options.url === null) {
//     console.log('Usage:');
//     console.log('   image-dl -u <link to scrape> -f <folder to save images>');

//     process.exit();
// } else {


// }


// var url = 'https://github.com/devedge';






// make the images folder
// mkdirp.sync('Images');



// Iterate over all the images and download them
function fetch_links(result) {
    result.images.forEach(function (imgstring) {

        // remove any invalid characters from the name
        var name = imgstring.src.match('[^/]*$')[0]
                            .replace('&', '')
                            .replace('<', '')
                            .replace('>', '');

        // request the image and write it to the Images folder
        request({
            uri: imgstring.src,
            encoding: null      // needed for writing the image as binary data
        }, function (err, resp, data) {
            if (!err && resp.statusCode === 200) {

                // write the file
                fs.writeFile('Images/' + name, data, function (err) {
                    if (err) { 
                        console.log('ERROR - ' + err); 
                    } else {
                        console.log('DONE - ' + imgstring.src);
                    }
                });

            } else {
                console.log('ERROR - ' + err);
            }
        });
        

    });
}


// output

/*

Extracting images from <>...
63 images found
DONE - https
DONE - https




*/

