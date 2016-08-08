// #!/usr/bin/env node

const colors = require('colors/safe');
const sanitize = require('sanitize-filename');
const commandLineArgs = require('command-line-args');

const fs = require('fs');
const ineed = require('ineed');
const mkdirp = require('mkdirp');
const request = require('request');

// Event emitter to handle different use cases
const events = require('events');
const eventEmitter = new events();

var folder = '';

// Set the cli options
const cli = [
    {name: 'url', alias: 'u', type: String, multiple: false},
    {name: 'folder', alias: 'f', type: String, multiple: false}
];

// Parse the options passed in
const options = commandLineArgs(cli);


// console.log(options.url);


// Define the event emitters (BEFORE caling them)

// event emitter for handling errors
eventEmitter.on('error', function(message, err, printusage) {

    // Automatically log the error to the console
    if (err) {
        console.log(colors.red('ERROR') + ' - ' + message + ': ' + err);
    } else {
        console.log(colors.red('ERROR') + ' - ' + message);
    }

    // Print usage
    if (printusage) {
        console.log('');
        console.log('Usage: image-dl -u <link to scrape> -f <folder to save images>');
        console.log('Example: ');
        console.log('       image-dl -u google.com');
        console.log('       image-dl -u google.com -f ~/Desktop/google/');
    }
});


eventEmitter.on('start', function(link) {

    // instead of immediately scraping images, determine what kind of scraping
    // needs to be done (image, links, etc)
    // that way, different modules for scraping different sites can be implemented


    // Run the image collector on the url
    ineed.collect.images.from(parse_url(link), function (err, response, result) {

        if (err) {
            eventEmitter.emit('error', 'Link request failed', err, false);

        } else {
            console.log(colors.green('Extracting images from: %s'), options.url);

            console.log('Saving to folder: ' + folder);

            // Print out how many images were found
            if (result.images.length === 0) {
                console.log(result.images.length + ' image(s) found');

            } else {
                console.log(result.images.length + ' image(s) found - Requesting...');

                // call the function that gets all the image links
                request_images(result);
            }

        }
    });
});


// Iterate over all the images and download them
function request_images(result) {

    result.images.forEach(function (imgstring) {

        // remove any invalid characters from the name
        var imglink = imgstring.src;
        var name = sanitize(imglink.match('[^/]*$')[0]);

        // console.log('   -- requesting: ' + imgstring.src);

        // asynchronously request the image and write it to the Images folder
        request({
            uri: imglink,
            encoding: null      // needed for writing the image as binary data
        }, function (err, resp, data) {
            if (!err && resp.statusCode === 200) {

                // write the file
                fs.writeFile(folder + '/' + name, data, function (err) {
                    if (err) { 
                        console.log('ERROR - ' + err); 
                    } else {
                        console.log(colors.green('DONE') + ' - ' + imglink);
                    }
                });

            } else {
                eventEmitter.emit('error', 'Image request failed', err + ' (' + imglink + ')' , false);
            }
        });
    });
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


// start
switch (options.url) {
    case undefined:
        eventEmitter.emit('error', 'A url must be specified', null, true);
        break;
        
    default:
        if (options.folder === undefined) {
            // use the url as the folder name
            folder = sanitize(options.url.match('[^/]*$')[0]);
            mkdirp.sync(folder);

        } else {
            folder = options.folder;
            // check that the specified folder exists?
        }
        eventEmitter.emit('start', options.url);
}


