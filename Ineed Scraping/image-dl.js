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

    if (printusage) {
        console.log('');
        console.log('Usage: image-dl -u <link to scrape> -f <folder to save images>');
        console.log('Example: ');
        console.log('       image-dl -u google.com');
        console.log('       image-dl -u google.com -f ~/Desktop/google/');
    }
});



// Program start
if (options.url !== undefined) {

    if (options.folder === undefined) {

        // use the url as the folder name
        folder = sanitize(options.url.match('[^/]*$')[0]);
        mkdirp.sync(folder);

    } else {
        folder = options.folder;

        // check that the specified folder exists

    }


    // Run the image collector on the url
    ineed.collect.images.from(parse_url(options.url), function (err, response, result) {

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

} else {
    eventEmitter.emit('error', 'A url must be specified', null, true);
}




// Iterate over all the images and download them
function request_images(result) {

    // if the folder already exists, mkdirp will ignore
    // mkdirp.sync();
    // console.log('Saving to %s', folder);

    // console.log('Starting array loop');

    result.images.forEach(function (imgstring) {

        // remove any invalid characters from the name
        var name = sanitize(imgstring.src.match('[^/]*$')[0]);

        // console.log('   -- requesting: ' + imgstring.src);

        // asynchronously request the image and write it to the Images folder
        request({
            uri: imgstring.src,
            encoding: null      // needed for writing the image as binary data
        }, function (err, resp, data) {
            if (!err && resp.statusCode === 200) {

                // console.log('   -- saving');

                // write the file
                fs.writeFile(folder + '/' + name, data, function (err) {
                    if (err) { 
                        console.log('ERROR - ' + err); 
                    } else {
                        console.log(colors.green('DONE') + ' - ' + imgstring.src);
                    }
                });

            } else {
                eventEmitter.emit('error', 'Image request failed', false);
                // console.log('ERROR - ' + err);
            }
        });
        

    });
}



