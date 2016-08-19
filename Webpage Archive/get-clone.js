
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

var link = process.argv[2];

if (!link) {
    console.log('ERR - A url must be passed in');
} else {
    console.log('Normalized url: ' + normalizeUrl(link));

}