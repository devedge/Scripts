
// downloads a webpage and formats everything into a single html document

// issue warning about images that are too large 


// workflow
// provide a url to the script when run
// get the html
// use 'ineed' to find all js, css, images (and fonts?, etc..)
// convert them all to data:uri format and embed it in the html
// minimize the html to reduce filesize a little
// save the html to disk


const fs = require('fs');
const request = require('request');

const ineed = require('ineed');
const mkdirp = require('mkdirp');
const Datauri = require('datauri');
const normalizeUrl = require('normalize-url');
const colors = require('colors/safe');

var link = process.argv[2];

if (!link) {
    console.log('ERR - A url must be passed in');
} else {
    console.log('Normalized url: ' + colors.green(normalizeUrl(link)));

}



function request_root_page(link) {

    request({
        method: 'GET',
        uri: link,
        encoding: 'utf-8'/*,
        headers: {
            // add options to specify header options
        }*/
    }, function (err, resp, html) {
        if (err) {
            // Log error to console
            console.log(colors.red('ERR') + ' - ' + err);

        } else if (resp.statusCode !== 200) {
            // status code is not right, print error to console
            console.log(colors.red('ERR') + ' - ' + resp.statusCode + ' - ' + resp.statusMessage);

        } else {

        }
    });
}












